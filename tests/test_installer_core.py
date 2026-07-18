#!/usr/bin/env python3
"""Test del nucleo installazione/ripristino senza modificare il gioco reale."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "star_citizen_it_installer.py"
)
SPEC = importlib.util.spec_from_file_location("star_citizen_it_installer", SCRIPT)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


def configure_work_dir(root: Path) -> None:
    installer.USER_WORK_DIR = root / "work"
    installer.SETTINGS_PATH = installer.USER_WORK_DIR / "settings.json"
    installer.STATE_PATH = installer.USER_WORK_DIR / "installed_state.json"
    installer.process_running = lambda: []


def create_fake_game(root: Path, change: str = installer.SUPPORTED_P4_CHANGE) -> Path:
    game = root / "StarCitizen" / "LIVE"
    (game / "Bin64").mkdir(parents=True)
    (game / "Bin64" / "StarCitizen.exe").write_bytes(b"")
    (game / "Data.p4k").write_bytes(b"fake")
    manifest = {
        "Data": {
            "Branch": installer.SUPPORTED_BRANCH,
            "Version": "4.9.test",
            "RequestedP4ChangeNum": change,
            "BuildDateStamp": "Test Day",
            "BuildTimeStamp": "12:00:00",
        }
    }
    (game / installer.BUILD_MANIFEST_NAME).write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return game


def test_payload() -> None:
    payload = installer.source_payload_root() / installer.TARGET_GLOBAL_REL
    report = installer.validate_payload(payload)
    assert report["entries"] == installer.EXPECTED_ENTRIES
    assert report["sha256"] == installer.EXPECTED_PAYLOAD_SHA256


def test_cfg_roundtrip() -> None:
    original = (
        b"r_Width=1920\r\n"
        b"g_language=french\r\n"
        b"g_LanguageAudio=french\r\n"
        b"g_language=german\r\n"
    )
    installed = installer.update_user_cfg(original)
    text = installed.decode("utf-8")
    assert text.count("g_language=") == 1
    assert text.count("g_LanguageAudio=") == 1
    assert "g_language=italian_(italy)" in text
    assert "g_LanguageAudio=english" in text
    assert "r_Width=1920" in text

    modified = installed + b"r_Height=1080\r\n"
    restored = installer.restore_user_cfg_settings(modified, original).decode("utf-8")
    assert "g_language=french" in restored
    assert "g_LanguageAudio=french" in restored
    assert "g_language=italian_(italy)" not in restored
    assert "r_Height=1080" in restored

    created = installer.update_user_cfg(None)
    removed = installer.restore_user_cfg_settings(created, None)
    assert removed == b""


def test_detection_and_build() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root)
        assert installer.looks_like_game_dir(game)
        assert installer.normalize_selected_game_dir(game.parent) == game.resolve()
        info = installer.read_build_info(game)
        assert installer.compatibility_status(info) == (True, "LIVE 4.9 verificata")

        old_env = os.environ.get("STAR_CITIZEN_LIVE")
        os.environ["STAR_CITIZEN_LIVE"] = str(game)
        try:
            found, source = installer.resolve_game_dir_with_source()
            assert found == game.resolve()
            assert source == "variabile di ambiente"
        finally:
            if old_env is None:
                os.environ.pop("STAR_CITIZEN_LIVE", None)
            else:
                os.environ["STAR_CITIZEN_LIVE"] = old_env


def test_install_and_restore_created_files() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root)
        report = installer.install_translation(game, force_open=True)
        paths = installer.resolve_paths(game)
        assert report["status"]["matches_current"] is True
        assert installer.sha256_file(paths.target_global) == installer.EXPECTED_PAYLOAD_SHA256
        assert paths.user_cfg.is_file()
        assert installer.STATE_PATH.is_file()

        current = paths.user_cfg.read_bytes() + b"r_CustomSetting=1\r\n"
        paths.user_cfg.write_bytes(current)
        restored = installer.restore_translation(game, force_open=True)
        assert not paths.target_global.exists()
        assert paths.user_cfg.read_text(encoding="utf-8") == "r_CustomSetting=1\n"
        assert not installer.STATE_PATH.exists()
        assert restored["conflicts_saved"] == []


def test_install_and_restore_existing_files() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root)
        paths = installer.resolve_paths(game)
        paths.target_global.parent.mkdir(parents=True)
        original_global = b"custom=original\r\n"
        paths.target_global.write_bytes(original_global)
        original_cfg = (
            b"r_Width=2560\r\n"
            b"g_language=german\r\n"
            b"g_LanguageAudio=german\r\n"
        )
        paths.user_cfg.write_bytes(original_cfg)

        installer.install_translation(game, force_open=True)
        paths.target_global.write_bytes(b"custom=changed-after-install\r\n")
        paths.user_cfg.write_bytes(paths.user_cfg.read_bytes() + b"r_NewSetting=7\r\n")
        restored = installer.restore_translation(game, force_open=True)

        assert paths.target_global.read_bytes() == original_global
        cfg = paths.user_cfg.read_text(encoding="utf-8")
        assert "r_Width=2560" in cfg
        assert "r_NewSetting=7" in cfg
        assert "g_language=german" in cfg
        assert "g_LanguageAudio=german" in cfg
        assert "italian_(italy)" not in cfg
        assert len(restored["conflicts_saved"]) == 1
        assert Path(restored["conflicts_saved"][0]).read_bytes() == (
            b"custom=changed-after-install\r\n"
        )


def test_rejects_unverified_build() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root, change="99999999")
        original_probe = installer.inspect_source_localization
        installer.inspect_source_localization = lambda _game_dir: {
            "available": True,
            "matches": False,
            "sha256": "CHANGED",
            "bytes": 1,
            "error": None,
        }
        try:
            try:
                installer.install_translation(game, force_open=True)
            except RuntimeError as exc:
                assert "non è ancora verificata" in str(exc)
                assert "localizzazione inglese" in str(exc)
            else:
                raise AssertionError(
                    "Una build con sorgente inglese cambiata è stata accettata."
                )
        finally:
            installer.inspect_source_localization = original_probe


def test_accepts_new_build_when_source_is_identical() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root, change="12248363")
        info = installer.read_build_info(game)
        original_probe = installer.inspect_source_localization
        installer.inspect_source_localization = lambda _game_dir: {
            "available": True,
            "matches": True,
            "sha256": installer.EXPECTED_SOURCE_SHA256,
            "bytes": installer.EXPECTED_SOURCE_BYTES,
            "error": None,
        }
        try:
            report = installer.compatibility_report(info, game)
            assert report["compatible"] is True
            assert report["method"] == "source_sha256"
            assert "sorgente inglese invariata" in report["reason"]

            manifest = json.loads((game / installer.BUILD_MANIFEST_NAME).read_text())
            manifest["Data"]["Branch"] = "sc-alpha-4.10.0"
            (game / installer.BUILD_MANIFEST_NAME).write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            future = installer.compatibility_report(
                installer.read_build_info(game),
                game,
            )
            assert future["compatible"] is True
            assert future["method"] == "source_sha256"
        finally:
            installer.inspect_source_localization = original_probe


def main() -> int:
    tests = [
        test_payload,
        test_cfg_roundtrip,
        test_detection_and_build,
        test_install_and_restore_created_files,
        test_install_and_restore_existing_files,
        test_rejects_unverified_build,
        test_accepts_new_build_when_source_is_identical,
    ]
    for test in tests:
        test()
    print(f"installer_core: {len(tests)}/{len(tests)} controlli superati")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

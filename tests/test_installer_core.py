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
            "Version": "4.10.test",
            "RequestedP4ChangeNum": change,
            "BuildDateStamp": "Test Day",
            "BuildTimeStamp": "12:00:00",
        }
    }
    (game / installer.BUILD_MANIFEST_NAME).write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return game


class FakeResponse:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _traceback):
        return False

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self.data) - self.offset
        chunk = self.data[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk


def fake_release(payload: bytes, *, digest_payload: bytes | None = None) -> dict:
    digest_payload = payload if digest_payload is None else digest_payload
    return {
        "tag_name": "sc-4.10-r3",
        "html_url": (
            "https://github.com/Sici29/SC-Italian-Translation/releases/tag/sc-4.10-r3"
        ),
        "draft": False,
        "prerelease": False,
        "assets": [
            {
                "name": "StarCitizen_Traduzione_Italiana_4.10_R3.exe",
                "state": "uploaded",
                "size": len(payload),
                "digest": "sha256:" + installer.sha256_bytes(digest_payload).lower(),
                "browser_download_url": (
                    "https://github.com/Sici29/SC-Italian-Translation/releases/"
                    "download/sc-4.10-r3/StarCitizen_Traduzione_Italiana_4.10_R3.exe"
                ),
            }
        ],
    }


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
        assert installer.compatibility_status(info) == (True, "LIVE 4.10 verificata")

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


def test_restore_refuses_stale_backup_without_active_state() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root)
        installer.install_translation(game, force_open=True)
        paths = installer.resolve_paths(game)
        installed_hash = installer.sha256_file(paths.target_global)
        installer.STATE_PATH.unlink()

        try:
            installer.restore_translation(game, force_open=True)
        except FileNotFoundError as exc:
            assert "installazione attiva" in str(exc)
        else:
            raise AssertionError("Un vecchio backup è stato ripristinato senza stato attivo.")

        assert paths.target_global.is_file()
        assert installer.sha256_file(paths.target_global) == installed_hash
        assert paths.user_cfg.is_file()


def test_restore_uses_only_recorded_active_backup() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        game = create_fake_game(root)
        report = installer.install_translation(game, force_open=True)
        active_backup = Path(report["backup"])

        stale = installer.USER_WORK_DIR / "backups" / "99999999-999999-999999"
        stale.mkdir(parents=True)
        (stale / "backup_manifest.json").write_text(
            json.dumps(
                {
                    "game_dir": str(game.resolve()),
                    "translation_version": "0.0-stale",
                    "original_global_exists": True,
                    "original_user_cfg_exists": False,
                }
            ),
            encoding="utf-8",
        )
        (stale / "original_global.ini").write_bytes(b"stale=wrong\r\n")

        restored = installer.restore_translation(game, force_open=True)
        assert Path(restored["backup"]) == active_backup
        assert not installer.resolve_paths(game).target_global.exists()


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
        game = create_fake_game(root, change="12599999")
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
            manifest["Data"]["Branch"] = "sc-alpha-4.11.0"
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


def test_release_update_metadata() -> None:
    payload = b"MZ-test-installer"
    release = fake_release(payload)
    original_urlopen = installer.urllib.request.urlopen
    installer.urllib.request.urlopen = lambda _request, timeout=0: FakeResponse(
        json.dumps(release).encode("utf-8")
    )
    try:
        latest = installer.check_latest_release()
    finally:
        installer.urllib.request.urlopen = original_urlopen

    assert installer.release_version_key("sc-4.10-r1") == (4, 10, 1)
    assert installer.release_version_key("sc-4.10-r2") == (4, 10, 2)
    assert installer.release_version_key("sc-4.11-r1") == (4, 11, 1)
    assert installer.release_version_key("sc-4.11-r1") > installer.release_version_key(
        installer.RELEASE_TAG
    )
    assert installer.release_version_key("formato-ignoto") is None
    assert latest["available"] is True
    assert latest["download_ready"] is True
    assert latest["latest"] == "sc-4.10-r3"
    assert latest["asset"]["size"] == len(payload)
    assert latest["asset"]["sha256"] == installer.sha256_bytes(payload)


def test_release_update_handles_invalid_utf8() -> None:
    original_urlopen = installer.urllib.request.urlopen
    installer.urllib.request.urlopen = lambda _request, timeout=0: FakeResponse(b"\xff")
    try:
        latest = installer.check_latest_release()
    finally:
        installer.urllib.request.urlopen = original_urlopen

    assert latest["available"] is None
    assert latest["current"] == installer.RELEASE_TAG
    assert latest["error"]


def test_release_asset_identity_is_strict() -> None:
    release = fake_release(b"MZ-test-installer")
    release["assets"][0]["name"] = "StarCitizen_Traduzione_Italiana_4.10_R2.exe"
    try:
        installer.select_installer_asset(release)
    except RuntimeError as exc:
        assert "un solo installer" in str(exc)
    else:
        raise AssertionError("È stato accettato un nome EXE incoerente con il tag.")

    release = fake_release(b"MZ-test-installer")
    release["assets"][0]["browser_download_url"] = (
        "https://github.com/Sici29/SC-Italian-Translation/releases/download/"
        "sc-4.10-r4/StarCitizen_Traduzione_Italiana_4.10_R3.exe"
    )
    try:
        installer.select_installer_asset(release)
    except RuntimeError as exc:
        assert "non appartiene" in str(exc)
    else:
        raise AssertionError("È stato accettato un URL incoerente con il tag.")

    release = fake_release(b"MZ-test-installer")
    release["assets"][0]["browser_download_url"] = (
        "https://github.com/Sici29/SC-Italian-Translation/releases/download/"
        "sc-4.10-r3/installer_diverso.exe"
    )
    try:
        installer.select_installer_asset(release)
    except RuntimeError as exc:
        assert "non appartiene" in str(exc)
    else:
        raise AssertionError("È stato accettato un URL con nome file incoerente.")


def test_download_update_verifies_and_reuses_file() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        payload = b"MZ-test-installer"
        release = fake_release(payload)
        latest = {
            "available": True,
            "download_ready": True,
            "latest": release["tag_name"],
            "asset": installer.select_installer_asset(release),
        }
        original_urlopen = installer.urllib.request.urlopen
        installer.urllib.request.urlopen = lambda _request, timeout=0: FakeResponse(payload)
        try:
            downloaded = installer.download_release_installer(latest)
            reused = installer.download_release_installer(latest)
        finally:
            installer.urllib.request.urlopen = original_urlopen

        path = Path(downloaded["path"])
        assert path.read_bytes() == payload
        assert downloaded["sha256"] == installer.sha256_bytes(payload)
        assert downloaded["reused"] is False
        assert reused["reused"] is True
        assert reused["path"] == downloaded["path"]


def test_download_update_rejects_wrong_digest() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        expected = b"MZ-new"
        received = b"MZ-bad"
        release = fake_release(received, digest_payload=expected)
        latest = {
            "available": True,
            "download_ready": True,
            "latest": release["tag_name"],
            "asset": installer.select_installer_asset(release),
        }
        original_urlopen = installer.urllib.request.urlopen
        installer.urllib.request.urlopen = lambda _request, timeout=0: FakeResponse(received)
        try:
            try:
                installer.download_release_installer(latest)
            except RuntimeError as exc:
                assert "SHA-256" in str(exc)
            else:
                raise AssertionError("È stato accettato un installer con hash errato.")
        finally:
            installer.urllib.request.urlopen = original_urlopen

        assert not list(installer.USER_WORK_DIR.rglob("*.exe"))
        assert not list(installer.USER_WORK_DIR.rglob("*.part"))


def test_launch_update_uses_verified_file() -> None:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        configure_work_dir(root)
        update_dir = installer.USER_WORK_DIR / "updates" / "sc-4.10-r2"
        update_dir.mkdir(parents=True)
        path = update_dir / "StarCitizen_Traduzione_Italiana_4.10_R2.exe"
        payload = b"MZ-test-installer"
        path.write_bytes(payload)
        calls = []
        events = []
        original_popen = installer.subprocess.Popen
        original_release_lock = installer.release_installer_instance_lock

        def fake_release_lock() -> None:
            events.append("release")

        def fake_popen(*args, **kwargs):
            events.append("popen")
            calls.append((args, kwargs))

        installer.release_installer_instance_lock = fake_release_lock
        installer.subprocess.Popen = fake_popen
        try:
            installer.launch_installer_update(
                {
                    "path": str(path),
                    "sha256": installer.sha256_bytes(payload),
                }
            )
        finally:
            installer.subprocess.Popen = original_popen
            installer.release_installer_instance_lock = original_release_lock

        assert events == ["release", "popen"]
        assert calls
        assert calls[0][0][0] == [str(path.resolve())]
        assert calls[0][1]["cwd"] == str(path.parent.resolve())


def main() -> int:
    tests = [
        test_payload,
        test_cfg_roundtrip,
        test_detection_and_build,
        test_install_and_restore_created_files,
        test_install_and_restore_existing_files,
        test_restore_refuses_stale_backup_without_active_state,
        test_restore_uses_only_recorded_active_backup,
        test_rejects_unverified_build,
        test_accepts_new_build_when_source_is_identical,
        test_release_update_metadata,
        test_release_update_handles_invalid_utf8,
        test_release_asset_identity_is_strict,
        test_download_update_verifies_and_reuses_file,
        test_download_update_rejects_wrong_digest,
        test_launch_update_uses_verified_file,
    ]
    for test in tests:
        test()
    print(f"installer_core: {len(tests)}/{len(tests)} controlli superati")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

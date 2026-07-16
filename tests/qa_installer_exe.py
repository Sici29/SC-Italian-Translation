#!/usr/bin/env python3
"""Collaudo end-to-end dell'EXE in un'installazione LIVE simulata."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


EXPECTED_PAYLOAD_SHA256 = "CEB1189451F36F07F9A9A2C9D39E5FFF8FB9100D81B760094F72E357040062C8"
TARGET_REL = Path("Data") / "Localization" / "italian_(italy)" / "global.ini"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run(exe: Path, args: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        [str(exe), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Comando non riuscito ({result.returncode}): {' '.join(args)}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("exe", type=Path)
    args = parser.parse_args()
    exe = args.exe.resolve()
    if not exe.is_file():
        raise FileNotFoundError(exe)

    with TemporaryDirectory() as folder:
        root = Path(folder)
        game = root / "StarCitizen" / "LIVE"
        (game / "Bin64").mkdir(parents=True)
        (game / "Bin64" / "StarCitizen.exe").write_bytes(b"")
        (game / "Data.p4k").write_bytes(b"sandbox")
        manifest = {
            "Data": {
                "Branch": "sc-alpha-4.9.0",
                "Version": "4.9.qa",
                "RequestedP4ChangeNum": "12232306",
                "BuildDateStamp": "QA",
                "BuildTimeStamp": "00:00:00",
            }
        }
        (game / "build_manifest.id").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        work = root / "work"
        env = dict(os.environ)
        env["SC_IT_WORK_DIR"] = str(work)
        env["STAR_CITIZEN_LIVE"] = str(game)

        install_output = run(
            exe,
            ["install", "--game-dir", str(game), "--force-open"],
            env,
        )
        target = game / TARGET_REL
        assert target.is_file()
        assert sha256(target) == EXPECTED_PAYLOAD_SHA256
        cfg = (game / "user.cfg").read_text(encoding="utf-8")
        assert "g_language=italian_(italy)" in cfg
        assert "g_LanguageAudio=english" in cfg
        assert (work / "installed_state.json").is_file()
        assert list((work / "backups").glob("*/backup_manifest.json"))

        check_output = run(exe, ["check", "--game-dir", str(game)], env)
        check = json.loads(check_output)
        assert check["compatible"] is True
        assert check["translation"]["matches_current"] is True

        with (game / "user.cfg").open("ab") as stream:
            stream.write(b"r_QASetting=1\r\n")
        restore_output = run(
            exe,
            ["restore", "--game-dir", str(game), "--force-open"],
            env,
        )
        assert not target.exists()
        assert (game / "user.cfg").read_text(encoding="utf-8") == "r_QASetting=1\n"
        assert not (work / "installed_state.json").exists()

        print("installer_exe_qa: installazione, verifica e ripristino superati")
        print("install_output:", install_output.splitlines()[0])
        print("restore_output:", restore_output.splitlines()[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

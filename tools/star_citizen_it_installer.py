#!/usr/bin/env python3
"""Installer pubblico della localizzazione italiana non ufficiale di Star Citizen."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from dataclasses import asdict, dataclass
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


APP_TITLE = "Star Citizen - Traduzione Italiana Non Ufficiale"
TRANSLATION_VERSION = "4.9-R1"
RELEASE_TAG = "sc-4.9-r1"
INSTALLER_FILENAME = "StarCitizen_Traduzione_Italiana_4.9_R1.exe"
SUPPORTED_BRANCH = "sc-alpha-4.9.0"
SUPPORTED_P4_CHANGE = "12232306"
EXPECTED_ENTRIES = 90121
EXPECTED_PAYLOAD_SHA256 = "CEB1189451F36F07F9A9A2C9D39E5FFF8FB9100D81B760094F72E357040062C8"

GITHUB_PROJECT_URL = "https://github.com/Sici29/SC-Italian-Translation"
GITHUB_RELEASES_URL = GITHUB_PROJECT_URL + "/releases"
GITHUB_ISSUES_URL = GITHUB_PROJECT_URL + "/issues"
GITHUB_API_LATEST = (
    "https://api.github.com/repos/Sici29/SC-Italian-Translation/releases/latest"
)

TARGET_GLOBAL_REL = Path("Data") / "Localization" / "italian_(italy)" / "global.ini"
BUILD_MANIFEST_NAME = "build_manifest.id"
USER_CFG_NAME = "user.cfg"
LANGUAGE_SETTINGS = {
    "g_language": "g_language=italian_(italy)",
    "g_languageaudio": "g_LanguageAudio=english",
}

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
else:
    APP_DIR = Path(__file__).resolve().parent
    BUNDLE_DIR = APP_DIR

USER_WORK_DIR = Path(
    os.environ.get("SC_IT_WORK_DIR")
    or (Path.home() / "Documents" / "StarCitizenItalianTranslation")
)
SETTINGS_PATH = USER_WORK_DIR / "settings.json"
STATE_PATH = USER_WORK_DIR / "installed_state.json"
_INSTANCE_MUTEX = None


class ConsoleColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"


@dataclass(frozen=True)
class BuildInfo:
    branch: str
    version: str
    requested_p4_change: str
    build_date: str
    build_time: str


@dataclass(frozen=True)
class GamePaths:
    game_dir: Path
    build_manifest: Path
    target_global: Path
    user_cfg: Path


def color_text(text: str, color: str, enabled: bool) -> str:
    return f"{color}{text}{ConsoleColor.RESET}" if enabled else text


def enable_console_colors() -> bool:
    if not sys.stdout.isatty():
        return False
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


def write_json(path: Path, value: object) -> None:
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic_write_bytes(path, payload)


def source_payload_root() -> Path:
    if getattr(sys, "frozen", False):
        candidates = [BUNDLE_DIR / "payload"]
    else:
        script = Path(__file__).resolve()
        candidates = [
            script.parents[2] / "03_PATCH" / "PAYLOAD",
            script.parents[1] / "translation",
            script.parent / "translation",
            BUNDLE_DIR / "payload",
        ]
    for candidate in candidates:
        if (candidate / TARGET_GLOBAL_REL).is_file():
            return candidate
    checked = "\n".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Payload italiano non trovato. Percorsi controllati:\n{checked}")


def validate_payload(path: Path) -> dict:
    raw = path.read_bytes()
    digest = sha256_bytes(raw)
    if digest != EXPECTED_PAYLOAD_SHA256:
        raise RuntimeError(
            "Il file italiano incorporato non supera il controllo di integrità. "
            "Scarica nuovamente l'installer dalla pagina ufficiale del progetto."
        )
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Il file italiano incorporato non usa la codifica prevista.")
    lines = raw.decode("utf-8-sig").splitlines()
    if len(lines) != EXPECTED_ENTRIES:
        raise RuntimeError(
            f"Il file italiano contiene {len(lines)} righe invece delle {EXPECTED_ENTRIES} previste."
        )
    keys: set[str] = set()
    malformed = 0
    for line in lines:
        if "=" not in line:
            malformed += 1
            continue
        key = line.split("=", 1)[0]
        if key in keys:
            raise RuntimeError(f"Chiave duplicata nel payload italiano: {key}")
        keys.add(key)
    if malformed:
        raise RuntimeError(f"Il payload italiano contiene {malformed} righe non valide.")
    return {"path": str(path), "sha256": digest, "entries": len(lines), "bytes": len(raw)}


def resolve_paths(game_dir: Path) -> GamePaths:
    game_dir = game_dir.expanduser().resolve()
    return GamePaths(
        game_dir=game_dir,
        build_manifest=game_dir / BUILD_MANIFEST_NAME,
        target_global=game_dir / TARGET_GLOBAL_REL,
        user_cfg=game_dir / USER_CFG_NAME,
    )


def looks_like_game_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "Data.p4k").is_file()
        and (path / BUILD_MANIFEST_NAME).is_file()
        and (path / "Bin64" / "StarCitizen.exe").is_file()
    )


def normalize_selected_game_dir(path: Path) -> Path | None:
    path = path.expanduser()
    candidates = [path, path / "LIVE", path / "StarCitizen" / "LIVE"]
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if looks_like_game_dir(resolved):
            return resolved
    return None


def load_settings() -> dict:
    return read_json(SETTINGS_PATH)


def save_game_dir(game_dir: Path) -> None:
    settings = load_settings()
    settings["game_dir"] = str(game_dir.resolve())
    write_json(SETTINGS_PATH, settings)


def candidate_game_dirs() -> list[tuple[Path, str]]:
    candidates: list[tuple[Path, str]] = []
    env = os.environ.get("STAR_CITIZEN_LIVE") or os.environ.get("STAR_CITIZEN_GAME_DIR")
    if env:
        candidates.append((Path(env), "variabile di ambiente"))
    saved = str(load_settings().get("game_dir") or "").strip()
    if saved:
        candidates.append((Path(saved), "percorso salvato"))

    candidates.extend((path, "accanto all'installer") for path in (APP_DIR, *APP_DIR.parents[:3]))
    cwd = Path.cwd()
    candidates.extend((path, "cartella corrente") for path in (cwd, *cwd.parents[:3]))

    if os.name == "nt":
        layouts = (
            Path("Robert Space Industries") / "StarCitizen" / "LIVE",
            Path("Roberts Space Industries") / "StarCitizen" / "LIVE",
            Path("Program Files") / "Roberts Space Industries" / "StarCitizen" / "LIVE",
            Path("Program Files") / "Robert Space Industries" / "StarCitizen" / "LIVE",
            Path("RSI") / "StarCitizen" / "LIVE",
            Path("StarCitizen") / "LIVE",
        )
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            root = Path(f"{letter}:\\")
            if root.exists():
                candidates.extend((root / layout, "rilevamento automatico") for layout in layouts)

    unique: list[tuple[Path, str]] = []
    seen: set[str] = set()
    for path, source in candidates:
        key = os.path.normcase(os.path.abspath(str(path)))
        if key not in seen:
            unique.append((path, source))
            seen.add(key)
    return unique


def resolve_game_dir_with_source(raw: str | None = None) -> tuple[Path, str]:
    if raw:
        normalized = normalize_selected_game_dir(Path(raw.strip().strip('"')))
        if normalized:
            return normalized, "manuale"
        raise FileNotFoundError("La cartella scelta non contiene una installazione LIVE valida.")
    for candidate, source in candidate_game_dirs():
        normalized = normalize_selected_game_dir(candidate)
        if normalized:
            return normalized, source
    raise FileNotFoundError("La cartella LIVE di Star Citizen non è stata trovata.")


def choose_game_dir_windows() -> str | None:
    if os.name != "nt":
        return None
    script = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$d=New-Object System.Windows.Forms.FolderBrowserDialog; "
        "$d.Description='Seleziona la cartella LIVE di Star Citizen'; "
        "$d.ShowNewFolderButton=$false; "
        "if($d.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){$d.SelectedPath}"
    )
    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-STA", "-Command", script],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return output or None


def configure_game_dir() -> Path | None:
    print("Seleziona la cartella LIVE che contiene Data.p4k e Bin64.")
    print(r"Esempio: D:\Robert Space Industries\StarCitizen\LIVE")
    raw = choose_game_dir_windows()
    if not raw:
        raw = input("Percorso della cartella LIVE (Invio per annullare): ").strip().strip('"')
    if not raw:
        return None
    try:
        game_dir, _ = resolve_game_dir_with_source(raw)
    except FileNotFoundError as exc:
        print(exc)
        return None
    save_game_dir(game_dir)
    print("Percorso verificato e salvato:", game_dir)
    return game_dir


def read_build_info(game_dir: Path) -> BuildInfo:
    manifest = read_json(game_dir / BUILD_MANIFEST_NAME)
    data = manifest.get("Data") if isinstance(manifest.get("Data"), dict) else {}
    if not data:
        raise RuntimeError("Il manifest della build non è leggibile.")
    return BuildInfo(
        branch=str(data.get("Branch") or ""),
        version=str(data.get("Version") or ""),
        requested_p4_change=str(data.get("RequestedP4ChangeNum") or ""),
        build_date=str(data.get("BuildDateStamp") or ""),
        build_time=str(data.get("BuildTimeStamp") or ""),
    )


def compatibility_status(info: BuildInfo) -> tuple[bool, str]:
    if info.branch != SUPPORTED_BRANCH:
        return False, f"canale/build {info.branch or 'non identificata'} non supportata"
    if info.requested_p4_change != SUPPORTED_P4_CHANGE:
        return False, (
            f"change {info.requested_p4_change or 'non identificato'} non verificato; "
            f"atteso {SUPPORTED_P4_CHANGE}"
        )
    return True, "LIVE 4.9 verificata"


def decode_text(raw: bytes) -> tuple[str, bool]:
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    try:
        return raw.decode("utf-8-sig"), has_bom
    except UnicodeDecodeError:
        return raw.decode("cp1252"), False


def cfg_key(line: str) -> str | None:
    match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
    return match.group(1).casefold() if match else None


def language_values(raw: bytes | None) -> dict[str, str]:
    if raw is None:
        return {}
    text, _ = decode_text(raw)
    values: dict[str, str] = {}
    for line in text.splitlines():
        key = cfg_key(line)
        if key in LANGUAGE_SETTINGS and key not in values:
            values[key] = line
    return values


def update_user_cfg(original: bytes | None) -> bytes:
    text, has_bom = decode_text(original or b"")
    output: list[str] = []
    written: set[str] = set()
    for line in text.splitlines():
        key = cfg_key(line)
        if key in LANGUAGE_SETTINGS:
            if key not in written:
                output.append(LANGUAGE_SETTINGS[key])
                written.add(key)
            continue
        output.append(line)
    if output and output[-1].strip():
        output.append("")
    for key, value in LANGUAGE_SETTINGS.items():
        if key not in written:
            output.append(value)
    rendered = "\r\n".join(output).rstrip("\r\n") + "\r\n"
    prefix = b"\xef\xbb\xbf" if has_bom else b""
    return prefix + rendered.encode("utf-8")


def restore_user_cfg_settings(current: bytes, original: bytes | None) -> bytes:
    original_values = language_values(original)
    text, has_bom = decode_text(current)
    output: list[str] = []
    written: set[str] = set()
    for line in text.splitlines():
        key = cfg_key(line)
        if key in LANGUAGE_SETTINGS:
            if key in original_values and key not in written:
                output.append(original_values[key])
                written.add(key)
            continue
        output.append(line)
    for key, value in original_values.items():
        if key not in written:
            if output and output[-1].strip():
                output.append("")
            output.append(value)
    rendered = "\r\n".join(output).rstrip("\r\n")
    if rendered:
        rendered += "\r\n"
    prefix = b"\xef\xbb\xbf" if has_bom and rendered else b""
    return prefix + rendered.encode("utf-8")


def process_running() -> list[str]:
    if os.name != "nt":
        return []
    try:
        output = subprocess.check_output(
            ["tasklist", "/FO", "CSV", "/NH"],
            text=True,
            encoding="utf-8",
            errors="replace",
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return []
    watched = {
        "starcitizen.exe",
        "starcitizen_launcher.exe",
        "rsi launcher.exe",
        "rsi launcher service.exe",
    }
    found: set[str] = set()
    for row in csv.reader(output.splitlines()):
        if row and row[0].casefold() in watched:
            found.add(row[0])
    return sorted(found, key=str.casefold)


def backup_live(paths: GamePaths, info: BuildInfo) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{time.time_ns() % 1_000_000:06d}"
    backup = USER_WORK_DIR / "backups" / stamp
    backup.mkdir(parents=True, exist_ok=False)
    original_global = paths.target_global.is_file()
    original_user_cfg = paths.user_cfg.is_file()
    if original_global:
        shutil.copy2(paths.target_global, backup / "original_global.ini")
    if original_user_cfg:
        shutil.copy2(paths.user_cfg, backup / "original_user.cfg")
    metadata = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "game_dir": str(paths.game_dir),
        "build": asdict(info),
        "translation_version": TRANSLATION_VERSION,
        "original_global_exists": original_global,
        "original_user_cfg_exists": original_user_cfg,
        "original_global_sha256": sha256_file(paths.target_global) if original_global else None,
        "original_user_cfg_sha256": sha256_file(paths.user_cfg) if original_user_cfg else None,
    }
    write_json(backup / "backup_manifest.json", metadata)
    return backup


def load_installed_state() -> dict:
    return read_json(STATE_PATH)


def record_installed_state(
    paths: GamePaths,
    info: BuildInfo,
    backup: Path,
    installed_user_cfg: bytes,
) -> dict:
    state = {
        "installed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "game_dir": str(paths.game_dir),
        "translation_version": TRANSLATION_VERSION,
        "release_tag": RELEASE_TAG,
        "payload_sha256": EXPECTED_PAYLOAD_SHA256,
        "installed_user_cfg_sha256": sha256_bytes(installed_user_cfg),
        "backup": str(backup),
        "build": asdict(info),
    }
    write_json(STATE_PATH, state)
    return state


def clear_installed_state(game_dir: Path) -> None:
    state = load_installed_state()
    recorded = str(state.get("game_dir") or "")
    if recorded and os.path.normcase(recorded) == os.path.normcase(str(game_dir)):
        try:
            STATE_PATH.unlink(missing_ok=True)
        except OSError:
            pass


def translation_status(paths: GamePaths) -> dict:
    global_exists = paths.target_global.is_file()
    global_hash = sha256_file(paths.target_global) if global_exists else None
    user_raw = paths.user_cfg.read_bytes() if paths.user_cfg.is_file() else None
    values = language_values(user_raw)
    language_ok = values.get("g_language", "").replace(" ", "").casefold() == (
        "g_language=italian_(italy)"
    )
    audio_ok = values.get("g_languageaudio", "").replace(" ", "").casefold() == (
        "g_languageaudio=english"
    )
    payload_ok = global_hash == EXPECTED_PAYLOAD_SHA256
    return {
        "installed": bool(global_exists and language_ok),
        "matches_current": bool(payload_ok and language_ok and audio_ok),
        "global_exists": global_exists,
        "global_sha256": global_hash,
        "payload_matches": payload_ok,
        "language_configured": language_ok,
        "english_audio_configured": audio_ok,
        "recorded_version": load_installed_state().get("translation_version"),
    }


def copy_conflict(path: Path, backup: Path, label: str) -> Path | None:
    if not path.is_file():
        return None
    conflict_dir = backup / "modifiche_successive"
    conflict_dir.mkdir(parents=True, exist_ok=True)
    destination = conflict_dir / label
    shutil.copy2(path, destination)
    return destination


def remove_empty_translation_dirs(paths: GamePaths) -> None:
    stop = paths.game_dir / "Data"
    current = paths.target_global.parent
    while current != stop.parent and current != paths.game_dir:
        try:
            current.rmdir()
        except OSError:
            break
        if current == stop:
            break
        current = current.parent


def restore_from_backup(paths: GamePaths, backup: Path, preserve_changes: bool = True) -> dict:
    manifest = read_json(backup / "backup_manifest.json")
    if not manifest:
        raise RuntimeError("Il backup selezionato non contiene un manifest valido.")
    original_global_exists = bool(manifest.get("original_global_exists"))
    original_cfg_exists = bool(manifest.get("original_user_cfg_exists"))
    state = load_installed_state()
    installed_cfg_hash = str(state.get("installed_user_cfg_sha256") or "")
    conflicts: list[str] = []

    if original_global_exists:
        original = backup / "original_global.ini"
        if not original.is_file():
            raise RuntimeError("Nel backup manca il global.ini originale.")
        if paths.target_global.is_file() and sha256_file(paths.target_global) != EXPECTED_PAYLOAD_SHA256:
            saved = copy_conflict(paths.target_global, backup, "global_modificato.ini")
            if saved:
                conflicts.append(str(saved))
        atomic_write_bytes(paths.target_global, original.read_bytes())
    elif paths.target_global.is_file():
        if sha256_file(paths.target_global) != EXPECTED_PAYLOAD_SHA256:
            saved = copy_conflict(paths.target_global, backup, "global_modificato.ini")
            if saved:
                conflicts.append(str(saved))
        paths.target_global.unlink()

    original_cfg = (backup / "original_user.cfg").read_bytes() if original_cfg_exists else None
    if paths.user_cfg.is_file():
        current = paths.user_cfg.read_bytes()
        unchanged = bool(installed_cfg_hash and sha256_bytes(current) == installed_cfg_hash)
        if preserve_changes and not unchanged:
            restored = restore_user_cfg_settings(current, original_cfg)
            if restored:
                atomic_write_bytes(paths.user_cfg, restored)
            else:
                paths.user_cfg.unlink()
        elif original_cfg_exists:
            atomic_write_bytes(paths.user_cfg, original_cfg or b"")
        else:
            paths.user_cfg.unlink()
    elif original_cfg_exists:
        atomic_write_bytes(paths.user_cfg, original_cfg or b"")

    remove_empty_translation_dirs(paths)
    clear_installed_state(paths.game_dir)
    return {"backup": str(backup), "conflicts_saved": conflicts}


def latest_backup_for_game(game_dir: Path) -> Path:
    root = USER_WORK_DIR / "backups"
    expected = os.path.normcase(str(game_dir.resolve()))
    if not root.is_dir():
        raise FileNotFoundError("Non esiste ancora alcun backup da ripristinare.")
    for backup in sorted((path for path in root.iterdir() if path.is_dir()), reverse=True):
        manifest = read_json(backup / "backup_manifest.json")
        recorded = str(manifest.get("game_dir") or "")
        if recorded and os.path.normcase(recorded) == expected:
            return backup
    raise FileNotFoundError("Non esiste un backup associato a questa installazione LIVE.")


def install_translation(
    game_dir: Path,
    *,
    force: bool = False,
    force_open: bool = False,
) -> dict:
    paths = resolve_paths(game_dir)
    if not looks_like_game_dir(paths.game_dir):
        raise FileNotFoundError("La cartella indicata non è una installazione LIVE valida.")
    running = process_running()
    if running and not force_open:
        raise RuntimeError(
            "Chiudi Star Citizen e RSI Launcher prima di installare. Processi aperti: "
            + ", ".join(running)
        )
    info = read_build_info(paths.game_dir)
    compatible, reason = compatibility_status(info)
    if not compatible and not force:
        raise RuntimeError(
            "Questa versione del gioco non è ancora verificata per la traduzione: " + reason
        )
    payload_path = source_payload_root() / TARGET_GLOBAL_REL
    payload = validate_payload(payload_path)
    backup = backup_live(paths, info)
    try:
        atomic_write_bytes(paths.target_global, payload_path.read_bytes())
        original_cfg = paths.user_cfg.read_bytes() if paths.user_cfg.is_file() else None
        installed_cfg = update_user_cfg(original_cfg)
        atomic_write_bytes(paths.user_cfg, installed_cfg)
        state = record_installed_state(paths, info, backup, installed_cfg)
        status = translation_status(paths)
        if not status["matches_current"]:
            raise RuntimeError("La verifica finale dell'installazione non è riuscita.")
    except Exception:
        restore_from_backup(paths, backup, preserve_changes=False)
        raise
    save_game_dir(paths.game_dir)
    return {
        "game_dir": str(paths.game_dir),
        "build": asdict(info),
        "compatibility": reason,
        "payload": payload,
        "backup": str(backup),
        "state": state,
        "status": status,
    }


def restore_translation(game_dir: Path, *, force_open: bool = False) -> dict:
    paths = resolve_paths(game_dir)
    running = process_running()
    if running and not force_open:
        raise RuntimeError(
            "Chiudi Star Citizen e RSI Launcher prima del ripristino. Processi aperti: "
            + ", ".join(running)
        )
    backup = latest_backup_for_game(paths.game_dir)
    return restore_from_backup(paths, backup, preserve_changes=True)


def check_latest_release(timeout: float = 4.0) -> dict:
    request = urllib.request.Request(
        GITHUB_API_LATEST,
        headers={"Accept": "application/vnd.github+json", "User-Agent": INSTALLER_FILENAME},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            release = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return {"available": None, "error": str(exc), "current": RELEASE_TAG}
    latest = str(release.get("tag_name") or "").strip()
    available = bool(latest and latest.casefold() != RELEASE_TAG.casefold())
    return {
        "available": available,
        "current": RELEASE_TAG,
        "latest": latest or None,
        "url": str(release.get("html_url") or GITHUB_RELEASES_URL),
    }


def acquire_installer_instance_lock() -> bool:
    global _INSTANCE_MUTEX
    if os.name != "nt":
        return True
    try:
        import ctypes

        handle = ctypes.windll.kernel32.CreateMutexW(None, False, "Sici29_StarCitizenItalianInstaller")
        if not handle:
            return True
        already_exists = ctypes.windll.kernel32.GetLastError() == 183
        _INSTANCE_MUTEX = handle
        return not already_exists
    except Exception:
        return True


def collect_startup_status() -> dict:
    result: dict[str, object] = {
        "game_dir": None,
        "path_source": None,
        "build": None,
        "compatible": None,
        "compatibility_reason": None,
        "translation": None,
    }
    try:
        game_dir, source = resolve_game_dir_with_source()
        paths = resolve_paths(game_dir)
        info = read_build_info(game_dir)
        compatible, reason = compatibility_status(info)
        result.update(
            {
                "game_dir": game_dir,
                "path_source": source,
                "build": info,
                "compatible": compatible,
                "compatibility_reason": reason,
                "translation": translation_status(paths),
            }
        )
    except (FileNotFoundError, RuntimeError, OSError, ValueError):
        pass
    return result


def print_status_panel(status: dict, colors: bool) -> None:
    game_dir = status.get("game_dir")
    compatible = status.get("compatible")
    translation = status.get("translation") or {}
    info = status.get("build")

    print(color_text(APP_TITLE, ConsoleColor.BOLD + ConsoleColor.CYAN, colors))
    print("=" * 64)
    if not game_dir:
        print(color_text("✗ GIOCO NON TROVATO", ConsoleColor.BOLD + ConsoleColor.RED, colors))
        print("Indica la cartella LIVE di Star Citizen per continuare.")
    elif compatible is not True:
        print(color_text("⚠ BUILD NON VERIFICATA", ConsoleColor.BOLD + ConsoleColor.YELLOW, colors))
        print(status.get("compatibility_reason") or "La build installata non è supportata.")
    elif translation.get("matches_current"):
        print(color_text("✓ TRADUZIONE AGGIORNATA", ConsoleColor.BOLD + ConsoleColor.GREEN, colors))
        print("La Revisione 1 coincide con i file installati.")
    elif translation.get("installed"):
        print(color_text("↑ TRADUZIONE DA AGGIORNARE", ConsoleColor.BOLD + ConsoleColor.YELLOW, colors))
        print("È presente una traduzione diversa: verrà salvata prima dell'aggiornamento.")
    else:
        print(color_text("✓ PRONTA PER L'INSTALLAZIONE", ConsoleColor.BOLD + ConsoleColor.GREEN, colors))
        print("La LIVE 4.9 è compatibile con questa revisione.")
    print()
    print("Gioco       :", game_dir or "non rilevato")
    if isinstance(info, BuildInfo):
        print("Build       :", f"{info.version} — change {info.requested_p4_change}")
    else:
        print("Build       :", "non rilevata")
    if translation.get("matches_current"):
        translation_label = "Revisione 1 installata"
    elif translation.get("installed"):
        translation_label = "altra versione rilevata"
    else:
        translation_label = "non installata"
    print("Traduzione  :", translation_label)
    print("Installer   :", TRANSLATION_VERSION)
    print("=" * 64)


def show_technical_status(status: dict) -> None:
    print("Dettagli tecnici")
    print("=" * 64)
    print("Cartella LIVE      :", status.get("game_dir") or "non rilevata")
    info = status.get("build")
    if isinstance(info, BuildInfo):
        print("Ramo                :", info.branch)
        print("Versione interna    :", info.version)
        print("Change              :", info.requested_p4_change)
        print("Data build          :", info.build_date, info.build_time)
    print("Build supportata    :", SUPPORTED_BRANCH, "change", SUPPORTED_P4_CHANGE)
    print("Righe italiane      :", EXPECTED_ENTRIES)
    print("SHA-256 payload     :", EXPECTED_PAYLOAD_SHA256)
    translation = status.get("translation") or {}
    print("Payload verificato  :", "sì" if translation.get("payload_matches") else "no")
    print("Testo italiano      :", "sì" if translation.get("language_configured") else "no")
    print("Audio inglese       :", "sì" if translation.get("english_audio_configured") else "no")
    print("=" * 64)


def show_credits() -> int:
    print(APP_TITLE)
    print("=" * 64)
    print("Progetto e traduzione : Sici29")
    print("GitHub                :", GITHUB_PROJECT_URL)
    print("Segnala un problema   :", GITHUB_ISSUES_URL)
    print("Sostieni il progetto  : metti una stella, condividi e segnala gli errori")
    print("=" * 64)
    answer = input("Vuoi aprire la pagina GitHub? [S/n]: ").strip().casefold()
    if answer in {"", "s", "si", "sì", "y", "yes"}:
        webbrowser.open(GITHUB_PROJECT_URL)
    return 0


def command_check(game_dir: str | None) -> int:
    resolved, _ = resolve_game_dir_with_source(game_dir)
    paths = resolve_paths(resolved)
    info = read_build_info(resolved)
    compatible, reason = compatibility_status(info)
    report = {
        "game_dir": str(resolved),
        "build": asdict(info),
        "compatible": compatible,
        "reason": reason,
        "translation": translation_status(paths),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if compatible else 2


def command_install(game_dir: str | None, force: bool, force_open: bool) -> int:
    resolved, _ = resolve_game_dir_with_source(game_dir)
    report = install_translation(resolved, force=force, force_open=force_open)
    print("Installazione completata e verificata.")
    print("Cartella LIVE :", report["game_dir"])
    print("Backup        :", report["backup"])
    print("Righe         :", report["payload"]["entries"])
    print("SHA-256       :", report["payload"]["sha256"])
    return 0


def command_restore(game_dir: str | None, force_open: bool) -> int:
    resolved, _ = resolve_game_dir_with_source(game_dir)
    report = restore_translation(resolved, force_open=force_open)
    print("Ripristino completato.")
    print("Backup usato  :", report["backup"])
    if report["conflicts_saved"]:
        print("Modifiche successive salvate prima del ripristino:")
        for path in report["conflicts_saved"]:
            print(" -", path)
    return 0


def run_menu() -> int:
    colors = enable_console_colors()
    status = collect_startup_status()
    print_status_panel(status, colors)
    if not status.get("game_dir"):
        print()
        answer = input("Vuoi selezionare adesso la cartella LIVE? [S/n]: ").strip().casefold()
        if answer in {"", "s", "si", "sì", "y", "yes"} and configure_game_dir():
            print()
            status = collect_startup_status()
            print_status_panel(status, colors)
    print()
    print("1. Installa o aggiorna la traduzione (consigliato)")
    print("2. Ripristina i file precedenti")
    print("3. Controlla se esiste una nuova versione")
    print("4. Indica o modifica la cartella LIVE")
    print("5. Crediti, GitHub e sostieni il progetto")
    print("6. Mostra i dettagli tecnici")
    print("0. Esci")
    print()
    choice = input("Scelta [Invio = installa]: ").strip() or "1"
    if choice == "0":
        return 0
    if choice == "2":
        return command_restore(None, False)
    if choice == "3":
        latest = check_latest_release()
        if latest.get("available") is True:
            print("Nuova versione disponibile:", latest.get("latest"))
            answer = input("Vuoi aprire la pagina delle release? [S/n]: ").strip().casefold()
            if answer in {"", "s", "si", "sì", "y", "yes"}:
                webbrowser.open(str(latest.get("url") or GITHUB_RELEASES_URL))
        elif latest.get("available") is False:
            print("Hai già la versione più recente.")
        else:
            print("Controllo online non disponibile. Riprova più tardi.")
        return 0
    if choice == "4":
        return run_menu() if configure_game_dir() else 1
    if choice == "5":
        return show_credits()
    if choice == "6":
        show_technical_status(status)
        return 0
    if choice != "1":
        print("Scelta non valida.")
        return 1
    return command_install(None, False, False)


def pause_if_needed(enabled: bool) -> None:
    if enabled and os.name == "nt":
        try:
            input("\nPremi Invio per chiudere...")
        except EOFError:
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Controlla compatibilità e installazione")
    check.add_argument("--game-dir")
    install = sub.add_parser("install", help="Installa o aggiorna la traduzione")
    install.add_argument("--game-dir")
    install.add_argument("--force", action="store_true", help="Ignora il controllo della build")
    install.add_argument("--force-open", action="store_true", help="Ignora i processi aperti")
    restore = sub.add_parser("restore", help="Ripristina l'ultimo backup")
    restore.add_argument("--game-dir")
    restore.add_argument("--force-open", action="store_true", help="Ignora i processi aperti")
    sub.add_parser("version", help="Mostra la versione dell'installer")
    return parser


def main() -> int:
    menu_mode = len(sys.argv) == 1
    if menu_mode:
        if not acquire_installer_instance_lock():
            print("L'installer è già aperto in un'altra finestra.")
            pause_if_needed(True)
            return 4
        try:
            code = run_menu()
        except Exception as exc:
            print("Errore:", exc)
            code = 1
        pause_if_needed(True)
        return code

    args = build_parser().parse_args()
    try:
        if args.command == "check":
            return command_check(args.game_dir)
        if args.command == "install":
            return command_install(args.game_dir, args.force, args.force_open)
        if args.command == "restore":
            return command_restore(args.game_dir, args.force_open)
        if args.command == "version":
            print(TRANSLATION_VERSION, RELEASE_TAG)
            return 0
    except Exception as exc:
        print("Errore:", exc)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

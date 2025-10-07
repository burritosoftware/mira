import os
import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Final

class BalconNotConfiguredError(RuntimeError):
    pass

class SynthesisError(RuntimeError):
    pass

def _balcon_path() -> Path:
    raw = os.getenv("BALCON_PATH", "").strip()
    if not raw:
        raise BalconNotConfiguredError(
            "BALCON_PATH is not set. Add it to your .env (see .env-example)."
        )
    p = Path(raw).expanduser()
    if not p.exists() or not p.is_file():
        raise BalconNotConfiguredError(f"BALCON_PATH is invalid or not a file: {p}")
    return p

async def synthesize(text: str, voice: str) -> bytes:
    """
    Auto: try SAPI5 via STDOUT (-o); on failure/empty output, fall back to SAPI4 temp WAV (-w).
    Returns WAV bytes either way.
    """
    balcon: Final[Path] = _balcon_path()

    # --- Attempt 1: SAPI5 path (STDOUT)
    cmd_stdout = [str(balcon), "-o", "-t", text, "-n", voice]
    try:
        res = await asyncio.to_thread(
            subprocess.run,
            cmd_stdout,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if res.stdout:  # success w/ SAPI5
            return res.stdout
        # If exit 0 but no bytes, treat as unsupported and fall back
    except subprocess.CalledProcessError as e:
        # Fall through to file method; keep stderr for context if that fails too
        stdout_attempt_err = e.stderr.decode(errors="ignore")[:400]
    else:
        stdout_attempt_err = ""  # no explicit error, just empty stdout

    # --- Attempt 2: SAPI4 path (file)
    tmp = tempfile.NamedTemporaryFile(prefix="balcon_", suffix=".wav", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()

    cmd_file = [str(balcon), "-w", str(tmp_path), "-t", text, "-n", voice]
    try:
        await asyncio.to_thread(subprocess.run, cmd_file, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = tmp_path.read_bytes()
        if not data:
            raise SynthesisError("Balcon (file mode) produced an empty WAV.")
        return data
    except subprocess.CalledProcessError as e:
        raise SynthesisError(
            "Balcon failed. STDOUT mode error:\n"
            f"{stdout_attempt_err}\n\n"
            "File mode error:\n"
            f"{e.stderr.decode(errors='ignore')[:400]}"
        ) from e
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

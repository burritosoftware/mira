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
    Synthesize `text` via Balcon using either SAPI4 or SAPI5 automatically.
    If STDOUT output is available (SAPI5), use it; otherwise fall back to temp WAV (SAPI4).

    Raises:
        BalconNotConfiguredError
        SynthesisError
    """
    balcon: Final[Path] = _balcon_path()

    tmp = tempfile.NamedTemporaryFile(prefix="balcon_", suffix=".wav", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()

    # Provide both -o and -w so SAPI5 uses STDOUT and SAPI4 uses file output.
    cmd = [
        str(balcon),
        "-o",  # STDOUT (ignored by SAPI4)
        "-w", str(tmp_path),
        "-t", text,
        "-n", voice,
    ]

    try:
        result = await asyncio.to_thread(
            subprocess.run,
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Prefer STDOUT if data present (SAPI5)
        if result.stdout:
            return result.stdout

        # Fallback to file output (SAPI4)
        if tmp_path.exists():
            data = tmp_path.read_bytes()
            return data

        raise SynthesisError("Balcon produced no output.")

    except subprocess.CalledProcessError as e:
        raise SynthesisError(f"Balcon failed with exit code {e.returncode}") from e
    except Exception as e:
        raise SynthesisError(f"Unexpected synthesis error: {e!r}") from e
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

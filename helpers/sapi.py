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
    Synthesize `text` via Balcon using `voice` at sample rate `fr`.
    Returns the WAV file as bytes. Temp file is deleted before returning.

    Raises:
        BalconNotConfiguredError
        SynthesisError
    """
    balcon: Final[Path] = _balcon_path()

    # Use a temp file on disk for Balcon output, then slurp bytes and delete.
    tmp = tempfile.NamedTemporaryFile(prefix="balcon_", suffix=".wav", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()  # we'll let Balcon write to it

    cmd = [
        str(balcon),
        "-w", str(tmp_path),
        "-t", text,
        "-n", voice,
    ]

    try:
        # Run the external process off the event loop
        await asyncio.to_thread(subprocess.run, cmd, check=True)
        data = tmp_path.read_bytes()
        return data
    except subprocess.CalledProcessError as e:
        raise SynthesisError(f"Balcon failed with exit code {e.returncode}") from e
    except Exception as e:
        raise SynthesisError(f"Unexpected synthesis error: {e!r}") from e
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            # Last-resort cleanup failure; don't mask upstream exceptions.
            pass

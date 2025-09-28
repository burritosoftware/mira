import time
from typing import Optional, Dict, Any
import httpx
from httpx_auth import AWS4Auth

IDENTITY_ID = "us-east-1:012d266b-ef9c-cc14-6950-f6132700e7d7"
REGION = "us-east-1"
SERVICE = "execute-api"

HOST = "moxu0s1jnk.execute-api.us-east-1.amazonaws.com"
PATH = "/prod-wpm/tts"
BASE_URL = f"https://{HOST}{PATH}"

_COG_URL = "https://cognito-identity.us-east-1.amazonaws.com/"
_COG_HEADERS = {
    "Content-Type": "application/x-amz-json-1.1",
    "X-Amz-Target": "AWSCognitoIdentityService.GetCredentialsForIdentity",
}

class _Creds:
    __slots__ = ("ak", "sk", "st", "exp_ts", "awsauth")
    def __init__(self, ak: str, sk: str, st: str, exp_ts: float):
        self.ak, self.sk, self.st, self.exp_ts = ak, sk, st, exp_ts
        # Let AWS4Auth manage the signed header set automatically.
        self.awsauth = AWS4Auth(ak, sk, REGION, SERVICE, security_token=st)

_creds: Optional[_Creds] = None
_SKEW = 60

async def _fetch_creds() -> _Creds:
    async with httpx.AsyncClient(timeout=20.0) as c:
        r = await c.post(_COG_URL, headers=_COG_HEADERS, json={"IdentityId": IDENTITY_ID})
        r.raise_for_status()
        j = r.json()
    c = j["Credentials"]
    exp = c.get("Expiration")
    exp_ts = float(exp) if isinstance(exp, (int, float)) else time.time() + 60*10
    return _Creds(c["AccessKeyId"], c["SecretKey"], c["SessionToken"], exp_ts)

async def _ensure_creds():
    global _creds
    if _creds is None or time.time() >= (_creds.exp_ts - _SKEW):
        _creds = await _fetch_creds()

async def synthesize(text: str, voice: str) -> bytes:
    await _ensure_creds()

    headers = {
        "Host": HOST,
        "Origin": "https://www.naturalreaders.com",
        "Referer": "https://www.naturalreaders.com/",
        "Content-Type": "application/json; charset=UTF-8",
        # Ensure the temp token is present as a header (it will also be signed)
        "X-Amz-Security-Token": _creds.st,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    }

    body = {"t": text}
    qs = {
      "e": "user@naturalreaders.com",
      "l": "0",
      "r": voice,
      "s": "0",
      "v": "aca",
      "vn": "10.6.13",
      "sm": "true",
      "ca": "false",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            BASE_URL,
            params=qs,
            json=body,
            headers=headers,
            auth=_creds.awsauth,
        )

        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code} — {resp.text[:500]}")

        ctype = resp.headers.get("content-type", "")
        if "audio" in ctype:
            return resp.content

        try:
            data: Dict[str, Any] = resp.json()
        except Exception:
            raise RuntimeError(f"Unexpected response {ctype}: {resp.text[:500]}")

        audio_url = data.get("url") or data.get("audioUrl") or data.get("mp3") or data.get("audio")
        if not audio_url:
            raise RuntimeError(f"No audio URL in response: {data}")

        r2 = await client.get(audio_url, timeout=30.0)
        r2.raise_for_status()
        return r2.content

import asyncio
import sys
sys.path.append("..")
from helpers.naturalreaders import synthesize

async def main():
    text = "The doors are closing. Please stand clear of the doors."
    mp3 = await synthesize(text)
    out_file = "out.mp3"
    with open(out_file, "wb") as f:
        f.write(mp3)
    print(f"Saved {out_file}")

if __name__ == "__main__":
    asyncio.run(main())

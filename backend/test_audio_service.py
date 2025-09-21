import asyncio
import io
import math
import wave

from fastapi import UploadFile

from app.services.audio import save_and_normalize


async def main() -> None:
    duration = 1.0
    sample_rate = 16000
    amplitude = 0.3

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(int(duration * sample_rate)):
            value = int(amplitude * 32767 * math.sin(2 * math.pi * 440 * (i / sample_rate)))
            frames += value.to_bytes(2, byteorder="little", signed=True)
        wf.writeframes(bytes(frames))

    buf.seek(0)

    upload = UploadFile(filename="tone.wav", file=io.BytesIO(buf.getvalue()))

    normalized = await save_and_normalize(upload)
    print("Normalized file written to", normalized)


if __name__ == "__main__":
    asyncio.run(main())

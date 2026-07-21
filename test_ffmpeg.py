import asyncio
from asyncio.subprocess import PIPE

async def test():
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-y", "-i", "pipe:0", "-f", "alaw", "-ar", "8000", "-ac", "1", "pipe:1",
        stdin=PIPE, stdout=PIPE, stderr=PIPE
    )
    
    proc.stdin.write(b"invalid data")
    await proc.stdin.drain()
    proc.stdin.close()
    # await proc.stdin.wait_closed()
    
    out = await proc.stdout.read()
    err = await proc.stderr.read()
    print("STDOUT:", len(out))
    print("STDERR:", err)

asyncio.run(test())

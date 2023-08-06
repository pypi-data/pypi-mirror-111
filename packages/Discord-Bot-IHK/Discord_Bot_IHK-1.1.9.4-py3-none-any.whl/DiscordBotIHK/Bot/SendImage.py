import io
import aiohttp
import discord

class ImageSender():
    async def sendFromURL(channel, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await channel.send(file=discord.File(data, 'cool_image.png'))



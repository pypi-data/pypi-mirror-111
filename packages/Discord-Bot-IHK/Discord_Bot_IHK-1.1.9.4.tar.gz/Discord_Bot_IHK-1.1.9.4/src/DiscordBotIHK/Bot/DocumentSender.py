import io
import aiohttp
import discord

class DocumentSender():
    async def sendFile(channel, name):
        await channel.send(file=discord.File(name))

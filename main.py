import asyncio
import os

import discord
from discord import Interaction
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class John(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix='v!',
            intents=intents,
            case_insensitive=True,
            activity=discord.Game(name="Valheim"),
            status=discord.Status.online
            )
        print(f"Created bot with prefix {self.command_prefix}.")

john = John()

async def main():

    @john.event
    async def on_ready():
        print(f'Logged into Discord as {john.user}.')

    @john.command(name="localsync", description="Sync all commands in the current guild.")
    async def localsync(ctx: commands.Context):
        john.tree.copy_global_to(guild=ctx.guild)
        await john.tree.sync(guild=ctx.guild)
        await ctx.reply("Commands synced locally!")

    @john.tree.command(name="test", description="Test if Viking John is working!")
    async def test(interaction: Interaction):
        await interaction.response.send_message("Yep, it works")

    print("Starting Viking John...")
    async with john:
        await john.start(DISCORD_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
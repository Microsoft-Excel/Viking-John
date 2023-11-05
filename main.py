import asyncio
import os
import random

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
        intents.voice_states = True
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

    @john.tree.command(name="pirate", description="That's got to be the worst pirate I've ever seen.")
    async def pirate(interaction: Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You must be in a voice channel to do this!")
            return
        
        voicelines = [
            "Setting sail!",
            "Please don't die to a sea serpent.",
            "That's a lot of iron you have there, would be a shame if there was a sea serpent around...",
            "Arr!",
            "I'm a viking, not a pirate!",
            "That's got to be the worst pirate I've ever seen."
        ]

        await interaction.response.send_message(voicelines[random.randint(0, len(voicelines) - 1)])
        channel = interaction.user.voice.channel
        vc = await channel.connect(reconnect=True, self_deaf=True)
        source = discord.FFmpegOpusAudio("assets/sound/pirateTheme.mp3")
        vc.play(source=source)

    print("Starting Viking John...")
    async with john:
        await john.start(DISCORD_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
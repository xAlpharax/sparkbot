#!/usr/bin/env python3

##########################################################################################

from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))

##########################################################################################

import discord

# from responses import get_response

class CustomClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        # if get_response(message.content):
            # await message.channel.send(get_response(message.content))

client = CustomClient()
tree = discord.app_commands.CommandTree(client)

##########################################################################################

@tree.command(name="test", description="Command used for testing")
async def test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}. I was made with Discord.py!", ephemeral = True)

##########################################################################################

client.run(DISCORD_TOKEN)

##########################################################################################

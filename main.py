#!/usr/bin/env python3

##########################################################################################

from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))

##########################################################################################

import discord

from responses import get_response

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
        if get_response(message.content):
            await message.channel.send(get_response(message.content))

client = CustomClient()
tree = discord.app_commands.CommandTree(client)

##########################################################################################

@tree.command(name="test", description="Command used for testing")
async def test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}. I was made with Discord.py!", ephemeral = True)

@tree.command(name="ping", description="pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"PONG {round(client.latency, 3)} ms", ephemeral = True)

from utils import get_vitals

@tree.command(name="stats", description="Check bot vital stats")
async def stats(interaction: discord.Interaction):
    await interaction.response.send_message(get_vitals(), ephemeral = True)

##########################################################################################

@tree.command(name="chat", description="Chat with Sparky")
async def chat(interaction: discord.Interaction, message: str):

    view = discord.ui.View()
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.danger, label="Cancel", custom_id="cancel"))
    # options for the ButtonStyle are: primary, secondary, success, danger, link

    if get_response(message):
        await interaction.response.send_message(get_response(message), ephemeral = True, view=view)
    else:
        ### LLM API LOGIC HERE ###
        return

##########################################################################################

client.run(DISCORD_TOKEN)

##########################################################################################

#!/usr/bin/env python3

##########################################################################################

from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))

##########################################################################################

import discord

from responses import get_response

# LLM AI API INTERACTION
from query import query
from upsert import upsert

class CustomClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        _ = upsert({})
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        ### check the category ID of the current channel ###
        if message.channel.category_id == 1244691546629214228 or message.channel.category_id in [1239120314340741152, 1239120397266321499, 1239120768563150880]:
            output = query({                # PRIV SERVER CATEGORY                                        # PUB SERVER
                "question": message.content,
            })

            output["text"] = output["text"][0:2000]

            await message.channel.send(output["text"])

        ### check the category ID of the current channel ###
        elif message.channel.id == 1244684281910132796 or message.channel.id == 1239122382304575508:
            output = query({    # PRIV SERVER CHANNEL                              # PUB SERVER
                "question": message.content,
            })

            output["text"] = output["text"][0:2000]

            await message.channel.send(output["text"])

        ### check if hardcoded guide message is better suited ###
        elif response := get_response(message.content):
            await message.channel.send(response)

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

    # view = discord.ui.View()
    # view.add_item(discord.ui.Button(style=discord.ButtonStyle.danger, label="Cancel", custom_id="cancel"))
    # options for the ButtonStyle are: primary, secondary, success, danger, link
    # buttons need to be added again

    await interaction.response.defer(thinking=True, ephemeral=True)

    ### LLM API LOGIC STARTS HERE ###

    output = query({
        "question": message,
    })

    output["text"] = output["text"][0:2000]

    ### LLM API LOGIC ENDS HERE ###

    await interaction.followup.send(output["text"])#, view=view)
    # output = query({"question" : message})["text"][0:2000]
    # await interaction.response.send_message(output, ephemeral = True)#, view=view)

@tree.command(name="sync", description="Sync/upsert the bot with the vector database")
async def sync(interaction: discord.Interaction):
    _ = upsert({})
    await interaction.response.send_message("Synced with the vector database!", ephemeral=True)

##########################################################################################

client.run(DISCORD_TOKEN)

##########################################################################################

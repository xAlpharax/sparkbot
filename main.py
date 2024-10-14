#!/usr/bin/env python3

##########################################################################################

from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))

##########################################################################################

import discord

from responses import get_response

# helper function to send long messages
async def send_long_message(channel, text):
    if len(text) > 2000:
        for i in range(0, len(text), 2000):
            await channel.send(text[i:i + 2000])
    else:
        await channel.send(text)

# LLM AI API INTERACTION
from query import query
from upsert import upsert

class CustomClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.user_sessions = {}  # This will hold user-specific conversation data
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

        user_id = message.author.id # Use this to identify users
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {"chat_id": user_id}  # Add user-specific memory

        # Use the user-specific chat_id in the query
        user_chat_id = self.user_sessions[user_id]["chat_id"]

        # Here you can remove the channel category checks if you want to allow DMs
        if isinstance(message.channel, discord.DMChannel):  # Check if it's a DM
            output = query({
                "question": message.content,
                "chatId": user_chat_id  # Use user chatId
            })
            await send_long_message(message.channel, output["text"])

        ### check the category ID of the current channel ###
        elif message.channel.category_id == 1244691546629214228 or message.channel.category_id in [1239120314340741152, 1239120397266321499, 1239120768563150880]:
            output = query({                # PRIV SERVER CATEGORY                                        # PUB SERVER
                "question": message.content,
                "chatId": user_chat_id  # Include chatId in query payload
            })

            await send_long_message(message.channel, output["text"])

        ### check the channel ID of the current channel ###
        elif message.channel.id == 1244684281910132796 or message.channel.id == 1239122382304575508:
            output = query({    # PRIV SERVER CHANNEL                              # PUB SERVER
                "question": message.content,
                "chatId": user_chat_id  # Include chatId in query payload
            })

            await send_long_message(message.channel, output["text"])

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
    user_id = interaction.user.id  # Get the user ID to track the user-specific session
    if user_id not in client.user_sessions:
        client.user_sessions[user_id] = {"chat_id": user_id}  # Create user-specific session if not already existing

    user_chat_id = client.user_sessions[user_id]["chat_id"]  # Get the user's chat ID

    await interaction.response.defer(thinking=True, ephemeral=True)  # Acknowledge the user's input

    ### LLM API LOGIC STARTS HERE ###
    output = query({
        "question": message,
        "chatId": user_chat_id  # Send chat_id along with the message for memory purposes
    })
    ### LLM API LOGIC ENDS HERE ###

    # Send long message using the helper function for splitting text over 2000 chars
    await send_long_message(interaction.followup, output["text"])

@tree.command(name="reset_chat", description="Reset your chat history with Sparky")
async def reset_chat(interaction: discord.Interaction):
    user_id = interaction.user.id  # Get the ID of the user issuing the command
    if user_id in client.user_sessions:
        del client.user_sessions[user_id]  # Delete the user's memory
        await interaction.response.send_message("Your chat history has been reset!", ephemeral=True)
    else:
        await interaction.response.send_message("You have no active chat history.", ephemeral=True)

@tree.command(name="sync", description="Sync/upsert the bot with the vector database")
async def sync(interaction: discord.Interaction):
    _ = upsert({})
    await interaction.response.send_message("Synced with the vector database!", ephemeral=True)

##########################################################################################

client.run(DISCORD_TOKEN)

##########################################################################################

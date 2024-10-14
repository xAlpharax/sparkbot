#!/usr/bin/env python3

##########################################################################################

from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))

##########################################################################################

import discord

# MESSAGING TWEAKS AND UTILS
from responses import get_response, send_long_message

# LLM AI API INTERACTION
from query import query
from upsert import upsert
from reset_memory import reset_memory

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
            output = await query({
                "question": message.content,
                "chatId": user_chat_id  # Use user chatId
            })
            await send_long_message(message.channel, output["text"])

        ### check the category ID of the current channel ###
        elif message.channel.category_id == 1244691546629214228 or message.channel.category_id in [1239120314340741152, 1239120397266321499, 1239120768563150880]:
            output = await query({                # PRIV SERVER CATEGORY                                        # PUB SERVER
                "question": message.content,
                "chatId": user_chat_id  # Include chatId in query payload
            })

            await send_long_message(message.channel, output["text"])

        ### check the channel ID of the current channel ###
        elif message.channel.id == 1244684281910132796 or message.channel.id == 1239122382304575508:
            output = await query({    # PRIV SERVER CHANNEL                              # PUB SERVER
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
    output = await query({
        "question": message,
        "chatId": user_chat_id  # Send chat_id along with the message for memory purposes
    })
    ### LLM API LOGIC ENDS HERE ###

    # Send long message using the helper function for splitting text over 2000 chars
    await send_long_message(interaction.followup, output["text"])

@tree.command(name="reset_all_memory", description="ADMIN UTIL: Reset all chat memory of Sparky")
async def reset_all_memory(interaction: discord.Interaction):

    if interaction.user.id == 313565570660564994:

        response = reset_memory()
        error = response.get("error")

        # Prepare the update message based on the success of the operation
        if error:
            print(f"Reset failed. Please check the error messages above. {error}")
            await interaction.response.send_message(error, ephemeral=True)
        else:  # If there was a success
            # del client.user_sessions  # Remove all user memory from the bot
            print("Reset successful:", response)
            await interaction.response.send_message(f"Your chat memory has been reset! {response}", ephemeral=True)

    else:
        await interaction.response.send_message("You do not have permission to do that")

@tree.command(name="update_docs", description="ADMIN UTIL: Update the vector database with new docs changes")
async def update_docs(interaction: discord.Interaction):

    if interaction.user.id == 313565570660564994:

        # Send an initial ephemeral response
        await interaction.response.send_message("Updating the vector database... Please wait.", ephemeral=True)

        # Perform the upsert operation
        success = upsert({})

        # Prepare the update message based on the success of the operation
        if success:
            update_message = "Successfully updated the vector database!"
        else:
            update_message = "Failed to update the vector database. Please try again later."

        # Send a follow-up ephemeral message with the update status
        # Editing the already sent message is harder, so we send a new one
        await interaction.followup.send(update_message, ephemeral=True)

    else:
        await interaction.response.send_message("You do not have permission to do that")

##########################################################################################

client.run(DISCORD_TOKEN)

##########################################################################################

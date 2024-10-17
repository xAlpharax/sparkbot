#!/usr/bin/env python3

##############################################################################

def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()

    if "hey sparky" in lowered or "hey sparkai" in lowered or "i need help" in lowered or "not working" in lowered:
        return 'Hey there! If you need help, simply open a ticket in https://discord.com/channels/449234259387875328/956661628957524009 and talk to me in natural language about the problems that you are encountering. Alternatively, you can use the `/chat` from anywhere in the server I am present. I will be happy to help you out!'
    else: return None

##############################################################################

async def send_long_message(channel, text, ephemeral=False, interaction=None):
    """
    Sends long messages in chunks, preserving code blocks, markdown, syntax highlighting, and prevents whitespace artifacts.

    Args:
        channel: The followup channel to send the message to.
        text: The content to send.
        ephemeral: A boolean flag to indicate if the message should be ephemeral (used only for interactions).
        interaction: The interaction object, if available, to send follow-up messages.
    """

    max_len = 2000  # Discord's character limit per message
    code_block_open = False  # Tracks whether we're inside a code block
    current_code_block_language = None  # Tracks the language for syntax highlighting

    def split_message(text):
        """Splits the message into chunks, preserving code blocks and markdown with syntax highlighting."""
        nonlocal code_block_open, current_code_block_language
        current_chunk = []
        current_length = 0

        for line in text.splitlines(keepends=True):  # Retain line breaks for markdown
            # Check for start/end of code blocks and identify the language for syntax highlighting
            if line.startswith('```'):
                if not code_block_open:
                    # Starting a new code block; capture the language if specified
                    code_block_open = True
                    current_code_block_language = line.strip()[3:].strip()  # Extract language
                    if current_length + len(line) > max_len:
                        # If this would exceed the limit, yield the current chunk first
                        yield ''.join(current_chunk).rstrip()  # Strip trailing whitespaces
                        current_chunk = []
                        current_length = 0
                else:
                    # Closing the code block
                    code_block_open = False
                    current_code_block_language = None

            # If adding this line exceeds the character limit
            if current_length + len(line) > max_len:
                # If we're inside a code block, close it temporarily before splitting
                if code_block_open:
                    current_chunk.append("```\n")
                    yield ''.join(current_chunk).rstrip()  # Yield the chunk with closed code block
                    current_chunk = []

                    # Reopen the code block in the next chunk with the correct language specifier
                    if current_code_block_language:
                        current_chunk.append(f"```{current_code_block_language}\n")
                        current_length = len(f"```{current_code_block_language}\n")
                    else:
                        current_chunk.append("```\n")
                        current_length = len("```\n")
                else:
                    yield ''.join(current_chunk).rstrip()  # Yield the chunk as is
                    current_chunk = []  # Start a new chunk
                    current_length = 0  # Reset chunk length

            # Add the line to the current chunk
            current_chunk.append(line)
            current_length += len(line)

        # Yield any remaining text in the current chunk
        if current_chunk:
            # If we're still inside a code block, close it properly
            if code_block_open:
                current_chunk.append("```\n")
            yield ''.join(current_chunk).rstrip()  # Yield the final chunk

    # Send the messages chunk by chunk
    first_message = True
    for chunk in split_message(text):
        if interaction is not None:  # Check if we have an interaction to send the message
            if first_message:
                await interaction.response.send_message(chunk, ephemeral=ephemeral)
                first_message = False
            else:
                await interaction.followup.send(chunk, ephemeral=ephemeral)
        else:  # Standard message send
            await channel.send(chunk)

##############################################################################

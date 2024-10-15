##############################################################################

def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()

    if "hey sparky" in lowered or "hey sparkai" in lowered or "i need help" in lowered or "not working" in lowered:
        return 'Hey there! If you need help, simply open a ticket in https://discord.com/channels/449234259387875328/956661628957524009 and talk to me in natural language about the problems that you are encountering. Alternatively, you can use the `/chat` from anywhere in the server I am present. I will be happy to help you out!'
    else: return None

##############################################################################

async def send_long_message(channel, text, ephemeral=False, interaction=None):
    """Sends long messages in chunks, preserving code blocks, markdown, and whitespace artifacts.

    Args:
        channel: The channel or interaction to send the message to.
        text: The content to send.
        ephemeral: A boolean flag to indicate if the message should be ephemeral.
        interaction: The interaction object (if any) used for sending ephemeral messages.
    """

    max_len = 2000
    code_block_open = False  # Tracks whether we're inside a code block

    def split_message(text):
        """Splits the message while preserving markdown and code blocks."""
        nonlocal code_block_open
        current_chunk = []
        current_length = 0

        for line in text.splitlines(keepends=True):
            # Detect start/end of code blocks
            if line.startswith('```'):
                code_block_open = not code_block_open

            # If the line would exceed the limit, yield the current chunk
            if current_length + len(line) > max_len:
                yield ''.join(current_chunk).rstrip()  # Remove trailing whitespaces
                current_chunk = []  # Start a new chunk
                current_length = 0  # Reset chunk length

            current_chunk.append(line)
            current_length += len(line)

        # Yield any remaining text in the current chunk
        if current_chunk:
            yield ''.join(current_chunk).rstrip()

    # Send the messages, handling both ephemeral and non-ephemeral cases
    first_message = True
    for chunk in split_message(text):
        if interaction and ephemeral:
            # For the first message, use interaction.response; for others, use followup
            if first_message:
                await interaction.response.send_message(chunk, ephemeral=True)
                first_message = False
            else:
                await interaction.followup.send(chunk, ephemeral=True)
        else:
            # Non-ephemeral messages or regular messages sent through a channel
            await channel.send(chunk)

        if code_block_open:
            # Add a blank line between chunks if inside a code block, to avoid breaking syntax
            await channel.send("```")

##############################################################################

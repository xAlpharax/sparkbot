##############################################################################

def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()

    if "hey sparky" in lowered or "hey sparkai" in lowered or "i need help" in lowered or "not working" in lowered:
        return 'Hey there! If you need help, simply open a ticket in https://discord.com/channels/449234259387875328/956661628957524009 and talk to me in natural language about the problems that you are encountering. Alternatively, you can use the `/chat` from anywhere in the server I am present. I will be happy to help you out!'
    else: return None

# async def send_long_message(channel, text):
    # if len(text) > 2000:
        # for i in range(0, len(text), 2000):
            # await channel.send(text[i:i + 2000])
    # else:
        # await channel.send(text)

async def send_long_message(channel, text):
    """Sends long messages in chunks, preserving code blocks, markdown, and whitespace artifacts."""

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
                if code_block_open:
                    code_block_open = False
                else:
                    code_block_open = True

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

    # Go through the chunks and send them as separate messages
    for chunk in split_message(text):
        await channel.send(chunk)
        if code_block_open:
            # Add a blank line between chunks if inside a code block, to avoid breaking syntax
            await channel.send("```")

##############################################################################

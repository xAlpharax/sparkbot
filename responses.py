##############################################################################

def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()

    if "hey sparky" in lowered or "hey sparkai" in lowered or "i need help" in lowered or "not working" in lowered:
        return 'Hey there! If you need help, simply open a ticket in https://discord.com/channels/449234259387875328/956661628957524009 and talk to me in natural language about the problems that you are encountering. Alternatively, you can use the `/chat` from anywhere in the server I am present. I will be happy to help you out!'
    else: return None

##############################################################################

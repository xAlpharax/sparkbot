def get_response(user_input: str):
    lowered: str = user_input.lower()

    if "hey sparky" in lowered or "sparky!" in lowered or "hey sparkai" in lowered:
        return 'Hey there! To get started, type `/chat` to see what I can do for you!'
    # else:
        # return 'Sorry, I am not sure what you are asking for. Please type `/chat` to see what I can do for you!'
    else: return None

conversation_history = {}


def add_message(chat_id, message):
    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    conversation_history[chat_id].append(message)


def get_history(chat_id):
    return conversation_history.get(chat_id, [])


def clear_history(chat_id):
    conversation_history.pop(chat_id, None)
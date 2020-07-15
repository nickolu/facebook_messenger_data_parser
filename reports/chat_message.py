class ChatMessage(object):
    def __init__(self, sender_name, timestamp_ms, message_content):
        self.sender_name = sender_name
        self.timestamp_ms = timestamp_ms
        self.message_content = message_content

    @classmethod
    def create_new_from_hangouts_data(hangouts_message):
        sender_name = hangouts_message[]
        timestamp_ms = hangouts_message[]
        message_content = hangouts_message[]
        
        return ChatMessage(sender_name, timestamp_ms, message_content)

    @classmethod
    def create_new_from_facebook_data(facebook_message):
        sender_name = facebook_message[]
        timestamp_ms = facebook_message[]
        message_content = facebook_message[]
        
        return ChatMessage(sender_name, timestamp_ms, message_content)
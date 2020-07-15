from .base_report import BaseReport
import json


class ChatReport(BaseReport):
    def iterate_hangouts_data(self):
        print("creating new manchat_messages.json...")
        f = open("chat_data/hangouts/manchat_messages.json", "w")
        f.write("[")
        f.close()
        print("loading hangouts json data...")
        data = json.load(open("chat_data/hangouts/Hangouts.json", "r"))
        conversations = data["conversations"]
        manchat_conversation_data = conversations[-1]["conversation"]["conversation"]
        manchat_participant_data = manchat_conversation_data["participant_data"]
        manchat_conversation_events = conversations[-1]["events"]
        user_hash = {}
        attachment_types = []
        longest_segment = []
        chat_message_count = 0
        text_message_count = 0
        attachment_count = 0
        other_attachment_count = 0
        longest_attachment_length = 0

        print("building user hash...")
        for user in manchat_participant_data:
            user_hash[user["id"]["chat_id"]] = user["fallback_name"]

        count = 0

        print("iterating events...")
        for event in manchat_conversation_events:

            user_id = event["sender_id"]["chat_id"]
            user_name = user_hash[user_id]
            timestamp_ms = event["timestamp"]
            message_content = {}

            if event.get("chat_message") is not None:
                chat_message_count += 1
                message_content = event["chat_message"]["message_content"]

            content = ""

            if message_content.get("segment") is not None:
                text_message_count += 1
                segment_text = ""

                for text in message_content.get("segment"):
                    if text.get("text") is not None:
                        segment_text += text.get("text")

                content = segment_text

            if message_content.get("attachment") is not None:
                attachment_count += 1
                attachment = message_content["attachment"][0]["embed_item"]

                if attachment.get("plus_photo") is not None:
                    if (
                        attachment.get("plus_photo").get("original_content_url")
                        is not None
                    ):
                        content += attachment.get("plus_photo").get(
                            "original_content_url"
                        )

            # for key in message_content:
            #     print(key, message_content[key])

            write_message_to_json_file(user_name, timestamp_ms, content)

        # for key in manchat_conversation_events[0]:
        #     print(key)

        print("add closing bracket to manchat_messages.json...")
        f = open("chat_data/hangouts/manchat_messages.json", "a")
        f.write("]")
        f.close()

        print(longest_attachment_length)


def write_message_to_json_file(sender_name, timestamp_ms, content):
    message = {
        "sender_name": sender_name,
        "timestamp_ms": timestamp_ms,
        "content": content,
    }
    f = open("chat_data/hangouts/manchat_messages.json", "a")
    f.write(json.dumps(message) + ",")
    f.close()


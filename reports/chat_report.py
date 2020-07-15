from .base_report import BaseReport
from nltk.tokenize import word_tokenize
import json
import re
import os

facebook_messages_path = "chat_data/facebook/manchat"
hangouts_messages_path = "chat_data/hangouts"


MAX_ITERATIONS = 100
TOTAL_ITERATIONS = 0

user_map = {"Nick Cunningham": "Nickolus Cunningham"}
common_words = [
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "I",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "they",
    "we",
    "say",
    "her",
    "she",
    "or",
    "an",
    "will",
    "my",
    "one",
    "all",
    "would",
    "there",
    "their",
    "what",
    "so",
    "up",
    "out",
    "if",
    "about",
    "who",
    "get",
    "which",
    "go",
    "me",
    "when",
    "make",
    "can",
    "like",
    "time",
    "no",
    "just",
    "him",
    "know",
    "take",
    "people",
    "into",
    "year",
    "your",
    "good",
    "some",
    "could",
    "them",
    "see",
    "other",
    "than",
    "then",
    "now",
    "look",
    "only",
    "come",
    "its",
    "over",
    "think",
    "also",
    "back",
    "after",
    "use",
    "two",
    "how",
    "our",
    "work",
    "first",
    "well",
    "way",
    "even",
    "new",
    "want",
    "because",
    "any",
    "these",
    "give",
    "day",
    "most",
    "us",
    "lol",
    "haha",
]


class ChatReport(BaseReport):
    def run(
        self, reports_to_build=[], reports_to_run=[], additional_logs=[],
    ):
        def build_reports(data):
            total_iterations = TOTAL_ITERATIONS
            messages = data.get("messages")
            if messages is not None:
                for message in messages:
                    # if total_iterations >= MAX_ITERATIONS:
                    #     break
                    total_iterations += 1
                    for build_report in reports_to_build:
                        build_report(message)

                    for additional_log in additional_logs:
                        additional_log(message)
            else:
                print('cant find key "messages" in data')
                print(type(data))

        iterate_message_files_in_directory(facebook_messages_path, build_reports)
        iterate_message_files_in_directory(hangouts_messages_path, build_reports)

        for report in reports_to_run:
            report()

    def get_user_data(self, message):
        sender_name = map_user(message["sender_name"])

        if self.user_data.get(sender_name) is None:
            self.user_data[sender_name] = {}

        user_data = self.user_data[sender_name]

        return user_data

    def build_users_list(self, message):
        self.senders.append(map_user(message["sender_name"]))

    def build_messages_per_user(self, message):
        sender_name = map_user(message["sender_name"])

        if self.user_data.get(sender_name) is None:
            self.user_data[sender_name] = {}

        user_data = self.user_data[sender_name]

        if user_data.get("message_count") is None:
            user_data["message_count"] = 1
        else:
            user_data["message_count"] += 1

    def build_words_per_user(self, message):
        sender_name = map_user(message["sender_name"])

        if self.user_data.get(sender_name) is None:
            self.user_data[sender_name] = {}

        user_data = self.user_data[sender_name]

        if message.get("content") is not None:
            words = []
            for word in re.findall(r"\w+", message["content"]):
                words.append(word)

            if user_data.get("word_count") is None:
                user_data["word_count"] = len(words)
            else:
                user_data["word_count"] += len(words)

    def build_unique_words_per_user(self, message):
        sender_name = map_user(message["sender_name"])

        if self.user_data.get(sender_name) is None:
            self.user_data[sender_name] = {}

        user_data = self.user_data[sender_name]

        if message.get("content") is not None:
            words = set(word_tokenize(message["content"]))
            if user_data.get("unique_words") is None:

                user_data["unique_words"] = words
            else:
                for word in words:
                    if word not in common_words:
                        user_data["unique_words"].add(word)

    def build_specific_word_count_for_user(self, message, word_to_count):
        user_data = self.get_user_data(message)

        if message.get("content") is not None:
            # words = set(word_tokenize(message["content"]))

            if user_data.get("specific_word_counts") is None:
                user_data["specific_word_counts"] = {}

            if user_data.get("specific_word_counts").get(word_to_count) is None:
                user_data["specific_word_counts"][word_to_count] = 0

            matches = re.findall(
                r"{}".format(word_to_count.lower()), message["content"].lower()
            )

            user_data["specific_word_counts"][word_to_count] += len(matches)

    def report_print_unique_users(self):
        print(set(self.senders))

    def report_messages_per_user(self):
        print(self.chats_per_user)

    def report_specific_word_count_for_users(self, word):
        items_to_print = []

        def sort_func(item):
            return item[1]

        for user in self.user_data:
            user_data = self.user_data[user]
            word_count = user_data.get("specific_word_counts").get(word)
            total_words = user_data.get("word_count")
            word_count_vs_total_words = None
            if total_words is not None:
                word_count_vs_total_words = round((word_count / total_words) * 100, 3)

            items_to_print.append([user, word_count, word_count_vs_total_words])

        items_to_print.sort(key=sort_func, reverse=True)

        print("counts for the word: {}".format(word))
        total = 0
        for item in items_to_print:
            if item[1] > 0:
                total += item[1]
                print("{}: {} ({}%)".format(item[0], item[1], item[2]))
        
        print('total: {}'.format(total))


def map_user(user_name):
    if user_map.get(user_name) is not None:
        return user_map.get(user_name)

    return user_name


def iterate_message_files_in_directory(directory_path, action):
    for entry in os.scandir(directory_path):
        if entry.path.endswith(".json"):
            data = json.load(open(entry.path))
            print("getting data at ", entry.path)
            action(data)

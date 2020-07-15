import calendar
import mailbox
import datetime

BREAK_AFTER = 1000000
RESULTS_FILE_NAME = "results.csv"
LOG_ITERATIONS = True
LOG_ITERATIONS_AT = 5000
WEEKDAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


class BaseReport(object):
    def __init__(self, reports_to_build=[], additional_logs=[], reports_to_run=[]):
        self.user_data = {}
        self.unique_users = []
        self.oldest_message = None
        self.date_counts = {}
        self.without_payload = 0
        self.chats_per_user = {"total": 0}
        self.words_per_user = {"total": 0}
        self.chars_per_user = {"total": 0}
        self.weekday_counts = {}
        self.senders = []

        for day in WEEKDAYS:
            self.weekday_counts[day] = 0

        self.set_up_csvs_to_write()

    def set_up_csvs_to_write(self):
        f = open("report_output/chats_per_user.csv", "w")
        f.close()
        f = open("report_output/words_per_user.csv", "w")
        f.close()
        f = open("report_output/chars_per_user.csv", "w")
        f.close()
        f = open("report_output/user_data.csv", "w")
        f.close()

    def write_chats_per_user_to_csv(self, file_name="report_output/chats_per_user.csv"):
        f = open(file_name, "a")
        for user in self.chats_per_user.items():
            f.write("{}, {},\n".format(user[0], user[1]))
        f.close()

    def write_words_per_user_to_csv(self, file_name="report_output/words_per_user.csv"):
        f = open(file_name, "a")
        for user in self.words_per_user.items():
            f.write("{}, {},\n".format(user[0], user[1]))
        f.close()

    def write_chars_per_user_to_csv(
        self, file_name="report_output/characters_per_user.csv"
    ):
        f = open(file_name, "a")
        for user in self.chars_per_user.items():
            f.write("{}, {},\n".format(user[0], user[1]))
        f.close()

    def write_user_data_to_csv(self, file_name="report_output/user_data.csv"):
        f = open(file_name, "a")
        for user in self.user_data:
            f.write(
                "{}, {}, {}, {}\n".format(
                    user,
                    self.user_data[user].get("message_count"),
                    self.user_data[user].get("word_count"),
                    len(self.user_data[user].get("unique_words")),
                )
            )
        f.close()

    def print_unique_users(self):
        users = []
        for user in self.chats_per_user:
            users.append(user)

        print(set(users))

    def print_chats_per_user(self):
        print("without_payload=", self.without_payload)
        print("messages=", self.chats_per_user)
        print("words=", self.words_per_user)
        print("characters=", self.chars_per_user)

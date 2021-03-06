import calendar
import mailbox
import datetime
from .base_report import BaseReport

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


class GmailMboxReport(BaseReport):
    def __init__(self, mbox_file_path):
        self.mailbox = mailbox.mbox(mbox_file_path)

    def run(self, reports_to_build=[], additional_logs=[], reports_to_run=[]):
        for key in self.mailbox.iterkeys():
            if key > BREAK_AFTER:
                break

            if key % LOG_ITERATIONS_AT == 0 and LOG_ITERATIONS:
                print("parsed {} messages".format(key), end="\r")

            message = self.mailbox[key]

            for build_report in reports_to_build:
                build_report(message)

            for run_log in additional_logs:
                run_log(message)

        for run_report in reports_to_run:
            run_report()

    def build_chats_per_day(self, message):
        date = get_mbox_message_date(message)

        if date is not None:
            date_str = date.__format__("%D")

            if self.date_counts.get(date_str) is None:
                self.date_counts[date_str] = 1
            else:
                self.date_counts[date_str] += 1

    def build_oldest_message(self, message):
        date = message.get_from()

        if date is not None:

            if self.oldest_message == None:
                oldest_message = date

            if date < self.oldest_message:
                oldest_message = date

    def build_chats_per_user(self, message):
        user = str(message.get("from"))

        if self.chats_per_user.get(user) is None:
            self.chats_per_user[user] = 1
        else:
            self.chats_per_user[user] += 1

        self.chats_per_user["total"] += 1

    def build_chars_per_user(self, message):
        user = str(message.get("from"))
        payload = message.get_payload()
        if type(payload) == list:
            self.without_payload += 1
            payload = ""

        chars = len(payload)

        if self.chars_per_user.get(user) is None:
            self.chars_per_user[user] = chars
        else:
            self.chars_per_user[user] += chars

        self.chars_per_user["total"] += chars

    def build_words_per_user(self, message):
        user = str(message.get("from"))
        payload = message.get_payload()
        if type(payload) == list:
            self.without_payload += 1
            payload = ""

        word_count = len(payload.split(" "))

        if self.words_per_user.get(user) is None:
            self.words_per_user[user] = word_count
        else:
            self.words_per_user[user] += word_count

        self.words_per_user["total"] += word_count

    def build_weekday_counts(self, message):
        date = get_mbox_message_date(message)

        if date is not None:
            day_number = date.weekday()
            weekday = calendar.day_name[day_number]

            self.weekday_counts[weekday] += 1


def get_mbox_message_date(mbox_message):
    date_list = mbox_message.get_from().split(" ")[1::]

    date_string = " ".join(date_list)
    date_object = datetime.datetime.strptime(
        date_string.replace("\r", ""), "%a %b %d %H:%M:%S %z %Y"
    )
    return date_object


def get_user_first_name_from_message(mbox_message):
    user = mbox_message.get("from")
    try:
        user_first_name = user.split(" ")[0]
    except Exception:
        user_first_name = "unknown"

    return user_first_name


def get_user_email_from_message(mbox_message):
    try:
        user = mbox_message.get("from")
        user_email_parts = user.split("@")
        email_handle_parts = user_email_parts[0].split(" ")
        email_domain_parts = user_email_parts[1].split(" ")
        email_handle = email_handle_parts[len(email_handle_parts) - 1]
        email_domain = email_domain_parts[0]

        email_from = "{}@{}".format(email_handle, email_domain)
    except:
        email_from = "not found"

    return email_from

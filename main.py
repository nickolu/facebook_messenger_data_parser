import time

from reports.gmail_mbox_report import GmailMboxReport
from reports.chat_report import ChatReport
from reports.simplify_hangouts_json_data import simplify_hangouts_json_data

START_TIME = time.time()


def log_sender(message):
    print(message["sender_name"])


report = ChatReport()

word_to_report = "d&d"


def count_word(message):
    report.build_specific_word_count_for_user(message, word_to_report)


def report_word_count():
    return report.report_specific_word_count_for_users(word_to_report)


report.run(
    reports_to_build=[count_word, report.build_words_per_user],
    reports_to_run=[report_word_count],
    additional_logs=[],
)

# simplify_hangouts_json_data()

# report = GmailMboxReport("./mailboxes/Chat.mbox")

# report.run(
#     additional_logs=[],
#     reports_to_build=[report.build_chats_per_user,],
#     reports_to_run=[report.print_unique_users,],
# )


print("took {} seconds".format(time.time() - START_TIME))

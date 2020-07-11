import time

from gmail_mbox_report import GmailMboxReport

START_TIME = time.time()

report = GmailMboxReport("./mailboxes/Chat.mbox")

report.run(
    additional_logs=[],
    reports_to_build=[
        report.build_chats_per_user,
        report.build_words_per_user,
        report.build_chars_per_user,
    ],
    reports_to_run=[
        report.write_chats_per_user_to_csv,
        report.write_words_per_user_to_csv,
        report.write_chars_per_user_to_csv,
    ],
)


print("took {} seconds".format(time.time() - START_TIME))

import time

from reports.gmail_mbox_report import GmailMboxReport
from reports.chat_report import ChatReport

START_TIME = time.time()

report = ChatReport()

report.iterate_hangouts_data()

# report = GmailMboxReport("./mailboxes/Chat.mbox")

# report.run(
#     additional_logs=[],
#     reports_to_build=[report.build_chats_per_user,],
#     reports_to_run=[report.print_unique_users,],
# )


print("took {} seconds".format(time.time() - START_TIME))

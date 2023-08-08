from datetime import datetime, timedelta

# from app import mail

last_day = datetime.utcnow() - timedelta(minutes=1)

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     hello_there(
#         2,
#         hello_there.s("adg"),
#         name="hello w"
#     )
#     sender.add_periodic_task(
#         5,
#         send_reminders.s(),
#         name='send_reminders every day at midnight'
#     )
#

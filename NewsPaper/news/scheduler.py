from apscheduler.schedulers.background import BackgroundScheduler


news_scheduler = BackgroundScheduler()
news_scheduler.add_job(
    id='send_mails',
    func=lambda: print('123'),
    trigger='interval',
    seconds=5,
)
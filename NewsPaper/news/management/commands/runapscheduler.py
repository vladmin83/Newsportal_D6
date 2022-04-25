import logging
from news.models import New, Category, CategoryToUser
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.sites.shortcuts import get_current_site


logger = logging.getLogger(__name__)

def my_job():
    #  Your job processing logic here...
    print('работает периодическая задача ')
    pull_new = {}  # словарь с выборкой необходимых к рассылке новостей - ключ - категория новости
    a = New.objects.filter(dateCreation__range=[datetime.now() - timedelta(days=7), datetime.now()])
    print(a)
    link = ''.join(['http://', get_current_site(None).domain, ':8000/news'])

    for b in a:  # итерация New
        cat = b.newCategory
        #print(cat)
        subject = f'{b.newCategory}, {b.title}'
        massage = f'{b.newCategory}, {b.title}, читать далее {link}/{b.id}'

        for s in CategoryToUser.objects.all():
            mail = s.subscribers.email
            #print(mail)
            if mail:
                #print(mail)
                send_mail(
                    subject=subject,
                    message=massage,
                    from_email='Vladbelov87@yandex.ru',
                    recipient_list=[mail],
                )
            else:
                print(f'На новые статьи в категории {mail} нет подписки')



            # userlist.append(mail)
            # print(userlist)

        # pull_new = pull_new(b)
        # print(pull_new)


        # for cat in pull_new.keys():
        #     print(cat)
        #     # mail_adres = Category.objects.get(id=cat)
        #     # print(mail_adres)
        #     if cat.subscribers.all():
        #         posts = ''
        #         for post in pull_new[cat]:
        #             posts = f'{posts}* Новость -->> {link}/{b.id}\n'
        #             print(posts)
        # формирование и рассылка писем
        # if mail_adres.subscribers.all():
        #     send_mail(
        #         subject=f'Пулл новых статей в категории ->> {mail_adres}',
        #         message=news,
        #         from_email='Vladbelov87@yandex.ru',
        #         recipient_list=[ml.email for ml in mail_adres.subscribers.all()],
        #     )
        # else:
        #     print(f'На новые статьи в категории {mail_adres} нет подписки')

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")






# # наша задача по выводу текста на экран
# def my_job():
#     #  Your job processing logic here...
#     print('hello from job')
#
#
# # функция, которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         # добавляем работу нашему задачнику
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(second="*/10"),
#             # То же, что и интервал, но задача тригера таким образом более понятна django
#             id="my_job",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from news.models import New, CategoryToUser, Author, Category
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site


@receiver(post_save, sender=New)
def notify_post_create(sender, instance, created, **kwargs):
    if created:
        print('свежие новости')
        print('***************Рассылка*******************')
        subject = f'{instance.title} {instance.newCategory} {instance.dateCreation.strftime("%d %m %Y")}'
        userlist = []
        link = ''.join(['http://', get_current_site(None).domain, ':8000/news'])
        message = f'Перейдите {link}/{instance.id}  чтобы прочесть статью.'
        for s in CategoryToUser.objects.all():
            mail = s.subscribers.email
            print(mail)
            userlist.append(mail)
            print(userlist)

            send_mail(
                subject=subject,
                message=message,
                from_email='Vladbelov87@yandex.ru',
                recipient_list=[userlist],
            )
    else:
        print('Новостей нет')
    print('***************Рассылка*******************')

post_save.connect(notify_post_create, sender=New)










        # for id_cat in id_new_cat.all().values('category'):
        #     id_cat
        #     print(id_cat)
        # mail_adres = Category.objects.get(id=id_cat['category'])
        # print(mail_adres.subscribers.all())
        # if mail_adres.subscribers.all():
        #     print('Подписки есть')
        #     for mail in mail_adres.subscribers.all():
        #         send_mail(
        #             subject=f'Свежие новости в категории ->> {mail}',
        #             message=f'Пройдите по ссылке ->> http://127.0.0.1:8000/newsall/{id_new}',
        #             from_email='vladikmin83@yandex.ru',
        #             recipient_list=[mail],
        #         )
        # else:
        #     print('Новостей нет')
        # print('***************Рассылка*******************')





# @receiver(post_save, sender=New)
# def send_subscribe(instance, newCategory, **kwargs):
#     # Если категория для подписчиков существует, вытаскиваю списки и делаю рассылку
#     try:
#         category_group = Group.objects.get(name=newCategory)
#         print(f'{instance.id} {instance.newCategory} {instance.dateCreation.strftime("%d %m %Y")}')
#         list_mail = list(User.objects.filter(groups=category_group).values_list('email', flat=True))
#         for user_email in list_mail:
#             username = list(User.objects.filter(email=user_email).values_list('username', flat=True))[0]
#             html_content = render_to_string('subscribe_new_post.html', {'new': instance, 'username': username, 'category': category})
#             msg = EmailMultiAlternatives(
#                 subject=f'News Portal: {category}',
#                 body='',
#                 from_email='vladikmin83@yandex.ru',
#                 to=[user_email, ],
#             )
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#     # Если категории нет (никто еще не подисывался на эту категорию)
#     except Group.DoesNotExist:
#         pass
from django.shortcuts import render, reverse, redirect
from .models import New, Category, CategoryToUser
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.core.paginator import Paginator
from .filters import NewFilter
from .forms import NewForm, UserForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import Form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import datetime
from django.dispatch import receiver
from django.core.mail import mail_managers
from django.db.models.signals import post_save, m2m_changed
from django.contrib.sites.shortcuts import get_current_site



class News(ListView):
    model = New
    context_object_name = 'news'
    template_name = 'news/posts.html'
    ordering = ['-dateCreation']
    author = 'authors'
    paginate_by = 10

    def get_filter(self):
        return NewFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class NewDetailView(DetailView):
    template_name = 'news/detail.html'
    queryset = New.objects.all()


class NewCreateView(CreateView):
    template_name = 'news/create.html'
    form_class = NewForm


class NewUpdateView(UpdateView):
    template_name = 'news/create.html'
    form_class = NewForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return New.objects.get(pk=id)


class NewDeleteView(DeleteView):
    template_name = 'news/delete.html'
    queryset = New.objects.all()
    success_url = '/news/'


class MyView(PermissionRequiredMixin, View):
    permission_required = ('news.view_New')


class AddNew(PermissionRequiredMixin, CreateView):
    permission_required = ('news.view_New', 'news.add_New', 'news.change_New', 'news.delete_New')


class CategoryList(ListView):
    model = Category
    template_name = 'news/abonent_category.html'
    context_object_name = 'abonent_category'

    #def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['is_not_subscribers'] = Category.objects.filter(subscriber=subscriber, user=user)
    #     # context['is_subscribers'] = Category.objects.filter(subscriber=user, user=subscriber)
    #     context['user_subscribers'] = Category.objects.all()
    #     return context

    def post(self, request, *args, **kwargs):
        id_category = request.POST.getlist("Подписка")
        print(f'категория- {id_category} ')
        mass_cat = ''
        for id_cat in id_category:
            a = Category.objects.get(id=id_cat)
            a.subscribers.add(request.user)
            mass_cat = mass_cat + f'{a}; '

        send_mail(
            subject=f'{request.user.username} Вы подписаны на новости в категории {mass_cat}',
            message=f'{request.user.username} Вы подписаны на новости в категории {mass_cat}',
            from_email="Vladbelov87@yandex.ru",
            recipient_list=[request.user.email],
        )
        return redirect('/news/')





# def my_job():
#     #  Your job processing logic here...
#     print('работает периодическая задача ')
#     pull_post = {}  # словарь с выборкой необходимых к рассылке новостей - ключ - категория новости
#     a = New.objects.filter(dateCreation__range=[datetime.now() - timedelta(days=7), datetime.now()])
#     for b in a:  # итерация New
#         for pc in b.newcategory_set.all():  # итерация транзитной категории NewCategory
#             # print(pc.get_id_cat(),pc.get_id_post())
#             # достаем с помощью функций модели newCategory id category и id post
#             pull_new[pc.get_id_cat()] = pull_new.get(pc.get_id_cat(), []) + [pc.get_id_new()]
#             # формируем словарь category/new
#     print(pull_new)
#     # рассылка писем
#     for cat in pull_new.keys():
#         mail_adres = Category.objects.get(id=cat)
#         if mail_adres.abonent.all():
#             news = ''
#             for new in pull_new[cat]:
#                 news = f'{news}* Новость -->> http://127.0.0.1:8000/newsall/{new}\n'
#             # print(news)
#         # формирование и рассылка писем
#         if mail_adres.abonent.all():
#             send_mail(
#                 subject=f'Пулл новых статей в категории ->> {mail_adres}',
#                 message=news,
#                 from_email='vladikmin83@yandex.ru',
#                 recipient_list=[ml.email for ml in mail_adres.abonent.all()],
#             )
#         else:
#             print(f'На новые статьи в категории {mail_adres} нет подписки')

# @login_required
# def add_subscribe(request, pk):
#     user = request.user
#     category_object = Category.objects.get(pk=pk)
#     category_object.subscribers.add(user)
#     return redirect('news/')
#
#
# @login_required
# def unsubscribe(request, pk):
#     user = request.user
#     category_object = Category.objects.get(pk=pk)
#     category_object.subscribers.remove(user)
#     return redirect('news/')
#
#
# class NewView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'make_new.html', {})
#
#     def post(self, request, *args, **kwargs):
#         new = New(
#             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
#             client_name=request.POST['client_name'],
#             message=request.POST['message'],
#         )
#         new.save()
#
#         # получаем наш html
#         html_content = render_to_string(
#             'new_created.html',
#             {
#                 'new': new,
#             }
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=f'{new.client_name} {new.date.strftime("%Y-%M-%d")}',
#             body=new.message,  # это то же, что и message
#             from_email='vladikmin83@yandex.ru',
#             to=['vladikmin@gmail.com'],  # это то же, что и recipients_list
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#         msg.send()  # отсылаем
#
#         return redirect('news:make_new')


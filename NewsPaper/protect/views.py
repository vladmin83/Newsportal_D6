from django.shortcuts import render
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class MyView(PermissionRequiredMixin, View):
    permission_required = ('news.view_New')


class AddNew(PermissionRequiredMixin, CreateView):
    permission_required = ('news.view_New', 'news.add_New', 'news.change_New', 'news.delete_New')
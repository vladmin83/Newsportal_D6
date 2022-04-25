from django.urls import path
from .views import *


urlpatterns = [
    path('', News.as_view(), name='news'),
    path('<int:pk>/', NewDetailView.as_view(), name='detail'),
    path('create/', NewCreateView.as_view(), name='create'),
    path('create/<int:pk>', NewUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', NewDeleteView.as_view(), name='delete'),
    path('newsall/', CategoryList.as_view(), name='abonent_category'),
]




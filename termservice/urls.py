from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('docs/', views.docs, name='docs'),
    path('dir/', views.DirectoryListView.as_view()),
    path('items/', views.ItemDirListView.as_view()),
    path('valid/', views.ValidatingItemDirListView.as_view()),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('docs/', views.docs, name='docs'),
    path('directory/', views.DirectoryListView.as_view()),
    path('item-dir/', views.ItemDirListView.as_view()),
    path('item-dir-valid/', views.ValidatingItemDirListView.as_view()),
]

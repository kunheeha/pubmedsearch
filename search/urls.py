from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),
    path('search/', views.search, name='search'),
    path('demosearch/<int:search_id>/', views.demo_search, name='demo-search'),
    path('demoarticle/<int:article_id>/', views.demo_article, name='demo-article'),
    path('delete_article/<int:article_id>/<int:search_id>/', views.delete_article, name='delete-article'),
    path('delete_search/<int:search_id>/', views.delete_search, name='delete-search'),
]

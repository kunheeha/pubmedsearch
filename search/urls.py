from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),
    path('search/', views.search, name='search'),
    path('demosearch/<int:search_id>/', views.demo_search, name='demo-search'),
    path('usersearch/<int:search_id>/', views.user_search, name='user-search'),
    path('demoarticle/<int:article_id>/', views.demo_article, name='demo-article'),
    path('userarticle/<int:article_id>/', views.user_article, name='user-article'),
    path('delete_article/<int:article_id>/<int:search_id>/', views.delete_article, name='delete-article'),
    path('delete_search/<int:search_id>/', views.delete_search, name='delete-search'),
    path('delete_userarticle/<int:article_id>/<int:search_id>/', views.delete_user_article, name='delete-user-article'),
    path('delete_usersearch/<int:search_id>/', views.delete_user_search, name='delete-user-search'),
]

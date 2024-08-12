from django.urls import path
from book import views

urlpatterns = [
    path('', views.login_page, name="login"),
    path('add_books/', views.add_book, name='add_book'),
    path('delete-book/<id>/', views.delete_book, name='delete_book'),
    path('update-book/<id>/', views.update_book, name='update_book'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_page, name="logout_page"),
]

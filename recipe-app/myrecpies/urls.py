from django.urls import path
from myrecpies.views import*

urlpatterns = [
    path('',home, name='home'),
    path('addrecipe/',add_recipe, name = 'add_recipe'),
    path('search/',search, name = 'search'),
    path('login_page/',login_page, name = 'login_page'),
    path('register/',register, name = 'register'),
    path('create_profile/',create_profile, name = 'create_profile'),
    path('update_profile/<id>/',update_profile, name = 'update_profile'),
    path('log_out/',log_out,name = 'log_out'),
    path('profile/<id>/',profile,name = 'profile'),
    path('recipe_detail/<id>/',recipe_detail,name = 'recipe_detail'),
    path('delete_recipe/<id>/',delete_recipe,name="delete_recipe"),
    path('update_recipe/<id>/',update_recipe,name="update_recipe"),
    path('viewrecipe/',viewrecipe,name="viewrecipe"),
  
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('delete_account/', delete_account, name='delete_account'),
]

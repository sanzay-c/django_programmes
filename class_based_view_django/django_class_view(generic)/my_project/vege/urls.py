from django.urls import path
from vege.views import (  # imported the views that were creatd in views.py
    HomepageView,
    ReceipesView,
    UpdateReceipeView,
    DeleteReceipeView,
    LoginPageView,
    RegisterPageView,
    LogoutPageView,
)

# name='url_name' => name is used to refer to the URL in templates or other parts of the code.
# path takes parameter like: path('url-routes', views-for-that-route, name='name-of-the-url(toutes)')
# here, in class based view we use 'view_name.as_view()'
urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("receipe/", ReceipesView.as_view(), name="receipes"),
    path("update-receipe/<pk>/", UpdateReceipeView.as_view(), name="update_receipe"),
    path("delete-receipe/<pk>/", DeleteReceipeView.as_view(), name="delete_receipe"),
    path("login/", LoginPageView.as_view(), name="login_page"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("logout/", LogoutPageView.as_view(), name="logout_page"),
]

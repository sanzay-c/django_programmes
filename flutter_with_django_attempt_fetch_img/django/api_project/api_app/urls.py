# from django.urls import path
# from .views import PersonsDetailsView

# urlpatterns = [
#     path('information/', PersonsDetailsView.as_view(), name='person_details'),
# ]

# myapp/urls.py

from django.urls import path
from .views import PersonDetailList, PersonDetailView

urlpatterns = [
    path('persons/', PersonDetailList.as_view(), name='person-detail-list'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),  
]



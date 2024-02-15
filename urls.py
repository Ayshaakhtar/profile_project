from django.urls import path
from.views import Home
from.views import all_prof, delete_prof, update


urlpatterns = [
    path('Home/', Home, name="Home"),
    path('all_prof/', all_prof, name="all_prof"),
    path('delete_prof/<int:id>/', delete_prof, name="delete_prof"),
    path('update/<int:id>/', update, name="update"),
]

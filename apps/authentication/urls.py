from django.urls import path

from .views import RegistrationEndpoint

urlpatterns = [
    path('auth/registration/', view=RegistrationEndpoint.as_view()),
]

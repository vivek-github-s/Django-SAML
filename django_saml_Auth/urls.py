# urls.py

from django.urls import path
from . import views  # Import your SAML views

urlpatterns = [
    path('login/', views.saml_login, name='saml_login'),
    path('callback/', views.saml_callback, name='saml_callback'),
]

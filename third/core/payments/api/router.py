from django.urls import path, include
from .views import (
    register_view,
    login_view,
    payments_view,
    change_password
)


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('payments/', payments_view, name='payments'),
    path('change-password/', change_password, name='change_password'),
]

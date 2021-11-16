from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
from .views import PasswordsChangeView

urlpatterns = [
    path('registration/', views.registration, name='user_registration'),
    path('login/', views.user_login, name='login'),
    # path('user_settings/', views.user_settings_view, name='user_settings'),
    path('change_your_password/',PasswordsChangeView.as_view(), name='change_your_password'),


    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
from django.urls import path

from account.views import account_views, profile_views


app_name = 'account'

urlpatterns = [
    path('login/', account_views.LoginView.as_view(), name='login'),
    path('logout/', account_views.LogoutView.as_view(), name='logout'),

    path('profile/change-password/',
         profile_views.PasswordUpdateView.as_view(),
         name='change-password'),
]

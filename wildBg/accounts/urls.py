from django.contrib.auth.views import LogoutView
from django.urls import path, include

from wildBg.accounts import views

urlpatterns = [
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailView.as_view(), name='profile-details'),
    ])),
]
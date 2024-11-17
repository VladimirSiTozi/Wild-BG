from django.contrib.auth.views import LogoutView
from django.urls import path, include

from wildBg.accounts import views

urlpatterns = [
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailView.as_view(), name='profile-details'),

    ])),
]
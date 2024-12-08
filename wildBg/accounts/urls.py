from django.contrib.auth.views import LogoutView
from django.urls import path, include

from wildBg.accounts import views

urlpatterns = [
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailView.as_view(), name='profile-details'),
        path('delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
        path('edit/', views.ProfileEditView.as_view(), name='profile-edit'),
    ])),
]
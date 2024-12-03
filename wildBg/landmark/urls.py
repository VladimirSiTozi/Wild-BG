from django.urls import path, include

from wildBg.landmark import views

urlpatterns = [
    path('add/', views.LandmarkAddView.as_view(), name='add-landmark'),
    path('<int:pk>/', include([
        path('', views.LandmarkDetailsView.as_view(), name='details-landmark'),
        path('add_review/', views.add_review, name='add_review'),
        path('like/', views.like_func, name='like-landmark'),
    ])),
]

from django.urls import path, include

from wildBg.post import views

urlpatterns = [
    path('<int:pk>/', include([
        path('', views.PostDetailView.as_view(), name='[post-detail'),
    ])),
]

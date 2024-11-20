from django.urls import path, include

from wildBg.landmark import views

urlpatterns = [
    path('add/', views.LandmarkAddView.as_view(), name='add-landmark'),
    path('<int:pk>/', include([
        path('', views.LandmarkDetailsView.as_view(), name='details-landmark'),
        path('add_review/', views.add_review, name='add_review'),
    ])),
]

    #     # path('edit/', views.EditPhotoPageView.as_view(), name='edit-photo'),
    #     # path('delete/', views.delete_photo, name='delete-photo')


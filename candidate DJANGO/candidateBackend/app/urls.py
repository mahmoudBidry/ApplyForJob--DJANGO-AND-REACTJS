from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="apiOverview"),
    path('candidate-list/', views.candidate_list, name="create-list"),
    path('candidate-create/', views.create_candidate, name="create-candidate"),
    path('candidate-detail/<int:pk>/', views.candidate_detail, name="candidate-detail"),
    path('candidate-update/<int:pk>/', views.update_candidate, name="update-candidate"),
    path('candidate-delete/<int:pk>/', views.delete_candidate, name="delete-candidate"),
]
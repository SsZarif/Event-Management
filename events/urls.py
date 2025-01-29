# urls.py

from django.urls import path
from . import views
from .views import homepage, organizer_dashboard

urlpatterns = [
    path('', homepage, name='homepage'),
    path('organizer_dashboard/', organizer_dashboard, name='organizer_dashboard'),
    
    path('event/create/', views.create_event, name='create_event'),
    path('event/list/', views.event_list, name='event_list'),
    path('event/update/<int:pk>/', views.update_event, name='update_event'),
    path('event/delete/<int:pk>/', views.delete_event, name='delete_event'),
    
    path('participant/create/', views.create_participant, name='create_participant'),
    path('participant/list/', views.participant_list, name='participant_list'),
    path('participant/update/<int:pk>/', views.update_participant, name='update_participant'),
    path('participant/delete/<int:pk>/', views.delete_participant, name='delete_participant'),
    
    path('category/create/', views.create_category, name='create_category'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/update/<int:pk>/', views.update_category, name='update_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
]

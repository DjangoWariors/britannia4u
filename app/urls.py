from django.urls import path, include

from . import views

urlpatterns = [


    path('region-master/', views.regionMaster, name='region-master'),
    path('add-region/', views.addRegion, name='add-region'),
    path('update-region/<str:pk>/', views.updateRegion, name='update-region'),

    path('delete-region/<str:pk>/', views.deleteRegion, name='delete-region'),

    path('britania-points/', views.britaniaPoints, name='britania-points'),

]
from django.urls import path
import front.views

urlpatterns = [
    path('', front.views.index),
    path('read/<int:id>/', front.views.read), 
    path('create/', front.views.create), 
    path('update/<int:id>/', front.views.update), 
    path('delete/<int:id>/', front.views.delete), 
]


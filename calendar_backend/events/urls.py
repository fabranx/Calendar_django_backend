from django.contrib import admin
from django.urls import path, include
from .views import EventListView, EventDetailView, EventPost

urlpatterns = [
    path('', EventPost.as_view(), name="EventPost"),
    path('<username>', EventListView.as_view(), name="EventListView"),
    path('<username>/<int:pk>/', EventDetailView.as_view(), name="EventDetailView")
]

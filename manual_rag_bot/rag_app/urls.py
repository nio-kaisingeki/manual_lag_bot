from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("chat/", views.chat, name="chat"),
    path("pdf_upload/", views.pdf_upload_view, name="pdf_upload"),
]
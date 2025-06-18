from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("chat/", views.chat, name="chat"),
    path("pdf_upload/", views.pdf_upload_view, name="pdf_upload"),
    path("documents/", views.DocumentListView.as_view(), name="document_list"),
    path(
        "documents/<int:pk>/delete/",
        views.DocumentDeleteView.as_view(),
        name="document_delete",
    ),
    path("signup/", views.signup, name="signup"),
]
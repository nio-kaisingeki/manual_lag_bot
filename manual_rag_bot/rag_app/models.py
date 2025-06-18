from django.db import models
from django.contrib.auth import get_user_model


class Document(models.Model):
    """Model to store uploaded document text for retrieval."""

    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="documents"
    )

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.title


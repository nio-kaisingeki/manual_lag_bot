from django.db import models


class Document(models.Model):
    """Model to store uploaded document text for retrieval."""

    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.title


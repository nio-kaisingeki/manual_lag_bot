from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Document


class DocumentModelTests(TestCase):
    def test_document_str(self):
        user = get_user_model().objects.create(username="u")
        doc = Document.objects.create(title="t", text="x", user=user)
        self.assertEqual(str(doc), "t")

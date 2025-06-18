from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PDFUploadForm
from .models import Document
from .services import chroma_service, openai_service
import fitz  # PyMuPDF

chat_history = []

@login_required
def home(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        chat_history.append({"sender": "user", "text": user_input})

        context_docs = chroma_service.query(request.user.id, user_input)
        context_text = "\n".join(context_docs)
        answer = openai_service.ask_with_context(user_input, context_text)

        chat_history.append({"sender": "bot", "text": answer})

    return render(request, "rag_app/home.html", {"messages": chat_history})


@login_required
def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        context_docs = chroma_service.query(request.user.id, user_input)
        context_text = "\n".join(context_docs)
        answer = openai_service.ask_with_context(user_input, context_text)
        return JsonResponse({"response": answer})

    return render(request, "rag_app/chat.html")


@login_required
def pdf_upload_view(request):
    text = ""
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["file"]
            # PDFからテキストを抽出
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
            document = Document.objects.create(
                title=pdf_file.name, text=text, user=request.user
            )
            chroma_service.add_document(request.user.id, str(document.id), text)
            return render(request, "rag_app/upload_success.html", {"text": text})
    else:
        form = PDFUploadForm()
    return render(request, "rag_app/pdf_upload.html", {"form": form})


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = "rag_app/document_list.html"

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    success_url = reverse_lazy("document_list")
    template_name = "rag_app/document_confirm_delete.html"

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

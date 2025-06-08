from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import PDFUploadForm
from .models import Document
from .services import chroma_service, openai_service
import fitz  # PyMuPDF

chat_history = []

def home(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        chat_history.append({"sender": "user", "text": user_input})

        context_docs = chroma_service.query(user_input)
        context_text = "\n".join(context_docs)
        answer = openai_service.ask_with_context(user_input, context_text)

        chat_history.append({"sender": "bot", "text": answer})

    return render(request, "rag_app/home.html", {"messages": chat_history})


def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        context_docs = chroma_service.query(user_input)
        context_text = "\n".join(context_docs)
        answer = openai_service.ask_with_context(user_input, context_text)
        return JsonResponse({"response": answer})

    return render(request, "rag_app/chat.html")


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
            document = Document.objects.create(title=pdf_file.name, text=text)
            chroma_service.add_document(str(document.id), text)
            return render(request, "rag_app/upload_success.html", {"text": text})
    else:
        form = PDFUploadForm()
    return render(request, "rag_app/pdf_upload.html", {"form": form})

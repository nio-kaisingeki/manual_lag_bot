from django.shortcuts import render
from django.http import HttpResponse
from .forms import PDFUploadForm
import fitz  # PyMuPDF

chat_history = []

def home(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        chat_history.append({"sender": "user", "text": user_input})
        chat_history.append({"sender": "bot", "text": "これはダミーの応答です。"})

    return render(request, "rag_app/home.html", {"messages": chat_history})


def chat(request):
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
            # ここでtextを次のステップに渡せるように保存などする
            return render(request, "rag_app/upload_success.html", {"text": text})
    else:
        form = PDFUploadForm()
    return render(request, "rag_app/pdf_upload.html", {"form": form})

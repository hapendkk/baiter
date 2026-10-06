import base64
import os
import tempfile

from django.shortcuts import render
from .ml.text_model import generate_headlines
from .ml.audio_model import transcribe_audio
from .ml.image_model import generate_image_description
from .ml.video_model import generate_video_description


def to_data_uri(uploaded_file):
#превращение в дата uri чтобы на старнице показать
    uploaded_file.seek(0)
    data = base64.b64encode(uploaded_file.read()).decode("ascii")
    mime = uploaded_file.content_type or "application/octet-stream"
    uploaded_file.seek(0)
    return f"data:{mime};base64,{data}"


def save_to_temp(uploaded_file):
    #временно сохраняет файл и возвращает путь
    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        return temp_file.name


def home(request):
    return render(request, 'baiter_app/home.html')


def text_page(request):
    headlines = []

    if request.method == "POST":
        keywords = request.POST.get("keywords", "")

        if keywords:
            headlines = generate_headlines(keywords)

    return render(
        request,
        "baiter_app/text.html",
        {"headlines": headlines}
    )


def audio_page(request):
    text = ""
    headlines = []
    media_url = ""

    if request.method == "POST":
        audio_file = request.FILES.get("audio")

        if audio_file:
            media_url = to_data_uri(audio_file)
            file_path = save_to_temp(audio_file)

            try:
                text = transcribe_audio(file_path)

                if text:
                    headlines = generate_headlines(text)

            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

    return render(
        request,
        "baiter_app/audio.html",
        {
            "text": text,
            "headlines": headlines,
            "media_url": media_url,
        }
    )


def image_page(request):
    description = ""
    headlines = []
    media_url = ""

    if request.method == "POST":
        image_file = request.FILES.get("image")

        if image_file:
            media_url = to_data_uri(image_file)
            file_path = save_to_temp(image_file)

            try:
                description = generate_image_description(file_path)

                if description:
                    headlines = generate_headlines(description)

            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

    return render(
        request,
        "baiter_app/image.html",
        {
            "description": description,
            "headlines": headlines,
            "media_url": media_url,
        }
    )


def video_page(request):
    description = ""
    headlines = []
    media_url = ""

    if request.method == "POST":
        video_file = request.FILES.get("video")

        if video_file:
            media_url = to_data_uri(video_file)
            file_path = save_to_temp(video_file)

            try:
                description = generate_video_description(file_path)

                if description:
                    headlines = generate_headlines(description)

            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

    return render(
        request,
        "baiter_app/video.html",
        {
            "description": description,
            "headlines": headlines,
            "media_url": media_url,
        }
    )

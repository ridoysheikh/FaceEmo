from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64, io, tempfile
from deepface import DeepFace



# Mapping emotions to emojis
def all_emoji(emotion):
    basic_emotions = {
        "happy": "😀",
        "sad":   "😢",
        "angry": "😠",
        "fear":  "😟",
        "disgust": "🤢",
        "surprise": "😲",
        "neutral": "😐"
    }
    return basic_emotions.get(emotion)

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def getReact(request):
    try:
        if request.POST.get("image"):
            img = request.POST.get("image")
            img = img.replace("data:image/jpeg;base64,", "")
            img = base64.b64decode(img)

            tem_dir = tempfile.TemporaryDirectory()
            image_path = f"{tem_dir.name}/image.jpg"

            with open(image_path, "wb") as fh:
                fh.write(img)

            

            objs = DeepFace.analyze(img_path = image_path, actions = ['emotion'])
            emotion=objs[0]['dominant_emotion']
            
            emoji=all_emoji(emotion)

            print(emoji)

            return JsonResponse({"emotion": emotion, "emoji": emoji}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)
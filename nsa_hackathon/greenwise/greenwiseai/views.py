from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from .models import AudioRecording

genai.configure(api_key="YourAPI-Key")

def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def recorder(request):
    recordings = AudioRecording.objects.all().order_by('-created_at')
    return render(request, 'recorder.html', {'recordings': recordings})


@csrf_exempt
def save(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)
        print("POST:", request.POST)
        title = request.POST.get('title', 'New Recording')
        audio_file = request.FILES.get('audio_file') 
        
        if audio_file:
            recording = AudioRecording.objects.create(
                title=title,
                audio_file=audio_file
            )
            return JsonResponse({'success': True, 'id': recording.id})
    
    return JsonResponse({'success': False})



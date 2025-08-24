from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from .models import AudioRecording
from django.core.files.base import ContentFile
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import translate_v2 as translate 

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
        title = request.POST.get('title', 'New Recording')
        uploaded_file = request.FILES.get('audio_file')
        
        if uploaded_file:
            # convert uploaded webm to mp3
            audio = AudioSegment.from_file(uploaded_file, format="webm")
            mp3_io = ContentFile(b"")
            audio.export(mp3_io, format="mp3")
            mp3_io.seek(0)
            
            # save to model
            recording = AudioRecording.objects.create(
                title=title,
                audio_file=ContentFile(mp3_io.read(), name='recording.mp3')
            )

            # Get transcript
            transcript = speech_to_text(recording)

            # Translate Nepali -> English
            translation = translate_np_to_eng(transcript)

            return JsonResponse({
                'success': True,
                'id': recording.id,
                'transcript': transcript,
                'translation': translation
            })

    return JsonResponse({'success': False, 'error': 'Invalid method'})

def speech_to_text(recording):
    client = speech.SpeechClient()
    with open(recording.audio_file.path, 'rb') as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # match saved MP3
        sample_rate_hertz=48000,
        language_code="ne-NP"  # Nepali
    )

    try:
        response = client.recognize(config=config, audio=audio)
        transcript = ' '.join(result.alternatives[0].transcript for result in response.results)
    except Exception as e:
        print("Google Speech API error:", e)
        transcript = ''

    return transcript

def translate_np_to_eng(transcript):
    if not transcript:
        return ''

    try:
        translate_client = translate.Client()
        translation = translate_client.translate(transcript, target_language='en')
        return translation['translatedText']
    except Exception as e:
        print("Google Translate API error:", e)
        return ''






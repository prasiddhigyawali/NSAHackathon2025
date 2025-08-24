from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.template import loader
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from .models import AudioRecording
from django.core.files.base import ContentFile
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import translate_v2 as translate 
from openai import OpenAI
import json
import re

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

            ret_json = prompt_engineering(translation)

            return JsonResponse({
                'success': True,
                'id': recording.id,
                'transcript': transcript,
                'translation': translation,
                'data': ret_json,
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


def prompt_engineering(translation):

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"USERINPUT: {translation} SYSTEM: You are **Krisi Sahayak** — an expert agronomist and practical field advisor for smallholder farmers in Nepal. Primary goal: give **concise, safe, actionable farming advice now tailored for the farmer based on the information given in [USERINPUT], do not ask any further questions**. Secondary goal: when natural, collect **very small** helpful metadata (but do NOT block advice). RULES (copy exactly): 1) LANGUAGE & TONE - Use very simple words, short sentences (6th-grade level). Respectful, expert, calm. 2) OUTPUT ORDER & LIMITS (required) Generate realistic farming data for [CROP TYPE] on [FARM SIZE] acres. Make all numbers realistic for [LOCATION/CLIMATE] and [SEASON/MONTH]. Provide specific numerical values in this exact format and do not add any other info or data give the data formatted in json: **PLANTING DATA:** - Seeds per acre: [X number] - Planting depth: [X millimeters] - Row spacing: [X millimeters] **WATER:** - Weekly irrigation: [X millimeters] **WEATHER:** - Rainfall this month: [X millimeters] - Average temperature: [X°C] **PROJECTED HARVEST:** - Expected yield: [X bushels/tons per acre] - Expected revenue per acre: [NPR X]",
        store=True,
    )

    json_data = parse_json_response(response.output_text)
    print(json_data)

    return json_data

def parse_json_response(response_text):
    # Remove markdown code blocks
    cleaned_text = re.sub(r'```json\s*|\s*```', '', response_text.strip())
    
    try:
        json_data = json.loads(cleaned_text)
        return json_data
    except json.JSONDecodeError as e:
        return None


# views.py - Simplified version that works without APIs
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import AudioRecording, FarmerQuery
import json
import time
from datetime import datetime

def home(request):
    """Main chat interface with placeholder data"""
    context = {
        'user_location': 'काठमाडौं, नेपाल',
        'weather_data': get_placeholder_weather(),
        'news_items': get_placeholder_news(),
    }
    # Using your existing index.html template
    return render(request, 'index.html', context)

def about(request):
    """About page"""
    return render(request, 'about.html')

@csrf_exempt
def process_message(request):
    """Process farmer messages - works without external APIs"""
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                message_type = data.get('type', 'text')
                user_message = data.get('message', '')
                language = data.get('language', 'ne')
            else:
                message_type = request.POST.get('type', 'text')
                user_message = request.POST.get('message', '')
                language = request.POST.get('language', 'ne')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Simulate processing time
            start_time = time.time()
            
            # Generate simple AI response (no external API needed)
            ai_response = generate_simple_farming_response(user_message, language)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Save to database
            try:
                query = FarmerQuery.objects.create(
                    question=user_message,
                    answer=ai_response,
                    location='काठमाडौं, नेपाल',
                    language=language,
                    query_type=message_type,
                    ip_address=get_client_ip(request),
                    weather_condition='सामान्य',
                    season=get_current_season(),
                    response_time=response_time
                )
            except Exception as e:
                print(f"Error saving query: {e}")
            
            return JsonResponse({
                'success': True,
                'response': ai_response,
                'user_message': user_message if message_type == 'voice' else None
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def generate_simple_farming_response(user_message, language='ne'):
    """Generate farming responses using simple keyword matching in both languages"""
    message_lower = user_message.lower()
    
    # Define responses in both languages
    responses_ne = {
        'rice': """धान बारे सुझाव:
        • रोपाइं: जेष्ठ-असारमा नर्सरी तयार गर्नुहोस्
        • पानी: नियमित पानी दिनुहोस्
        • मल: यूरिया र डीएपी प्रयोग गर्नुहोस्
        
        समस्या भए नजिकैको कृषि कार्यालयमा सम्पर्क गर्नुहोस्।""",
        
        'corn': """मकै खेतीका लागि:
        • बीजारोपण: चैत-बैशाखमा रोप्नुहोस्
        • दूरी: 75cm x 25cm राख्नुहोस्
        • मल: कम्पोस्ट + रासायनिक मल
        
        पहेंलो भए फलामयुक्त मल दिनुहोस्।""",
        
        'vegetable': """तरकारी खेतीका लागि:
        • मौसम अनुसार बीउ छान्नुहोस्
        • जैविक मल प्रयोग गर्नुहोस्
        • नियमित पानी र निकाई गर्नुहोस्
        
        बजार भाउ हेरेर बेच्नुहोस्।""",
        
        'potato': """आलु खेतीका लागि:
        • रोपाइं: कार्तिक-मंसिरमा
        • बीउ: प्रमाणित बीउ प्रयोग गर्नुहोस्
        • माटो: खुकुलो र निकास भएको
        
        दाग लागे कपर सल्फेट छर्कनुहोस्।""",
        
        'yellow': """बाली पहेंलो भएमा:
        • कारण: नाइट्रोजनको कमी हुन सक्छ
        • समाधान: यूरिया मल दिनुहोस्
        • पानी: पानीको कमी नहोस्
        
        २ हप्तामा सुधार नभए विशेषज्ञसँग सम्पर्क गर्नुहोस्।""",
        
        'pest': """किरा नियन्त्रणका लागि:
        • जैविक विधि: नीमको तेल प्रयोग गर्नुहोस्
        • रासायनिक: कृषि पसलमा सल्लाह लिनुहोस्
        • रोकथाम: सफा खेती गर्नुहोस्
        
        छर्कदा सुरक्षा उपकरण लगाउनुहोस्।""",
        
        'weather': """मौसम अनुसार खेती:
        • वर्षा: धान र मकै राम्रो
        • जाडो: गहुँ र तरकारी
        • गर्मी: सिंचाईको व्यवस्था गर्नुहोस्
        
        मौसम पूर्वानुमान हेरेर काम गर्नुहोस्।""",
        
        'fertilizer': """मल प्रयोगका लागि:
        • जैविक: कम्पोस्ट र गोबर खाद
        • रासायनिक: यूरिया, डीएपी, पोटास
        • समय: रोपाइं र फूल आउँदा दिनुहोस्
        
        धेरै नदिनुहोस्, माटो बिग्रिन्छ।""",
        
        'market': """बजार जानकारी:
        • भाउ: दैनिक बजार भाउ हेर्नुहोस्
        • बेच्ने समय: बिहान जल्दै बेच्नुहोस्
        • गुणस्तर: राम्रो फसल बढी मूल्यमा बिक्छ
        
        सामूहिक बिक्री गर्दा फाइदा हुन्छ।""",
        
        'default': """तपाईंको प्रश्नको लागि धन्यवाद! 
        
        कृपया थप स्पष्ट गरेर सोध्नुहोस्:
        • कुन बाली बारे जान्न चाहनुहुन्छ?
        • के समस्या छ?
        • कुन मौसममा रोप्ने सोच्दै हुनुहुन्छ?
        
        म तपाईंलाई राम्रो सल्लाह दिन चाहन्छु।"""
    }
    
    responses_en = {
        'rice': """Rice farming advice:
        • Planting: Prepare nursery in May-June
        • Water: Provide regular irrigation
        • Fertilizer: Use urea and DAP
        
        Contact nearby agriculture office if problems occur.""",
        
        'corn': """Corn farming tips:
        • Planting: Plant in March-April
        • Spacing: Keep 75cm x 25cm distance
        • Fertilizer: Use compost + chemical fertilizer
        
        Apply iron-rich fertilizer if yellowing occurs.""",
        
        'vegetable': """Vegetable farming:
        • Choose seeds according to season
        • Use organic fertilizer
        • Regular watering and weeding
        
        Sell according to market prices.""",
        
        'potato': """Potato cultivation:
        • Planting: October-December
        • Seeds: Use certified seeds
        • Soil: Well-drained loose soil
        
        Spray copper sulfate if spots appear.""",
        
        'yellow': """If crops turn yellow:
        • Cause: May be nitrogen deficiency
        • Solution: Apply urea fertilizer
        • Water: Ensure adequate water
        
        Consult expert if no improvement in 2 weeks.""",
        
        'pest': """Pest control:
        • Organic method: Use neem oil
        • Chemical: Consult agriculture shop
        • Prevention: Maintain clean farming
        
        Wear safety equipment when spraying.""",
        
        'weather': """Weather-based farming:
        • Rainy season: Good for rice and corn
        • Winter: Wheat and vegetables
        • Summer: Arrange irrigation
        
        Check weather forecast before farming.""",
        
        'fertilizer': """Fertilizer application:
        • Organic: Compost and manure
        • Chemical: Urea, DAP, Potash
        • Timing: Apply during planting and flowering
        
        Don't over-apply, it damages soil.""",
        
        'market': """Market information:
        • Prices: Check daily market rates
        • Selling time: Sell early morning
        • Quality: Good crops fetch higher prices
        
        Group selling is beneficial.""",
        
        'default': """Thank you for your question!
        
        Please be more specific:
        • Which crop do you want to know about?
        • What problem are you facing?
        • Which season are you planning to plant?
        
        I want to give you good advice."""
    }
    
    # Select response set based on language
    responses = responses_ne if language == 'ne' else responses_en
    
    # Keywords for different topics (works for both languages)
    keywords = {
        'rice': ['धान', 'चामल', 'rice', 'paddy'],
        'corn': ['मकै', 'corn', 'maize'],
        'vegetable': ['तरकारी', 'vegetable', 'साग', 'vegetables'],
        'potato': ['आलु', 'potato', 'potatoes'],
        'yellow': ['पहेंलो', 'yellow', 'yellowing', 'पहेलो'],
        'pest': ['किरा', 'pest', 'insect', 'insects', 'bug'],
        'weather': ['मौसम', 'weather', 'पानी', 'water', 'climate'],
        'fertilizer': ['मल', 'fertilizer', 'खाद', 'manure', 'compost'],
        'market': ['बजार', 'market', 'मूल्य', 'price', 'selling', 'बेच्ने']
    }
    
    # Find matching category
    for category, words in keywords.items():
        if any(word in message_lower for word in words):
            return responses[category]
    
    # Default response
    return responses['default']

def get_placeholder_weather():
    """Return placeholder weather data"""
    return {
        'temperature': 28,
        'condition': 'घाम र बादल',
        'humidity': 65,
        'rainfall': 0,
        'advice': 'फसल रोप्नको लागि राम्रो मौसम छ'
    }

def get_placeholder_news():
    """Return placeholder agriculture news"""
    return [
        {
            'title': 'धान बीउ वितरण सुरु',
            'summary': 'सरकारले उन्नत किसिमको धान बीउ वितरण गर्न थालेको छ।',
            'time': '२ घण्टा अगाडि',
            'category': 'subsidy'
        },
        {
            'title': 'मल अनुदान कार्यक्रम',
            'summary': 'यो महिनाका लागि मल अनुदान दर घोषणा भएको छ।',
            'time': '५ घण्टा अगाडि',
            'category': 'subsidy'
        },
        {
            'title': 'नयाँ कृषि प्रविधि',
            'summary': 'जैविक खेती प्रविधिको तालिम कार्यक्रम सञ्चालन हुँदै।',
            'time': '१ दिन अगाडि',
            'category': 'training'
        }
    ]

def get_current_season():
    """Determine current agricultural season"""
    month = datetime.now().month
    
    if month in [6, 7, 8, 9]:  # June to September
        return "वर्षा/धान रोपाइं"
    elif month in [10, 11, 12, 1]:  # October to January  
        return "शीत/फसल काट्ने"
    else:  # February to May
        return "वसन्त/तरकारी रोपाइं"

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def get_market_prices(request):
    """Return placeholder market prices"""
    prices = {
        'धान': 'रु. २५-३०/के.जी',
        'मकै': 'रु. ३२-३८/के.जी',
        'आलु': 'रु. ४५-५०/के.जी',
        'प्याज': 'रु. ४०-६०/के.जी',
        'टमाटर': 'रु. ६०-८०/के.जी'
    }
    return JsonResponse({'success': True, 'prices': prices})

# Keep your existing views for backward compatibility
def recorder(request):
    recordings = AudioRecording.objects.all().order_by('-created_at')
    return render(request, 'recorder.html', {'recordings': recordings})

@csrf_exempt
def save(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'New Recording')
        audio_file = request.FILES.get('audio_file') 
        
        if audio_file:
            recording = AudioRecording.objects.create(
                title=title,
                audio_file=audio_file
            )
            return JsonResponse({'success': True, 'id': recording.id})
    
    return JsonResponse({'success': False})
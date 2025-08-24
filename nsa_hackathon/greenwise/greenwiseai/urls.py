# urls.py - Simplified URL patterns for initial setup
from django.urls import path
from . import views

urlpatterns = [
    # Main interface
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # API endpoints (working without external APIs)
    path('api/message/', views.process_message, name='process_message'),
    path('api/market-prices/', views.get_market_prices, name='market_prices'),
    
    # Legacy endpoints (keep for backward compatibility)  
    path('save/', views.save, name='save'),
    path('recorder/', views.recorder, name='recorder'),
]
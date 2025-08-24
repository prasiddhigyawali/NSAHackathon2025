from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os

# Create your models here.

class AudioRecording(models.Model):
    title = models.CharField(max_length=100, blank=True)
    audio_file = models.FileField(upload_to="recordings/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Recording {self.id}"
    
    class Meta:
        db_table = 'audio_recording'  # Explicit table name

# New models for Krisi Sahayak

class FarmerQuery(models.Model):
    """Store farmer queries for data collection and analytics"""
    question = models.TextField(help_text="Farmer's original question")
    answer = models.TextField(help_text="AI generated response")
    location = models.CharField(max_length=100, blank=True, help_text="User location")
    language = models.CharField(max_length=20, default='nepali')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, help_text="Browser session")
    
    # Contextual information
    weather_condition = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=50, blank=True)
    crop_mentioned = models.CharField(max_length=100, blank=True, help_text="Main crop discussed")
    
    # Metadata
    query_type = models.CharField(max_length=20, choices=[
        ('voice', 'Voice Input'),
        ('text', 'Text Input')
    ], default='text')
    
    response_time = models.FloatField(default=0.0, help_text="AI response time in seconds")
    user_satisfaction = models.IntegerField(null=True, blank=True, 
                                          help_text="1-5 rating from user")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'farmer_queries'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Query {self.id}: {self.question[:50]}..."

class NewsItem(models.Model):
    """Store agriculture news for farmers"""
    title = models.CharField(max_length=200)
    summary = models.TextField()
    source_url = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('subsidy', 'Government Subsidy'),
        ('weather', 'Weather Alert'),
        ('market', 'Market Prices'),
        ('technology', 'New Technology'),
        ('training', 'Training Programs'),
        ('general', 'General News')
    ])
    
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1, help_text="1=Low, 5=Critical")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'news_items'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title

class WeatherData(models.Model):
    """Store weather data for agricultural advice"""
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField(default=0.0, help_text="In mm")
    wind_speed = models.FloatField(default=0.0, help_text="In km/h")
    weather_condition = models.CharField(max_length=100)
    
    # Agricultural recommendations based on weather
    farming_advice = models.TextField(blank=True)
    suitable_activities = models.TextField(blank=True, 
                                         help_text="Comma-separated farming activities")
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'weather_data'
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.location} - {self.weather_condition}"
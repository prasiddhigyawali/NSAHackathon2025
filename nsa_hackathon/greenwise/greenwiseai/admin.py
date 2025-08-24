# admin.py - Start with these essential models
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import AudioRecording, FarmerQuery, NewsItem, WeatherData

# Your existing AudioRecording admin (keep as is)
@admin.register(AudioRecording)
class AudioRecordingAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'audio_file']
    list_filter = ['created_at']
    search_fields = ['title']
    ordering = ['-created_at']

# New models admin classes
@admin.register(FarmerQuery)
class FarmerQueryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'question_preview', 'crop_mentioned', 'location', 
        'query_type', 'satisfaction_display', 'timestamp'
    ]
    list_filter = [
        'query_type', 'language', 'location', 'season', 
        'user_satisfaction', 'timestamp'
    ]
    search_fields = ['question', 'answer', 'crop_mentioned', 'location']
    readonly_fields = ['timestamp', 'response_time', 'ip_address']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Query Information', {
            'fields': ('question', 'answer', 'query_type', 'language')
        }),
        ('Context Data', {
            'fields': ('location', 'season', 'weather_condition', 'crop_mentioned')
        }),
        ('User Feedback', {
            'fields': ('user_satisfaction', 'response_time')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'session_id', 'timestamp'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = "Question"
    
    def satisfaction_display(self, obj):
        if obj.user_satisfaction:
            stars = "⭐" * obj.user_satisfaction
            color = "green" if obj.user_satisfaction >= 4 else "orange" if obj.user_satisfaction >= 3 else "red"
            return format_html(
                '<span style="color: {};">{} ({})</span>', 
                color, stars, obj.user_satisfaction
            )
        return "No rating"
    satisfaction_display.short_description = "Satisfaction"

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'priority_display', 'is_active', 
        'created_at', 'expires_at'
    ]
    list_filter = ['category', 'priority', 'is_active', 'created_at']
    search_fields = ['title', 'summary']
    ordering = ['-priority', '-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'summary', 'category', 'source_url')
        }),
        ('Settings', {
            'fields': ('priority', 'is_active', 'expires_at')
        }),
    )
    
    def priority_display(self, obj):
        colors = {1: 'green', 2: 'blue', 3: 'orange', 4: 'red', 5: 'darkred'}
        return format_html(
            '<span style="color: {};">Priority {}</span>', 
            colors.get(obj.priority, 'black'), obj.priority
        )
    priority_display.short_description = "Priority"

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = [
        'location', 'temperature', 'humidity', 'weather_condition', 
        'rainfall', 'recorded_at'
    ]
    list_filter = ['location', 'weather_condition', 'recorded_at']
    search_fields = ['location', 'weather_condition', 'farming_advice']
    ordering = ['-recorded_at']
    readonly_fields = ['recorded_at']
    
    fieldsets = (
        ('Location & Time', {
            'fields': ('location', 'recorded_at')
        }),
        ('Weather Data', {
            'fields': ('temperature', 'humidity', 'rainfall', 'wind_speed', 'weather_condition')
        }),
        ('Agricultural Advice', {
            'fields': ('farming_advice', 'suitable_activities')
        }),
    )

# Custom admin site header
admin.site.site_header = "कृषि सहायक Administration"
admin.site.site_title = "Krisi Sahayak Admin"
admin.site.index_title = "Welcome to Krisi Sahayak Admin Panel"
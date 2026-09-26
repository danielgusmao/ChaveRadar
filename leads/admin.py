from django.contrib import admin
from .models import Classification, CollectionRun, Comment, MonitoringProfile, Profile, Publication


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('handle', 'display_name', 'source_type', 'active', 'last_sync_at')
    search_fields = ('handle', 'display_name')
    list_filter = ('source_type', 'active')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'property_type', 'property_region', 'transaction_type', 'published_at')
    search_fields = ('profile__handle', 'property_type', 'property_region', 'caption_original')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'publication', 'displayed_date_original', 'source_type', 'captured_at')
    search_fields = ('username', 'display_name', 'text_original')
    list_filter = ('source_type',)


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('comment', 'qualification', 'is_lead', 'review_status', 'confidence')
    list_filter = ('qualification', 'is_lead', 'review_status')


@admin.register(CollectionRun)
class CollectionRunAdmin(admin.ModelAdmin):
    list_display = ('profile', 'source_type', 'status', 'comments_found', 'comments_new', 'started_at')
    list_filter = ('source_type', 'status')


@admin.register(MonitoringProfile)
class MonitoringProfileAdmin(admin.ModelAdmin):
    list_display = ('handle', 'display_name', 'active', 'alerts_enabled', 'last_status', 'last_checked_at')
    search_fields = ('handle', 'display_name', 'keywords', 'notes')
    list_filter = ('active', 'alerts_enabled', 'last_status')

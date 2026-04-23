from django.contrib import admin

from .models import KnowledgeArticle, LeadRequest, NewsletterSubscriber


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'content')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'company', 'subscribed_at')
    search_fields = ('email', 'first_name', 'company')


@admin.register(LeadRequest)
class LeadRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'instagram_handle', 'created_at')
    search_fields = ('name', 'email', 'instagram_handle', 'message')

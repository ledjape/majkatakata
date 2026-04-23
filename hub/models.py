from django.db import models


class KnowledgeArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.title


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80, blank=True)
    company = models.CharField(max_length=120, blank=True)
    goals = models.TextField(blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-subscribed_at',)

    def __str__(self) -> str:
        return self.email


class LeadRequest(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    instagram_handle = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.name} ({self.email})'

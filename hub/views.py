from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import LeadRequestForm, NewsletterForm
from .models import KnowledgeArticle


def home(request):
    featured_article = KnowledgeArticle.objects.filter(is_featured=True).first()
    latest_articles = KnowledgeArticle.objects.all()[:6]

    newsletter_form = NewsletterForm(prefix='newsletter')
    lead_form = LeadRequestForm(prefix='lead')

    if request.method == 'POST':
        if 'newsletter-submit' in request.POST:
            newsletter_form = NewsletterForm(request.POST, prefix='newsletter')
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, 'Thanks! You are now subscribed.')
                return redirect('home')
        elif 'lead-submit' in request.POST:
            lead_form = LeadRequestForm(request.POST, prefix='lead')
            if lead_form.is_valid():
                lead_form.save()
                messages.success(request, 'Thanks! We will reach out soon.')
                return redirect('home')

    context = {
        'featured_article': featured_article,
        'latest_articles': latest_articles,
        'newsletter_form': newsletter_form,
        'lead_form': lead_form,
    }
    return render(request, 'hub/home.html', context)

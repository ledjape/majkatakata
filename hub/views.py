from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import LeadRequestForm, NewsletterForm
from .models import KnowledgeArticle


def home(request):
    try:
        featured_article = KnowledgeArticle.objects.filter(is_featured=True).first()
        latest_articles = KnowledgeArticle.objects.all()[:6]
    except Exception:
        featured_article = None
        latest_articles = []

    newsletter_form = NewsletterForm(prefix='newsletter')
    lead_form = LeadRequestForm(prefix='lead')

    if request.method == 'POST':
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

        if 'newsletter-submit' in request.POST:
            newsletter_form = NewsletterForm(request.POST, prefix='newsletter')
            if newsletter_form.is_valid():
                newsletter_form.save()
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Благодариме! Вашата претплата е успешна.'})
                messages.success(request, 'Благодариме! Вашата претплата е успешна.')
                return redirect('home')
            elif is_ajax:
                return JsonResponse({'success': False, 'errors': newsletter_form.errors}, status=400)

        elif 'lead-submit' in request.POST or is_ajax:
            lead_form = LeadRequestForm(request.POST, prefix='lead')
            if lead_form.is_valid():
                lead = lead_form.save()
                
                # Send email notification to recipient list
                subject = f"🍼 Нова пријава за BLW обука: {lead.name}"
                message = (
                    f"Примена е нова регистрација на страницата majkatakata:\n\n"
                    f"👤 Име на родител: {lead.name}\n"
                    f"📧 Е-пошта: {lead.email}\n"
                    f"👶 Фаза на бебето: {lead.baby_stage}\n"
                    f"🎓 Пријава за обука со Катерина: {'Да (Потврдено)' if lead.training_course_signup else 'Не'}\n"
                    f"📝 Прашања/Белешки: {lead.message or 'Нема белешки'}\n\n"
                    f"Детали во Admin: http://127.0.0.1:8000/admin/hub/leadrequest/{lead.id}/change/"
                )
                
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pejahs@gmail.com'),
                        recipient_list=getattr(settings, 'NOTIFICATION_RECIPIENTS', ['delikates@gmail.com']),
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Error sending lead notification email: {e}")

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message_mk': 'Благодариме! Вашата пријава е успешно испратена. Ќе ве контактираме наскоро.',
                        'message_en': 'Thank you! Your registration has been submitted successfully. We will reach out soon.'
                    })

                messages.success(request, 'Благодариме! Вашата пријава е успешно испратена.')
                return redirect('home')
            elif is_ajax:
                return JsonResponse({'success': False, 'errors': lead_form.errors}, status=400)

    context = {
        'featured_article': featured_article,
        'latest_articles': latest_articles,
        'newsletter_form': newsletter_form,
        'lead_form': lead_form,
    }
    return render(request, 'hub/home.html', context)

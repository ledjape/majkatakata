from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
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

    import time
    newsletter_form = NewsletterForm(prefix='newsletter')
    lead_form = LeadRequestForm(prefix='lead', initial={'form_ts': time.time()})

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
                # Anti-Spam Defense: Silent drop if flagged by honeypot or time-gate
                if lead_form.cleaned_data.get('is_spam'):
                    print(f"🛡️ Spam bot detected and silently dropped: {lead_form.cleaned_data.get('name')} | {lead_form.cleaned_data.get('email')}")
                    if is_ajax:
                        return JsonResponse({
                            'success': True,
                            'message_mk': 'Благодариме! Вашата пријава е успешно испратена. Ќе ве контактираме наскоро.',
                            'message_en': 'Thank you! Your registration has been submitted successfully. We will reach out soon.'
                        })
                    messages.success(request, 'Благодариме! Вашата пријава е успешно испратена.')
                    return redirect('home')

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
                
                # Send email notification in a background thread using Resend HTTPS API (Port 443, never blocked)
                def send_email_async(sub, msg, recips):
                    import urllib.request, json
                    resend_key = getattr(settings, 'RESEND_API_KEY', None)
                    resend_from = getattr(settings, 'RESEND_FROM_EMAIL', 'majkatakata <onboarding@resend.dev>')
                    
                    if resend_key:
                        try:
                            url = 'https://api.resend.com/emails'
                            payload = {
                                'from': resend_from,
                                'to': recips,
                                'subject': sub,
                                'text': msg
                            }
                            req = urllib.request.Request(
                                url,
                                data=json.dumps(payload).encode('utf-8'),
                                headers={
                                    'Authorization': f'Bearer {resend_key}',
                                    'Content-Type': 'application/json',
                                    'User-Agent': 'majkatakata-app'
                                }
                            )
                            with urllib.request.urlopen(req, timeout=8) as resp:
                                print("Email delivered successfully via Resend HTTPS API")
                                return
                        except Exception as resend_err:
                            print(f"Resend API error: {resend_err}")
                    
                    # Fallback to standard Django send_mail
                    try:
                        from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', 'pejahs@gmail.com')
                        send_mail(
                            subject=sub,
                            message=msg,
                            from_email=from_addr,
                            recipient_list=recips,
                            fail_silently=True,
                        )
                    except Exception as err:
                        print(f"Fallback send_mail error: {err}")

                recipients = getattr(settings, 'NOTIFICATION_RECIPIENTS', ['delikates@gmail.com', 'pejahs@gmail.com'])
                
                import threading
                threading.Thread(target=send_email_async, args=(subject, message, recipients), daemon=True).start()



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


def google_verification(request):
    return HttpResponse('google-site-verification: google8e77f9c223e6e972.html', content_type='text/html')


def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://majkatakata.com/sitemap.xml
"""
    return HttpResponse(content.strip(), content_type='text/plain')


def sitemap_xml(request):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://majkatakata.com/</loc>
    <lastmod>2026-09-16</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    return HttpResponse(content.strip(), content_type='application/xml')


from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from .models import LeadRequest


class RegistrationFormTestCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.url = reverse('home')

    def test_get_home_page_includes_csrf_token(self):
        """Test GET request returns 200 OK and contains CSRF token."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_post_registration_form_success(self):
        """Test submitting the registration form creates database record and sends email notification."""
        get_response = self.client.get(self.url)
        csrf_token = get_response.cookies['csrftoken'].value

        post_data = {
            'csrfmiddlewaretoken': csrf_token,
            'lead-name': 'Ana Galić',
            'lead-email': 'ana.galic@example.com',
            'lead-baby_stage': 'Expecting (Pregnant)',
            'lead-training_course_signup': 'Yes',
            'lead-message': 'Testing registration form submission',
            'lead-human_check': '1',
            'lead-honeypot': '',
            'lead-submit': 'Submit Registration',
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

        self.assertEqual(LeadRequest.objects.count(), 1)
        lead = LeadRequest.objects.first()
        self.assertEqual(lead.name, 'Ana Galić')
        self.assertEqual(lead.email, 'ana.galic@example.com')
        self.assertEqual(lead.training_course_signup, 'Yes')

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Ana Galić', email.subject)

    def test_post_ajax_registration_form_success(self):
        """Test submitting registration via AJAX returns JSON response without redirect."""
        get_response = self.client.get(self.url)
        csrf_token = get_response.cookies['csrftoken'].value

        post_data = {
            'csrfmiddlewaretoken': csrf_token,
            'lead-name': 'Elena Risteska',
            'lead-email': 'elena@example.com',
            'lead-baby_stage': '0-6 months',
            'lead-training_course_signup': 'Yes',
            'lead-message': 'Testing AJAX submission',
            'lead-human_check': '1',
            'lead-honeypot': '',
        }

        response = self.client.post(self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertIn('Благодариме', json_data['message_mk'])

        self.assertEqual(LeadRequest.objects.count(), 1)

    def test_missing_human_check_rejected(self):
        """Test submitting form without human check boolean fails validation."""
        get_response = self.client.get(self.url)
        csrf_token = get_response.cookies['csrftoken'].value

        post_data = {
            'csrfmiddlewaretoken': csrf_token,
            'lead-name': 'Bot User',
            'lead-email': 'bot@example.com',
            'lead-baby_stage': '0-6 months',
            'lead-training_course_signup': 'Yes',
        }

        response = self.client.post(self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('human_check', json_data['errors'])
        self.assertEqual(LeadRequest.objects.count(), 0)

    def test_honeypot_spambot_rejected(self):
        """Test honeypot field submission is rejected as bot spam."""
        get_response = self.client.get(self.url)
        csrf_token = get_response.cookies['csrftoken'].value

        post_data = {
            'csrfmiddlewaretoken': csrf_token,
            'lead-name': 'Spam Bot',
            'lead-email': 'spambot@example.com',
            'lead-baby_stage': '0-6 months',
            'lead-training_course_signup': 'Yes',
            'lead-human_check': '1',
            'lead-honeypot': 'http://spam-link.com',
        }

        response = self.client.post(self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('honeypot', json_data['errors'])
        self.assertEqual(LeadRequest.objects.count(), 0)

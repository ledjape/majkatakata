from django import forms
from .models import LeadRequest, NewsletterSubscriber

STAGE_CHOICES = (
    ('Expecting (Pregnant)', 'Expecting (Pregnant)'),
    ('0-6 months', '0-6 months'),
    ('6-9 months', '6-9 months'),
    ('9-12 months', '9-12 months'),
    ('12+ months', '12+ months'),
)

COURSE_SIGNUP_CHOICES = (
    ('Yes', 'Да, сакам да се пријавам за обука со Катерина (Yes)'),
    ('No', 'Не, во моментов сакам само информации (No)'),
)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email', 'first_name', 'company', 'goals')
        widgets = {'goals': forms.Textarea(attrs={'rows': 3})}


class LeadRequestForm(forms.ModelForm):
    baby_stage = forms.ChoiceField(
        choices=STAGE_CHOICES,
        initial='Expecting (Pregnant)',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    training_course_signup = forms.ChoiceField(
        choices=COURSE_SIGNUP_CHOICES,
        initial='Yes',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    human_check = forms.BooleanField(
        required=True,
        error_messages={'required': 'Ве молиме потврдете дека сте човек.'}
    )

    # Stealth Honeypots: attractive to automated bots, hidden from humans
    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'})
    )
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'})
    )
    form_ts = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = LeadRequest
        fields = ('name', 'email', 'baby_stage', 'training_course_signup', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Ana Galić',
                'autocomplete': 'name',
                'autocapitalize': 'words',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'name@example.com',
                'autocomplete': 'email',
                'inputmode': 'email',
            }),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell me about your baby or any specific questions...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        hp = cleaned_data.get('honeypot')
        website = cleaned_data.get('website_url')
        ts = cleaned_data.get('form_ts')

        # 1. Stealth Honeypot check: If any honeypot was filled, flag as spam
        if hp or website:
            cleaned_data['is_spam'] = True
            return cleaned_data

        # 2. Time-Gate check: Real humans take at least 3 seconds to complete the form
        if ts:
            try:
                import time
                rendered_at = float(ts)
                elapsed = time.time() - rendered_at
                if elapsed < 3.0:
                    cleaned_data['is_spam'] = True
                    return cleaned_data
            except (ValueError, TypeError):
                cleaned_data['is_spam'] = True
                return cleaned_data

        cleaned_data['is_spam'] = False
        return cleaned_data


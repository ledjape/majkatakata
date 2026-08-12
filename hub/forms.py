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

    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none !important;', 'tabindex': '-1', 'autocomplete': 'off'})
    )

    class Meta:
        model = LeadRequest
        fields = ('name', 'email', 'baby_stage', 'training_course_signup', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Ana Galić'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell me about your baby or any specific questions...'
            }),
        }

    def clean_honeypot(self):
        hp = self.cleaned_data.get('honeypot')
        if hp:
            raise forms.ValidationError("Bot submission detected.")
        return hp

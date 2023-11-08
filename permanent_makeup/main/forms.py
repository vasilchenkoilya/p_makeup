from django import forms
from .models import Review, Service

class ReviewForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['service', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
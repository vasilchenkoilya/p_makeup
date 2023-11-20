from typing import List, Tuple
from django import forms
from .models import Review, Service, Reservation, TimeSlot
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class ReviewForm(forms.ModelForm):
    """
    Form for submitting reviews.
    """

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Review
        fields: List[str] = ['service', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    """
    Form for making reservations.
    """

    class Meta:
        model = Reservation
        fields: List[str] = ['service', 'time_slot']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'time_slot': DateTimePickerInput(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'time_slot': 'Available time:',
            'service': 'Treatment:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['service'].widget = forms.Select(choices=self.get_available_services(attrs={'class': 'form-control'}))
        self.fields['time_slot'].widget = forms.Select(choices=self.get_available_slots(attrs={'class': 'form-control'}))

    def get_available_services(self, attrs=None) -> List[Tuple[str, str]]:
        """
        Get available services as choices for the form.
        """
        available_services = Service.objects.all().order_by('name')

        available_services_choices = []
        for service in available_services:
            service_info = (str(service.id), f"{service.name}")
            available_services_choices.append(service_info)

        return [('', '---')] + available_services_choices

    def get_available_slots(self, attrs=None) -> List[Tuple[str, str]]:
        """
        Get available time slots as choices for the form.
        """
        available_slots = TimeSlot.objects.filter(is_available=True).order_by('start_time')

        available_slots_choices = []
        for slot in available_slots:
            slot_info = (
                str(slot.id),
                f"{slot.start_time.strftime('%Y-%m-%d // %H:%M')} - {slot.end_time.strftime('%H:%M')}"
            )
            available_slots_choices.append(slot_info)

        return [('', '---')] + available_slots_choices


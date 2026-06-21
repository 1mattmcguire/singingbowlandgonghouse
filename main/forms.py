from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        required_fields = [
            "name",
            "email",
            "phone",
            "service",
            "booking_date",
            "session_type",
        ]

        missing = [f for f in required_fields if not cleaned_data.get(f)]

        if missing:
            raise forms.ValidationError(
                "Please fill all required fields before submitting the form."
            )

        return cleaned_data
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['service'].required = True
        self.fields['booking_date'].required = True


   
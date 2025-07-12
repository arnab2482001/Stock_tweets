from django import forms


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={"placeholder": "DD-MM-YYYY"}),
        input_formats=["%d-%m-%Y"],
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={"placeholder": "DD-MM-YYYY"}),
        input_formats=["%d-%m-%Y"],
    )

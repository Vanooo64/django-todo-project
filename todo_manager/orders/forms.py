from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("title", "content", "type_of_work", "subject", "plagiarism_percentage", "file_upload", "deadline")

        widgets = {
            "title": forms.Textarea(attrs={"cols": 30, "rows": 5}),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


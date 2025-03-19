from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("title", "content", "type_of_work", "subject", "plagiarism_percentage", "order_amount", "file_upload", "deadline", "status",)

        widgets = {
            "title": forms.Textarea(attrs={"cols": 30, "rows": 5}),
        }

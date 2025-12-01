from django import forms
# from main.validators import mark_validator
from main.models import SiteReview
from main.fields import CharField, TextField, IntegerField


# class SiteReviewForm(forms.ModelForm):
#     class Meta:
#         model = SiteReview
#         fields = ["name", "mark", "text"]
#         widgets = {
#             "name":  forms.TextInput(attrs={
#                 "class": "form-control",
#                 "placeholder": "Ваше ім'я"
#             }),
#             "mark":  forms.NumberInput(attrs={
#                 "class": "form-control",
#                 "min": "1",
#                 "max": "10",
#             }),
#             "text":  forms.Textarea(attrs={
#                 "class": "form-control",
#                 "placeholder": "Ваш відгук"
#             }),
#         }   

    # def clean_mark(self):
    #     mark = self.cleaned_data.get("mark")
    #     if mark < 1 or mark > 10:
    #         raise forms.ValidationError("Оцінка повинна бути від 1 до 10")
    #     return mark

    
class SiteReviewForm(forms.Form):
    name = CharField(
        max_length=255,
    )
    mark = IntegerField(
        min_value=1,
        max_value=10,
    )
    text = TextField()

    def clean_text(self):
        if len(self.cleaned_data['text']) < 10:
            raise forms.ValidationError("Error text")
        return self.cleaned_data['text']
    
    def save(self):
        data = self.cleaned_data
        review = SiteReview.objects.create(
            name=data['name'],
            mark=data['mark'],
            text=data['text']
        )
        return review
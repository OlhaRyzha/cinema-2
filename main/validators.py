from django import forms

def mark_validator(value):
    if value < 1 or value > 10:
        raise forms.ValidationError("Оцінка повинна бути від 1 до 10")
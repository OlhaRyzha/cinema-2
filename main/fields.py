from django import forms


class BaseFieldMixin:
    def __init__(self, *args, **kwargs):
        widget = self.widget()
        widget.attrs.update({
            "class": "form-control",
        })
        super().__init__(widget=widget, *args, **kwargs)

class TextField(BaseFieldMixin, forms.CharField):
    widget = forms.Textarea
    
class IntegerField(BaseFieldMixin, forms.IntegerField):
    widget = forms.NumberInput
    
class CharField(BaseFieldMixin, forms.CharField):
    widget = forms.TextInput

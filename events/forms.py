from django import forms
from .models import Category, Event, Participant

class StyledFormMixin:
    '''Mixin to apply styles to form fields'''
    default_classes = "border-2 border-gray-600 w-full p-3 rounded-lg shadow-sm focus:border-rose-300 focus:ring-red-400"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Describe the {field.label.lower()}",
                    'rows': 5,
                })
            # elif isinstance(field.widget, forms.DateInput):
            #     field.widget.attrs.update({'type': 'date', 'class': self.default_classes})
            # elif isinstance(field.widget, forms.TimeInput):
            #     field.widget.attrs.update({'type': 'time', 'class': self.default_classes})


class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
    'date': forms.DateInput(attrs={
        'type': 'date',
        'class': 'w-full bg-gray-700 border border-gray-600 text-white rounded-lg p-3 focus:ring-2 focus:ring-rose-400 focus:border-rose-400 transition duration-200'
    }),
    'time': forms.TimeInput(attrs={
        'type': 'time',
        'class': 'w-full bg-gray-700 border border-gray-600 text-white rounded-lg p-3 focus:ring-2 focus:ring-cyan-400 focus:border-cyan-400 transition duration-200'
    }),
    'category': forms.Select(attrs={
        'class': 'w-full bg-gray-700 border border-gray-600 text-white rounded-lg p-3 focus:ring-2 focus:ring-cyan-400 focus:border-cyan-400 transition duration-200'
    }),
}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()  # Fetch all categories dynamically
        self.apply_styled_widgets()


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'events': forms.SelectMultiple(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 text-white rounded-lg p-3 focus:ring-2 focus:ring-blue-500 transition duration-200'
            })
        }

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'


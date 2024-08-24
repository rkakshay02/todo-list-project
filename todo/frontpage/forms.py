from django import forms
from .models import Task

class LoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(choices=Task.STATUS_CHOICES)
        }

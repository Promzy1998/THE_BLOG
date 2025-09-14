from django.contrib import admin
from django import forms
from .models import DataPost

class DataPostForm(forms.ModelForm):
    buttonColor = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color'})
    )

    class Meta:
        model = DataPost
        fields = '__all__'

class DataPostAdmin(admin.ModelAdmin):
    form = DataPostForm

admin.site.register(DataPost, DataPostAdmin)

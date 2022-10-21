from dataclasses import fields
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        modle = Review
        fields = ['title', 'content', 'movie_name', 'grade', ]
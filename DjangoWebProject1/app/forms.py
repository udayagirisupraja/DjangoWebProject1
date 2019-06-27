"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

# forms.py 
from .models import *

class FileUploadForm(forms.ModelForm): 
	class Meta: 
		model = File_Upload 
		fields = ['log_File'] 
"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum

# models.py 
class File_Upload(models.Model): 
	log_File = models.FileField(upload_to='log_Files/') 

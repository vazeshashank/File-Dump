# uploadapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from cryptography.fernet import Fernet
from django.views.decorators.cache import cache_control
from django.contrib import messages
import os


key = Fernet.generate_key()

def handle_uploaded_file(f, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def encrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)
@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            filename = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            handle_uploaded_file(uploaded_file, filename)
            encrypt_file(filename, key) 
            messages.success(request,"File Uploaded")
            return HttpResponse('File uploaded and encrypted successfully.')
        else:
            messages.error(request,'No file selected to upload')
            return HttpResponse('Failed to Upload')
    return render(request, 'upload.html')

from django.shortcuts import render
from base64 import b64encode

from django.core.files.storage import FileSystemStorage

def home(request):
	if request.method == 'POST':
		uploaded_file = request.FILES['image']
		fs = FileSystemStorage()
		name = fs.save(uploaded_file.name, uploaded_file)
		url = fs.url(name)
		return render(request, 'threshold.html', {'url': url})
	return render(request, 'home.html')

def threshold(request):
	return render(request, 'threshold.html')

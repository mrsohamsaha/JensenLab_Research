from django.shortcuts import render

def home(request):
	if request.method == 'POST':
		uploaded_file = request.FILES['image']
		print(uploaded_file.name)
		print(uploaded_file.size)
	return render(request, 'home.html')

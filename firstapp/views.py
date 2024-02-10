from django.shortcuts import render

# Create your views here.

def hello_view(request):
    message = "Hello World Django"
    return render(request, 'firstapp/index.html', {'message': message})

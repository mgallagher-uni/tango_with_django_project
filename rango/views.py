from django.shortcuts import render
from django.http import HttpResponse

# Import the Category model
from rango.models import Category

def index(request):
    # gets top 5 most liked categories
    # Place the list in our context_dict dictionary that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')
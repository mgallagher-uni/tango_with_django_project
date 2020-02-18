from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from django.urls import reverse
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    # gets top 5 most liked categories
    # Place the list in our context_dict dictionary that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):

    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
        
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # Boolean value representing the success of the registraion
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the users datato the database
            user = user_form.save()

            # Hash the password and update User object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user

            # Get profile picture and save in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registed = True
        
        else:
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST, render form using two ModelForm instances

        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
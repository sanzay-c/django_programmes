#-- **LoginRequiredMixin
#   It is a Django-provided mixin used to restrict access to views for authenticated users only.
#   If a user who is not logged in tries to access a view,
#   that uses LoginRequiredMixin, they are automatically redirected to the login page. is used for authentication --


#-- **View
#   It is the base class for all class-based views in Django.
#   The View class allows you to handle HTTP requests 
#   (like GET, POST, etc.) by defining corresponding methods (get, post, etc.).
#   Simplifies request handling by separating logic,
#   for different HTTP methods into separate methods (e.g., get, post).
#   Encourages modular and reusable code. --


from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receipe

class ReceipesView(LoginRequiredMixin, View):
    # redirects to login page if not authenticated
    login_url = "/login/"

    def get(self, request):
        # fetch all recipes from the database
        queryset = Receipe.objects.all()

        # check if there is a search query in the request
        search_query = request.GET.get('search')
        if search_query:
            # filter recipes based on the search query (case-insensitive)
            queryset = queryset.filter(receipe_name__icontains=search_query)

        # pass the filtered or full recipe list to the template
        context = {'receipes': queryset}
        return render(request, "receipes.html", context)

    def post(self, request):
        # retrieve data from the submitted form
        data = request.POST
        receipe_name = data.get('receipe_name') # get name of the recipe form the model i.e. receipe_name in model
        receipe_description = data.get('receipe_description') # get name of the recipe_description from the model
        receipe_image = request.FILES.get('receipe_image') # get name of the receipe_image from the model uploaded file name

        # Create a new recipe
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
        )

        # after creating a receipe redirect tto the page
        return redirect('receipes.html')


class DeleteReceipeView(View):
    def post(self, request, id):
        # fetch the recipe with the given ID from the database
        queryset = Receipe.objects.get(id=id)
        # delete the fetched recipe
        queryset.delete()
        # after deletion redirect to the page
        return redirect("/")


class UpdateReceipeView(View):
    def get(self, request, id):
        # fetch the specific recipe by its ID from the database
        queryset = Receipe.objects.get(id=id)
        # pass the fetched recipe to the update template
        context = {'receipe': queryset}
        # with the help of context we send the data from views to templates
        return render(request, 'update_receipes.html', context)

    def post(self, request, id):
        # fetch the specific recipe by its ID from the database
        queryset = Receipe.objects.get(id=id)
        # get updated data from the submitted form
        data = request.POST

        receipe_name = data.get('receipe_name') # get name of the recipe form the model i.e. receipe_name in model
        receipe_description = data.get('receipe_description') # get name of the recipe_description from the model
        receipe_image = request.FILES.get('receipe_image') # get name of the receipe_image from the model uploaded file name

        # Update the recipe fields
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image # update image only if a new one is provided

        # save the change from the database
        queryset.save()
        # after saving the data redirect to the page
        return redirect('')


class LoginPageView(View):
    def get(self, request):
        # render the login page when accessed via a GET request
        return render(request, 'login.html')

    def post(self, request):
        # retrieve the username and password from the submitted form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if the username exists in the database
        if not User.objects.filter(username=username).exists():
            # if the username is invalid, show an error message
            messages.error(request, 'Invalid username')
            # redirect to the login page
            return redirect('/login/')  

        # authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        if user is None:
            # if authentication fails (invalid password), show an error message
            messages.error(request, 'Invalid Password')
            # redirect back to the login page
            return redirect('/login/')  
        else:
            # if authentication is successful, log the user in
            login(request, user)
            # redirect to the recipes page after successful login
            return redirect('/receipe/')

class RegisterPageView(View):
    def get(self, request):
        # render the registration page when accessed via a GET request
        return render(request, 'register.html')

    def post(self, request):
        # retrieve the user registration details from the submitted form
        first_name = request.POST.get("first_name")  # Get the first name
        last_name = request.POST.get("last_name")    # Get the last name
        username = request.POST.get("username")     # Get the username
        password = request.POST.get("password")     # Get the password

        # check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            # if the username is taken, show an error message
            messages.info(request, 'Username already taken')
            # redirect back to the registration page
            return redirect('/register/')  

        # create a new user with the provided details
        user = User.objects.create(
            first_name=first_name,  # Set the first name
            last_name=last_name,    # Set the last name
            username=username,      # Set the username
        )
        # set the user's password (hashed for security)
        user.set_password(password)
        # save the user to the database
        user.save()  

        # inform the user that the account has been successfully created
        messages.info(request, 'Account created successfully')
        # redirect back to the registration page (or elsewhere)
        return redirect('/register/')  

class LogoutPageView(View):
    def get(self, request):
        # log out the currently logged-in user
        logout(request)

        # redirect the user to the login page after logging out
        return redirect('/login/')

class HomepageView(View):
    def get(self, request):
        # Render the 'homepage.html' template when the homepage is accessed via a GET request
        return render(request, 'homepage.html')


# -- explanation for => return render(request, 'template_name', context)
#     request: The HTTP request object passed to the view
#     template_name: The name of the HTML template to be used
#     context: A dictionary containing data you want to pass to the template. 
#     It makes dynamic content possible.--
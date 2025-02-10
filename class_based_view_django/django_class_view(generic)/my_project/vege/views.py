from django.shortcuts import render, redirect
# provide built-in behavior for common tasks like displaying, creating, updating, and deleting data. 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Receipe
from django.urls import reverse_lazy

# --**reverse_lazy 
#   allows you to defer resolving the URL until,
#   it's actually needed (like when the view is called or the page is rendered).
#   It’s used when the URL is needed in the future, not right away. 
#   It’s typically used in situations where URLs aren’t available yet --

# --**LoginRequiredMixin
#   is used for authentication
#   When a view uses LoginRequiredMixin, 
#   it checks if the user is logged in before letting them access the page.
#   If the user is not logged in, 
#   they will be automatically redirected to the URL specified in login_url (in this case, /login/).
#   *login_url = '/login/



# Receipes View (List and Search)
# ReceipesView inherits from LoginRequiredMixin and ListView to show the list of receipe
class ReceipesView(LoginRequiredMixin, ListView):
    model = Receipe # name of the model
    template_name = "receipes.html" # name of the templates for the views
    context_object_name = 'receipes' # in the template, the list of recipes can be accessed as 'receipes'
    login_url = '/login/' # if a non-logged-in user tries to access this view, they will be redirected to "/login/".

    def get_queryset(self):
        # get the default queryset from the model (all objects in the Receipe table).
        queryset = super().get_queryset()
        
        # check if there is a search query in the request
        search_query = self.request.GET.get('search')
        
        # if a search term is provided, filter the queryset to only include recipes
        # whose names contain the search term (case-insensitive match).
        if search_query:
            queryset = queryset.filter(receipe_name__icontains=search_query)
        
        return queryset


# Create Recipe View
# here, class name is CreateReceipeView which creats the receipe,
# which implements CreateView for the creations
# creating new records in the database
class CreateReceipeView(LoginRequiredMixin, CreateView):
    model = Receipe # name of the model
    template_name = 'create_receipe.html' # name of the templates
    
    # ---these fields name is actually the model name,
    #    fields name and model name should be maching to put the data, 
    #    we can use '__all__' for all the fileds in the models ---
    fields = ['receipe_name', 'receipe_description', 'receipe_image'] 

    login_url = '/login/' # if the user is not logged in, they will be redirected to this URL

    # redirect to the receipes list page after creation
    # --- *'receipes' is the name of a URL pattern defined in your urls.py file. 
    #       --urls.py file:
    #       path("receipe/", ReceipesView.as_view(), name="receipes"), --
    success_url = reverse_lazy('receipes')  

    # This function is called when the form is valid and ready to save
    def form_valid(self, form):
        # *form.instance: Refers to the object that is about to be created by the form. For example, if you're creating a new Receipe, form.instance represents that new Receipe object.
        # *self.request.user: Refers to the currently logged-in user who is making the request.
        form.instance.creator = self.request.user
        # Save the form and return the result
        return super().form_valid(form)


# Update Recipe View
# here, in UpdateReceipeView the 'UpdateView' is implemented to update the receipe
class UpdateReceipeView(LoginRequiredMixin, UpdateView):
    model = Receipe # name of the model
    template_name = 'update_receipes.html' # name of the templates
    fields = ['receipe_name', 'receipe_description', 'receipe_image'] # accessing fields for the update
    login_url = '/login/' # if the user is not logged in, they will be redirected to this URL

    def get_success_url(self):
        # --- *'receipes' is the name of a URL pattern defined in your urls.py file. 
        #       --urls.py file:
        #       path("receipe/", ReceipesView.as_view(), name="receipes"), --
        return reverse_lazy('receipes')  # Redirect back to receipes list after update


# Delete Recipe View
# here, in DeleteReceipeView the 'DeleteView' is implemented to delete the receipe
class DeleteReceipeView(LoginRequiredMixin, DeleteView):
    model = Receipe # name of the model
    template_name = 'confirm_delete_receipe.html' # name of templates to use this logic
    login_url = '/login/' # if the user is not logged in, they will be redirected to this URL
    # --- *'receipes' is the name of a URL pattern defined in your urls.py file. 
    #       --urls.py file:
    #       path("receipe/", ReceipesView.as_view(), name="receipes"), --
    success_url = reverse_lazy('receipes')  # Redirect to receipes list page after deletion


# Login View
# here, in the LoginPageView the TemplateView is implemented.
# TemplateView is just to render a template
# --- *TemplateView is a built-in Django view class that renders a template. 
#      It is used when you want to render a page without doing any complex logic or processing in the view itself
#      here we are not using the CreateView because you are not creating a new record in the database. 
#      Instead, you're checking whether a user exists, verifying their password, and then logging them in. 
#      So, using CreateView wouldn't be appropriate --- 
class LoginPageView(TemplateView):
    template_name = 'login.html' # name of the templates

    def post(self, request, *args, **kwargs):
        # get the username and password entered by the user from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the entered username exists in the database
        if not User.objects.filter(username=username).exists():
            # if the username doesn't exist, show an error message and reload the login page
            messages.error(request, 'Invalid username')
            return redirect('/login/') # this is the url
        
        # Authenticate the user using the entered username and password,
        # checking if the username and password matches or not. 
        user = authenticate(username=username, password=password)
        # if authentication fails, show an error message and reload the login page
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/') # this is the url
        else:
            login(request, user)
            return redirect('/receipe/')


# Register View
# here, for the RegisterPageView implementing a CreateView
# ---here, CreateView is important because we are creating a new user, 
#    registering a new user in the database so we use the CreateView---
class RegisterPageView(CreateView):
    model = User # name of the model
    template_name = 'register.html' # name of the templates
    fields = ['first_name', 'last_name', 'username', 'password'] # fields for creating a new user
    success_url = reverse_lazy('login_page') # this 'login_page' is the name given for urls in the urls.py file.

   # This method handles what happens when the form is valid and submitted
    def form_valid(self, form):
        # Set the password using the 'set_password' method (to securely hash the password)
        
        # ---*form.instance.set_password():
        #     form.instance refers to the actual model instance,
        #     that is being created or updated (in this case, the User model instance).
        #      set_password() is a method provided by Django's User model, it ensures that the password is securely hashed before being saved. ---

        # ---*form.cleaned_data['password']:
        #     form.cleaned_data is a dictionary that contains the data from the form after,
        #     it has been validated and cleaned by Django
        #     validated: Checking if the data is correct (e.g., does the email look like an email?).
        #     cleaned is the process of sanitizing the data to make sure it's safe and in the right format (e.g., trimming spaces or converting to the correct data type).
        #     'password' refers to the field from the form where the user entered their password.---
        form.instance.set_password(form.cleaned_data['password'])
        
        # Save the user data to the database
        form.save()
        
        # Show a success message to the user
        messages.info(self.request, 'Account created successfully')

        # Proceed with the normal form handling process
        return super().form_valid(form)


# Logout View
# here, the LogoutPageView implements the RedirectView
# ---*RedirectView is specifically designed for redirecting users to another URL.
#     It's a simple view for redirecting users without requiring any template rendering.
#     Since logging out doesn't require rendering a new template 
#     (you just want to log the user out and send them to another page), TemplateView is not necessary.---
class LogoutPageView(RedirectView):
    # define the URL to redirect to after the user logs out (in this case, the login page)
    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# Homepage View
# here, in the HomePageView we are implementing the the TemplateView, only to render a template
class HomepageView(TemplateView): 
    template_name = 'homepage.html' # name of the templates

from django.shortcuts import get_object_or_404, render
from .models import* 
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # iniially only 4 items is shown in the home page if dont want to show remove [:4] or add it.
    queryset = Recipe.objects.all()[:4] 
    context = {'recipes': queryset}
    return render(request,"index.html",context)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_ingridents = data.get('recipe_ingridents')
        instructions = data.get('instructions')
        cooking_time = data.get('cooking_time')
        category = data.get('category')  # Get the selected category
        recipe_image = request.FILES.get('recipe_image')

        Recipe.objects.create(
            user = request.user,
            recipe_image = recipe_image,
            recipe_name = recipe_name,
            recipe_ingridents = recipe_ingridents ,
            recipe_description = recipe_description,
            instructions = instructions,
            cooking_time = cooking_time,
            category=category,  # Store the selected category
        )
        return redirect('/addrecipe')
    return render(request,"addrecipe.html", {"CATEGORY_CHOICES": Recipe.CATEGORY_CHOICES})

def viewrecipe(request):
    queryset = Recipe.objects.order_by('-created_at')
    context = {'recipes': queryset, }
    return render(request,"view.html",context)

@login_required
def delete_recipe(request,id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete() 
    return redirect('/viewrecipe')

@login_required  
def update_recipe(request,id):
    queryset = Recipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_ingridents = data.get('recipe_ingridents')
        instructions = data.get('instructions')
        cooking_time = data.get('cooking_time')
        category = data.get('category')  # Get the selected category
        recipe_image = request.FILES.get('recipe_image')  

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        queryset.recipe_ingridents = recipe_ingridents
        queryset.instructions = instructions
        queryset.cooking_time  = cooking_time
        queryset.category=category  # Store the selected category

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('/viewrecipe/')
    context = {'recipe':queryset, "CATEGORY_CHOICES": Recipe.CATEGORY_CHOICES}
    return render(request,"update_recipe.html",context)

def recipe_detail(request,id):
    queryset = Recipe.objects.get(id=id)
    ingredients = queryset.recipe_ingridents.split('\n')
    instructions = queryset.instructions.split('.')

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Comment
            content = request.POST.get('content')
            if content:
                comment = Comment(user=request.user, recipe_name=queryset, content=content)
                comment.save()
        else:
            messages.error(request,'Please Login to Rate or Comment.')
        return redirect("recipe_detail",id=id)
    
    comments = Comment.objects.filter(recipe_name=queryset).order_by('-created_at')
    context = {
        'recipes': queryset,
        'ingredients':ingredients,
        'instructions':instructions,
        'comments': comments,
    }
    
    return render(request,"recipedetail.html",context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login_page')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login_page/')
        else:
            login(request,user)
            return redirect('/viewrecipe/')
        
    return render(request,"login_page.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username already exists')
            return redirect('/register')
        user = User.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   email=email,
                                   username=username)
        user.set_password(password)
        user.save()
        messages.success(request,'Account Created Successfully')
        return redirect('/register/')
    
    return render(request,"register.html")

@login_required
def log_out(request):
    logout(request)  # Logs out the user
    return redirect('/login_page')  # Redirects to the desired URL after logout (replace 'home' with the appropriate URL name)

# def search(request):
#     queryset = Recipe.objects.order_by('-created_at')
#     if request.GET.get('search'):
#         queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))
#     context = {'recipes': queryset}
#     return render(request,"search.html",context)


def bubble_sort(queryset):
    """
    Function to sort the queryset by the created_at field in descending order using the Bubble Sort algorithm.
    This will sort the queryset manually without using Django's built-in .order_by().
    """
    queryset_list = list(queryset)  # Convert queryset to a list for sorting
    
    n = len(queryset_list)
    
    # Perform bubble sort on the list of recipes
    for i in range(n):
        for j in range(0, n-i-1):
            # Compare the 'created_at' field of two adjacent elements
            if queryset_list[j].created_at < queryset_list[j+1].created_at:
                # Swap the elements if they are in the wrong order
                queryset_list[j], queryset_list[j+1] = queryset_list[j+1], queryset_list[j]
    
    return queryset_list  # Return the sorted list


def linear_search(query, queryset):
    """
    Performs a linear search for a query string within the queryset.
    Filters records where recipe_name contains the query string.
    """
    results = []
    for recipe in queryset:
        # Check if the search term (case-insensitive) is part of the recipe's name
        if query.lower() in recipe.recipe_name.lower():
            results.append(recipe)
    return results

def search(request):
    """
    View for searching and filtering recipes.
    Filters by cooking time, category, and/or search query.
    Sorts by recently added (created_at) first using Bubble Sort.
    """
    queryset = Recipe.objects.all()  # Get all recipes initially

    query = request.GET.get('search', '')  # Get the search query (optional)
    cooking_time_min = request.GET.get('cooking_time_min')  # Get the minimum cooking time filter
    cooking_time_max = request.GET.get('cooking_time_max')  # Get the maximum cooking time filter
    selected_category = request.GET.get('category')  # Get the selected category from the request

    # Step 1: Apply search filtering if there's a search query
    if query:
        queryset = linear_search(query, queryset)  # Use linear_search to filter by name (optional)

    # Step 2: Apply cooking time range filter if both min and max are provided
    if cooking_time_min and cooking_time_max:
        try:
            # Ensure cooking_time_min and cooking_time_max are integers
            cooking_time_min = int(cooking_time_min)
            cooking_time_max = int(cooking_time_max)

            # Filter recipes where cooking time is between the given min and max
            queryset = queryset.filter(cooking_time__gte=cooking_time_min, cooking_time__lte=cooking_time_max)
        except ValueError:
            queryset = queryset  # If the cooking time filters are invalid, return all results

    # Step 3: Apply category filter if a category is selected
    if selected_category:
        queryset = queryset.filter(category=selected_category)  # Filter by category

    # Step 4: Sort the queryset by created_at to get most recent recipes first using Bubble Sort
    queryset = bubble_sort(queryset)  # Custom Bubble Sort function for sorting by recently added

    # Pass the filtered and sorted queryset to the template
    context = {
        'recipes': queryset,  # This will be a queryset after filtering and sorting
        'search': query,  # Pass the search term
        'cooking_time_min': cooking_time_min,  # Pass the min cooking time to keep it in the URL
        'cooking_time_max': cooking_time_max,  # Pass the max cooking time to keep it in the URL
        'selected_category': selected_category,  # Pass the selected category to keep it in the URL
        "CATEGORY_CHOICES": Recipe.CATEGORY_CHOICES  # Pass category choices to the template
    }

    return render(request, "search.html", context)

@login_required
def profile(request,id):
    try:
        queryset = User.objects.get(id=id)
        user_recipes = Recipe.objects.filter(user=queryset)
        recipe_count = user_recipes.count()
        recipe = Recipe.objects.filter(user=queryset)
        userdetails = UserProfile.objects.get(user=queryset)
        context = {'user': queryset,'recipes': recipe,'userdetails':userdetails,'recipe_count':recipe_count}
        return render(request,"profile.html",context)
    except UserProfile.DoesNotExist:
        return redirect("/create_profile/")
    
def create_profile(request):
    queryset = User.objects.get(username = request.user.username)
    if request.method == 'POST':
        bio = request.POST.get('bio')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_pic')
        profile = UserProfile.objects.create(
            user = queryset,
            profile_pic = profile_pic,
            bio = bio,
            dob = dob,
        )
        messages.success(request,'Profile Created Successfully')
        profile.save()
        return redirect('profile',id=request.user.id)
    return render(request,"create_prrofile.html")

def update_profile(request,id):
    queryset = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        bio = data.get('bio')
        dob = data.get('dob')

        profile_pic = request.FILES.get('profile_pic')  
        queryset.dob = dob
        queryset.bio = bio
        if profile_pic:
            queryset.profile_pic = profile_pic
        queryset.save()
        print("User Id",request.user.id)
        return redirect('profile',id=request.user.id)
    context = {'userprofile':queryset}
    return render(request,"updateprofile.html",context)

# user profile -----

def user_profile(request, username):
    # Fetch the user based on the username
    user = get_object_or_404(User, username=username)
    # Optionally, you can pass additional data like the user's recipes
    recipes = user.recipe_set.all()  # Assuming a related Recipe model
    return render(request, 'user_profile.html', {'user': user, 'recipes': recipes})

# delete account
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Deletes the user from the database
        logout(request)  # Log the user out after account deletion
        return redirect('home')  # Redirect to the home page or another appropriate page

    return redirect('settings')  # In case someone accesses the view directly without POSTing
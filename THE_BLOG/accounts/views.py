from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.urls import reverse_lazy
from .models import CustomUser
from django.views import View
from django.views.generic import DetailView, ListView
from .forms import CustomUserCreationForm, CustomLoginForm

class SignupLoginView(View):
    template_name = "Login_signup.html"

    def get(self, request, *args, **kwargs):
        """Render the page with empty signup & login forms."""
        context = {
            "signup_form": CustomUserCreationForm(),
            "login_form": CustomLoginForm(),
            "signup_error": "",  # Initialize empty error message
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle both signup and login without redirection on errors."""
        if "signup" in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            login_form = CustomLoginForm()  # Keep an empty login form
            signup_error = "Signup was not successful!, please click the signup to check for errors"  # Default empty error message

            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect(reverse_lazy("Index"))  # Redirect only if successful

            else:
                signup_error = "Signup failed!. Please check the errors below."

            # Re-render the page with errors
            return render(
                request,
                self.template_name,
                {"signup_form": signup_form, "login_form": login_form, "signup_error": signup_error},
            )

        elif "login" in request.POST:
            login_form = CustomLoginForm(data=request.POST)
            signup_form = CustomUserCreationForm()  # Keep an empty signup form

            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect(reverse_lazy("PostViews", kwargs={
                        "slugs": user.slugs,
                        "category" :"Lifestyle"
                    }))  # Redirect only if successful
                login_form.add_error(None, "Invalid username or password")  # Show error without redirecting

            # Re-render the page with errors
            return render(
                request,
                self.template_name,
                {"signup_form": signup_form, "login_form": login_form, "signup_error": ""},
            )

        return self.get(request, *args, **kwargs)  # Default GET request

class UrlView(DetailView):
    model = "CustomUser"
    template_name="Authors_Post.html"
    context_object_name = "author"

    def get_object(self):
        user = self.kwargs.get("name")  # Get name from URL
        return CustomUser.objects.get(username__iexact=user)  # Fetch by Name


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse_lazy('signup_login'))




# class TestView(CreateView): # new
#  model = CustomUser
#  template_name = 'post_new.html'
#  fields = ['username','email', 'phone', 'password']
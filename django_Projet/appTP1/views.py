from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import JsonResponse

from django.http import JsonResponse

def AuthPage(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success_message': "Your account has been successfully created!"})
        else:
            # Return the errors in JSON format
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)  # Send a 400 status for invalid form
    else:
        form = CustomUserCreationForm()  # Display an empty form initially

    return render(request, "index.html", {"form": form})


from django.shortcuts import render


def AuthPage(request):
    return render(request, "index.html")


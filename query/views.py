from django.shortcuts import render, redirect
from .models import Query

def query_info(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        query_text = request.POST.get('query')

        Query.objects.create(
            name=name,
            email=email,
            query=query_text
        )

        return redirect('home')  # or index page url name

    return redirect('home')

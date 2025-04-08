from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def reviews_view(request):
    return render(request, 'eviews/eviews.html')

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings

@cache_page(settings.CACHE_SECONDS)
def dashboard(request):

    return render(request, 'dashboard.html', {
    })
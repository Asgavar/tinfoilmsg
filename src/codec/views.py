from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def encode(request):
    return render(request, 'encode.html')


@login_required
def decode(request):
    return render(request, 'decode.html')

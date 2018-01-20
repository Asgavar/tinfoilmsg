from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('glowna')


def encode(request):
    return HttpResponse('encode')


def decode(request):
    return HttpResponse('decode')

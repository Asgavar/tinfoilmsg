from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AlgorithmForm
from .models import Algorithm


@login_required
def encode(request):
    return render(request, 'encode.html')


@login_required
def decode(request):
    return render(request, 'decode.html')


@login_required
def my_algorithms(request):
    current_user = request.user
    to_show_list = Algorithm.objects.filter(
        Q(sender__id=current_user.id) | Q(receiver__id=current_user.id)
    )
    return render(request, 'my_algorithms.html', {'to_show_list': to_show_list})


@login_required
def algorithm_configuration(request):
    if request.method == 'POST':
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/my_algorithms')
    form = AlgorithmForm()
    return render(request, 'algorithm_configuration.html', {'form': form})

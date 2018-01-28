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
    """
    Displays a list made of algorithms in which the user is involved.
    """
    current_user = request.user
    to_show_list = Algorithm.objects.filter(
        Q(sender__id=current_user.id) | Q(receiver__id=current_user.id)
    )
    return render(request, 'my_algorithms.html', {'to_show_list': to_show_list})


@login_required
def algorithm_configuration(request, id=None):
    """
    Displays and receives a form which creates or modifies an algorithm,
    depending on whether the algorithm_id was passed in or not.
    """
    if request.method == 'POST':
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            new_algorithm = form.save(commit=False)
            new_algorithm.sender = request.user
            new_algorithm.save()
            return HttpResponseRedirect('/my_algorithms')
    form = AlgorithmForm()
    return render(request, 'algorithm_configuration.html', {'form': form})

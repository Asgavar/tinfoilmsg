from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AlgorithmForm
from .forms import DecodeForm
from .forms import EncodeForm
from .models import Algorithm


@login_required
def encode(request):
    where_user_is_sender = Algorithm.objects.filter(sender=request.user)
    receiver_ids = [algo.receiver.id for algo in where_user_is_sender]
    available_rec = User.objects.filter(id__in=receiver_ids)
    return render(request, 'encode.html', {'form': EncodeForm(available_rec)})


@login_required
def decode(request):
    return render(request, 'decode.html', {'form': DecodeForm()})


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
def algorithm_configuration(request):
    """
    Displays and receives a form which creates or modifies an algorithm,
    depending on whether the algorithm_id was passed in or not.
    """
    if request.method == 'POST':
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            # TODO: show a message after validation failure
            new_algorithm = form.save(commit=False)
            new_algorithm.sender = request.user
            new_algorithm.save()
            return HttpResponseRedirect('/my_algorithms')
    # sender field is set twice since it's needed for validation
    form = AlgorithmForm(initial={'sender': request.user})
    return render(request, 'algorithm_configuration.html', {'form': form})


@login_required
def algorithm_delete(request, algo_id):
    if request.method == 'POST':
        if 'yesiam' in request.POST:
            Algorithm.objects.get(id=algo_id).delete()
            return HttpResponseRedirect('/my_algorithms')
    victim = Algorithm.objects.get(id=algo_id)
    return render(request, 'algorithm_delete.html', {'victim': victim})

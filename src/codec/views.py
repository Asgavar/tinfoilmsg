import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AlgorithmForm
from .forms import DecodeForm
from .forms import EncodeForm
from .models import Algorithm

from tinfoilmsg import settings

import libstegan


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


@login_required
def encode_results(request):
    if request.method == 'POST':
        message = request.POST['message_text']
        receiver = request.POST['message_receiver']
        algo_query = Q(sender=request.user) & Q(receiver=receiver)
        algorithm = Algorithm.objects.get(algo_query)
        libstegan_conf = {
            'red': algorithm.red,
            'green': algorithm.green,
            'blue': algorithm.blue,
            'frequency': algorithm.frequency
        }
        generated_image = libstegan.encode(libstegan_conf, message)
        # 13 randomly choiced letters form a file name
        filename = settings.TINFOILMSG_TMP_DIR
        filename += ''.join(random.sample(string.ascii_letters, 13))
        filename += '.bmp'
        with open(filename, 'w+b') as physical_file:
            generated_image.save(physical_file, format='BMP')
    img_link = filename.replace(settings.TINFOILMSG_TMP_DIR, '')
    return render(request, 'encode_results.html', {'image': img_link})


@login_required
def decode_results(request):
    pass

import os

from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_H

from django.conf import settings
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Tree


JSONP_CALLBACK_PARAM = 'callback'


def index(request):
    latest_updated_trees = Tree.objects.order_by('-updated')[:25]
    context = {'latest_updated_trees': latest_updated_trees}
    return render(request, 'trees/index.html', context)


def index_json(request):
    trees = Tree.objects.all()
    data = serialize('json', trees, fields=None)
    if JSONP_CALLBACK_PARAM in request.GET:
        data = f'{request.GET[JSONP_CALLBACK_PARAM]}({data})'
        return HttpResponse(data, content_type='text/javascript')
    else:
        return HttpResponse(data, content_type='application/json')


def detail(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)
    return render(request, 'trees/detail.html', {'tree': tree})


def qrcode(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)

    # Temporarily hard-code domain name
    # absolute_uri = request.build_absolute_uri(reverse('trees:detail', args=[tree.id]))
    absolute_uri = f"https://treedb.org{reverse('trees:detail', args=[tree.id])}"

    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(absolute_uri)
    qr.make(fit=True)
    image = qr.make_image(fill_color='green', back_color='white').convert('RGB')

    static_dir = f'trees/{tree.id}'
    full_static_dir = f'{settings.BASE_DIR}/trees/static/{static_dir}'

    static_path = f'{static_dir}/qr.png'
    full_path = f'{settings.BASE_DIR}/trees/static/{static_path}'

    print(f'Saving to {full_path}')
    os.makedirs(full_static_dir, exist_ok=True)
    image.save(full_path)

    return render(request, 'trees/qrcode.html', {'static_path': static_path})

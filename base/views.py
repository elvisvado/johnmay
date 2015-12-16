import json
from django.http.response import HttpResponse
from .models import *
from django.core import serializers


def datos_cliente(request):
    obj = Cliente()
    try:
        obj = Cliente.objects.get(id=request.GET.get('id', ''))
    except:
        pass
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')

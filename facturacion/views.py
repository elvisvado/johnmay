from django.http.response import HttpResponse
import json
from django.core import serializers
from base.models import Documento as Factura, TipoPago, TipoDoc, Cliente, \
Producto, Detalle, Bodega
from base.base import base_cliente
from base.api import get_cliente
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


def factura():
    return TipoDoc.objects.get(name="FACTURA")


def tipopagos():
    return TipoPago.objects.all()


def grabar_factura(request):
    c = base_cliente()
    c.cliente_codigo = request.POST.get("cliente_code", "")
    c.cliente_nombre = request.POST.get("cliente_nombre", "")
    c.cliente_identificacion = request.POST.get("cliente_identificacion", "")
    c.cliente_email = request.POST.get("cliente_email", "")
    c.cliente_telefono = request.POST.get("cliente_telefono", "")
    c.cliente_direccion = request.POST.get("cliente_direccion", "")

    f = Factura()
    f.fecha = datetime.now()
    f.user = request.user
    f.sucursal = request.user.sucursal
    f.tipodoc = factura()

    f.vendedor = request.user
    f.tipopago = TipoPago.objects.get(id=request.POST.get("factura_tipopago", ""))
    f.comentarios = request.POST.get("factura_comentarios", "")
    f.cliente = get_cliente(c)

    f.subtotal = float(request.POST.get("factura_subtotal", "0.0"))
    f.descuento = float(request.POST.get("factura_descuento", "0.0"))
    f.iva = float(request.POST.get("factura_iva", "0.0"))
    f.total = float(request.POST.get("factura_total", "0.0"))
    f.costo = float(request.POST.get("factura_costo", "0.0"))
    f.factor = (f.subtotal - f.descuento) / f.costo
    f.utilidad = (f.subtotal - f.descuento) - f.costo
    f.aplicado = False

    f.save()
    #f.aplicar()
    #f.calcular()
    return f


def grabar_detalle(request, factura):
    t = len(request.POST.getlist('producto_codigo', ''))
    d = Factura()
    data = []
    for i in range(0, t):
        dd = Detalle()
        p = Producto.objects.get(code=request.POST.getlist('producto_codigo', '')[i])
        b = Bodega.objects.get(id=int(request.POST.getlist('bodega', '')[i]))
        e = p.existencias().filter(bodega=b)[0]
        dd.documento = factura
        dd.producto = p
        dd.producto_cantidad = float(request.POST.getlist('producto_cantidad', '')[i])
        dd.producto_precio_unitario = float(request.POST.getlist('producto_precio', '')[i])
        dd.producto_descuento_unitario = float(request.POST.getlist('producto_descuento', '')[i])
        dd.bodega = b
        dd.producto_costo_unitario = p.costo
        dd.producto_existencia = float(e.existencia_disponible)
        dd.producto_saldo = dd.producto_existencia - dd.producto_cantidad
        e.existencia_disponible = dd.producto_saldo
        dd.producto_costo_promedio = p.costo
        dd.precio_total = dd.producto_cantidad * dd.producto_precio_unitario
        dd.costo_total = dd.producto_cantidad * dd.producto_costo_unitario
        dd.descuento_total = dd.producto_cantidad * dd.producto_descuento_unitario
        dd.utilidad = (dd.precio_total - dd.descuento_total) - dd.costo_total
        dd.factor = round((dd.precio_total - dd.descuento_total) / dd.costo_total, 2)

        dd.save()
        e.save()
        data.append(dd)
    return data


def validar(request):
    data = {'mensajes': [], 'resoult': True}
    if len(request.POST.getlist('producto_codigo', '')) == 0:
        data['mensajes'].append(("no se puede grabar una factura sin productos",
            "danger"))
        data['resoult'] = False
    if request.POST.get('cliente_nombre', '') == '':
        data['mensajes'].append(("el nombre del cliente es obligatorio",
            "danger"))
        data['resoult'] = False
    return data


@login_required(login_url='/admin/login/')
def facturacion(request):
    validacion = validar(request)
    context = RequestContext(request)
    data = {'tipopagos': tipopagos(), 'mensajes': []}
    template_name = "factura.html"
    if request.method == "POST":
        if validacion['resoult']:
            data['factura'] = grabar_factura(request)
            data['detalle'] = grabar_detalle(request, data['factura'])
        else:
            data['mensajes'] = validacion['mensajes']
    return render_to_response(template_name, data, context_instance=context)


def autocomplete_entidad(instance, request):
    if request.is_ajax:
        model = type(instance)
        result = []
        term = request.GET.get('term', None)
        code = request.GET.get('code', None)
        if term:
            qs = model.objects.filter(
                Q(code__istartswith=term) |
                Q(name__icontains=term)
                )
            for obj in qs:
                obj_json = {}
                obj_json['label'] = obj.name
                obj_json['value'] = obj.name
                obj_json['obj'] = model_to_dict(obj)
                result.append(obj_json)
        if code:
            obj = model.objects.get(code=code)
            obj_json = {}
            obj_json['label'] = obj.name
            obj_json['value'] = obj.name
            obj_json['obj'] = model_to_dict(obj)
            result.append(obj_json)
        data = json.dumps(result)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')


def instance_to_json(instance, request):
    obj = type(instance)
    try:
        obj = obj.objects.get(id=request.GET.get('id', ''))
    except:
        pass
    data = serializers.serialize('json', [obj, ])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def autocomplete_cliente(request):
    return autocomplete_entidad(Cliente(), request)


def autocomplete_producto(request):
    return autocomplete_entidad(Producto(), request)


def datos_cliente(request):
    return instance_to_json(Cliente(), request)


def datos_producto(request):
    return instance_to_json(Producto(), request)


@csrf_exempt
def existencias_producto(request):
    p = None
    existencias = []
    try:
        p = Producto.objects.get(code=request.POST.get('code', ''))
    except:
        pass
    if p:
        if p.existencias():
            for e in p.existencias():
                obj_json = {}
                obj_json['bodega_id'] = e.bodega.id
                obj_json['bodega_nombre'] = e.bodega.name
                obj_json['existencia'] = e.existencia_disponible
                existencias.append(obj_json)
    data = json.dumps(existencias)
    return HttpResponse(data, content_type='application/json')

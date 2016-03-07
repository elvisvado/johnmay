# -*- coding: utf-8 -*-
from .models import *
from .models import Detalle


def get_media_url(model, filename):
    clase = model.__class__.__name__
    code = str(model.id)
    return '%s/%s/%s' % (clase, code, filename)


def get_by_code(instance, code):
    model = type(instance)
    try:
        return model.objects.get(code=code)
    except:
        return instance


def get_by_name(instance, name):
    model = type(instance)
    try:
        return model.objects.get(name=name)
    except:
        return instance


def get_or_create_entidad(instance, name):
    model = type(instance)
    o, created = model.objects.get_or_create(name=name)
    o.save()
    return o


def get_factor(subtotal, descuento, costo):
    try:
        return round((subtotal - descuento) / costo, 1)
    except:
        return 0.0


def get_utilidad(subtotal, descuento, costo):
    try:
        return round(subtotal - (descuento + costo), 2)
    except:
        return 0.0


def totalizar(a, b):
    try:
        return round(a * b, 2)
    except:
        return 0.0


def devolver_mayor(a, b):
    if a and not b:
        return a
    else:
        return b
    if a > b:
        return a
    else:
        return b


def get_producto(obj):
    """
    obj is a instance of base_producto
    """
    p, created = Producto.objects.get_or_create(code=obj.producto_codigo)
    p.name = obj.producto_nombre
    if not p.marca:
        p.marca = get_or_create_entidad(Marca(), obj.producto_marca)
    if not p.categoria:
        p.categoria = get_or_create_entidad(Categoria(),
            obj.producto_categoria)
    p.precio = obj.producto_precio
    p.costo = obj.producto_costo
    p.save()
    return p


def get_cliente(obj):
    """
    obj is a instance of base_cliente
    """
    c = None
    if obj.cliente_codigo and obj.cliente_codigo != '':
        c, created = Cliente.objects.get_or_create(code=obj.cliente_codigo)
    else:
        try:
            c = Cliente.objects.filter(name=obj.cliente_nombre)[0]
        except:
            c, created = Cliente.objects.get_or_create(
                name=self.cliente_nombre)
    c.name = devolver_mayor(c.name, obj.cliente_nombre)
    c.identificacion = devolver_mayor(c.identificacion,
        obj.cliente_identificacion)
    c.telefono = devolver_mayor(c.telefono, obj.cliente_telefono)
    c.email = devolver_mayor(c.email, obj.cliente_email)
    c.direccion = devolver_mayor(c.direccion, obj.cliente_direccion)
    c.save()
    return c


def get_user(username):
    try:
        return User.objects.get(username=username)
    except:
        u, created = User.objects.get_or_create(
            username=username, password="12345")
        return u


def get_documento(obj):
    """
    obj is a instance of base_documento
    """
    tipodoc, created = TipoDoc.objects.get_or_create(name=obj.documento_tipo,
        afectacion=obj.get_afectacion())
    sucursal = get_or_create_entidad(Sucursal(), obj.documento_sucursal)
    d, created = Documento.objects.get_or_create(tipodoc=tipodoc,
        sucursal=sucursal, numero=obj.documento_numero,
        fecha=obj.documento_fecha, user=get_user(obj.documento_usuario))
    if obj.cliente_nombre:
        d.cliente = get_cliente(obj)
    if obj.documento_pago:
        d.tipopago = get_or_create_entidad(TipoPago(), obj.documento_pago)
    d.save()
    return d


def get_detalle(obj):
    dd = Detalle()
    dd.documento = get_documento(obj)
    dd.bodega = get_or_create_entidad(Bodega(),
        name=obj.documento_bodega)
    dd.sucursal = get_or_create_entidad(Sucursal(), obj.documento_sucursal)
    dd.producto = get_producto(obj)
    dd.producto_cantidad = obj.producto_cantidad
    dd.producto_precio_unitario = obj.producto_precio
    dd.producto_descuento_unitario = obj.producto_descuento
    dd.producto_costo_unitario = obj.producto_costo
    dd.save()
    return dd


/*
factura.js
funciones
    completar datos del cliente *
    completar info del producto *

    calcular factura
        calcular subtotal
        calcular descuento
        calcular iva
        calcular ir
        calcular al
        calcular total

    buscar existencias en bodega
*/

var complete_cliente = function(){
    var _self = $(this);
    $(_self).autocomplete({
        minLength: 2,
        source: "/facturacion/buscar_cliente",
        select: function( event, ui ) {
                $('#id_cliente_code').val(ui.item.obj.code);
                $('#id_cliente_id').val(ui.item.obj.id);
                $('#id_cliente_nombre').val(ui.item.obj.name);
                $('#id_cliente_identificacion').val(ui.item.obj.identificacion);
                $('#id_cliente_telefono').val(ui.item.obj.telefono);
                $('#id_cliente_email').val(ui.item.obj.email);
                $('#id_cliente_direccion').val(ui.item.obj.direccion);
        }
    });
}

var create_row = function(obj){
    var row = $('<tr class="detalle"></tr>').data('producto', JSON.stringify(obj));
    row.attr('id', obj.id);
    row.append($('<td><input type="input" id="id_producto_codigo" class="form-control" readonly name="producto_codigo" value="' + obj.code + '"></td>'));
    row.append($('<td><input type="input" id="id_producto_nombre" class="form-control" readonly name="producto_nombre" value="'+obj.name+'"></td>'));
    row.append($('<td><input type="input" id="id_producto_cantidad" class="form-control" readonly name="producto_cantidad" value="1"></td>'));
    row.append($('<td><input type="input" id="id_producto_precio" class="form-control" readonly name="producto_precio" value="'+obj.precio+'"></td>'));
    row.append($('<td><input type="input" id="id_producto_descuento" class="form-control" readonly name="producto_descuento" value="0"></td>'));
    row.append($('<td><input type="input" id="id_total" class="form-control" readonly name="producto_total" value="'+obj.precio+'"></td>'));
    var oculta = $('<td></td>');
    oculta.append($('<input type="hidden" id="producto_id" name="producto"></input>'));
    oculta.append($('<input type="hidden" id="bodega_id" name="bodega"></input>'));
    row.append(oculta);
    $('#productos tbody').append(row);
    return row;
}

var load_existencias = function (obj){
    $.ajax("/facturacion/existencias_producto/", {
        type: 'POST',
        data: {'code': obj.code},
        success: function(data){
            var exist = $("#exitencia>tbody");
            exist.empty();
            $.each(data, function(i, o){
                var row = $('<tr></tr>').data('pk', o.bodega_id);
                row.append($('<td></td>').html(o.bodega_nombre));
                row.append($('<td></td>').html(o.existencia));
                exist.append(row);
            });
            $('#modal_bodega').val(undefined);
            $('#modal_cantidad').val(1);
        }
    });
}

var load_modal = function(row){
    var obj = JSON.parse($(row).data('producto'));
    $('#myModal').data('producto', $(row).data('producto'));
    $('#modal_codigo').val(obj.code);
    $('#modal_descripcion').val(obj.name);
    $('#modal_precio_pop').val(obj.precio);
    $('#modal_precio_1').val(row.find('#id_producto_precio').val());
    load_existencias(obj);
    $('#myModal').modal('show');
    try {
        if(parseFloat($(fila).find('#producto_precio').val()) == 0){
            $('#modal_precio_1').val(
                parseFloat($(fila).find('#producto_precio').val()));
        }
    }
    catch (e) {
       console.log(e);
    }

    return row
}

var complete_producto = function () {
    var _self = $(this);
    if($.trim($(_self).val()) != '') {
        $(_self).autocomplete({
            minLength: 2,
            source: "/facturacion/buscar_producto",
            select: function(i, o) {
                var row = create_row(o.item.obj);
                load_modal(row);
            }
        });
    }
}

var save_fila = function (){
    var modal = $('#myModal');
    var obj = JSON.parse(modal.data('producto'));
    var row = $('#'+obj.id);
    row.find('#id_producto_precio').val($('#modal_precio_1').val());
    row.find('#id_producto_cantidad').val($('#modal_cantidad').val());
    row.find('#id_producto_descuento').val($('#modal_descuento_1').val());
    modal.modal('hide');
}

var update_fila = function(){
    load_modal($(this));
}


 $("#exitencia").on("click", "td", function() {
            $("#exitencia>tbody>tr").removeClass("selected");
            $( this ).parent().addClass("selected");
            var bodega = $(this).parent().attr("row");
            var existencia = $(this).parent().find('#existencia_existencia').html();
            document.getElementById("modal_bodega").value = bodega;
            document.getElementById("modal_existencia").value = existencia;
        });

$(document).on('ready', function(){
    $('#id_cliente_nombre').on('keyup', complete_cliente);
    $('#id_buscador_productos').on('keyup', complete_producto);
    $('#productos tbody').on('dblclick', '.detalle', update_fila);
    $('#modal_ok').on('click', save_fila);
});

/*
factura.js
funciones
    completar datos del cliente
    completar info del producto

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





function quitar(){
    $("#productos tr:last").remove();
    calcular();
    }

function totalFilas(){
    return $('.fila').length;
    }

function producto_bodega(codigo){
    $.ajax("/facturacion/existencias_producto/", {
        type: 'POST',
        data: codigo,
        success: function(data){
            $("#exitencia>tbody").empty()
            for (var i = 0; i < data.length; i++){
                var row = '<tr row='+ data[i].bodega_id +'>';
                row += '<td id="existencia_bodega">' + data[i].bodega_nombre + '</td>';
                row += '<td id="existencia_existencia">' + data[i].existencia + '</td>';
                row += '</tr>';
                $("#exitencia>tbody").append(row);
                }
            $('#modal_bodega').val('None');
            $('#modal_cantidad').val('1');
            }
        });
    }

function calcular() {
    var Subtotal = 0;
    var Descuento = 0;
    var Iva = 0;
    var Retencion = 0;
    var Total = 0;

    $('#productos>tbody tr').each(function(){
        $this = $(this);
        var cantidad = $(this).find("#id_producto_cantidad").val();
        var precio = $(this).find("#id_producto_precio").val();
        var descuento = $(this).find("#id_producto_descuento").val();
        $(this).find("#id_total").val(((precio * cantidad) - (descuento * cantidad)).toFixed(2));
        Subtotal += cantidad * precio;
        Descuento += cantidad * descuento;
    });

    if($('#id_excento').is(':checked')) {
        Iva = 0;
    } else {
        Iva = (Subtotal - Descuento) * 0.15;
    }
    if($('#id_ir').is(':checked')) {
        Retencion += (Subtotal - Descuento) * 0.02;
    }
    if($('#id_al').is(':checked')) {
        Retencion += (Subtotal - Descuento) * 0.01;
    }

    Total = (Subtotal - Descuento) + Iva - Retencion;
    $("#id_factura_subtotal").val(Subtotal.toFixed(2));
    $("#id_factura_descuento").val(Descuento.toFixed(2));
    $("#id_factura_iva").val(Iva.toFixed(2));
    $("#id_factura_retencion").val(Retencion.toFixed(2));
    $("#id_factura_total").val(Total.toFixed(2));
    }

function add_detail_product() {
    $('#msg').empty().append('<span class="alert-danger"></span>');

    var prod = $('#modal_id').val();
    var bod = $('#modal_bodega').val();
    var prods = $('#producto_id[value='+prod+']');

    if (prods.length > 0) {
        $.each(prods, function(i, obj){
            alert("este producto ya esta en la factura");
        });
    } else {
        var row = '<tr class="fila" number="' + totalFilas() + '">';
        row += '<td><input type="input" id="id_producto_codigo" class="form-control" value="' + $('#modal_codigo').val() + '" readonly name="producto_codigo"></td>';
        row += '<td><input type="input" id="id_producto_nombre" class="form-control" value="' + $('#modal_descripcion').val() + '" readonly name="producto_nombre"></td>';
        row += '<td><input type="input" id="id_producto_cantidad" class="form-control" value=' + $('#modal_cantidad').val() + ' onchange="calcular()" readonly name="producto_cantidad"></td>';
        row += '<td><input type="input" id="id_producto_precio" class="form-control" value="' + $('#modal_precio_1').val() + '" onchange="calcular()" readonly name="producto_precio"></td >';
        row += '<td><input type="input" id="id_producto_descuento" class="form-control" value="' + $('#modal_descuento_1').val() + '" onchange="calcular()" readonly name="producto_descuento"></td>';
        row += '<td><input type="input" id="id_total" class="form-control" value="' + $('#modal_precio').val() + '" onchange="calcular()" readonly name="producto_total"></td>'
        row += '<td>';
        row += '<input type="hidden" id="producto_id" value=' + $('#modal_id').val() + ' name="producto" data-precio="'+ $('#myModal').data('precio') +'"></input>';
        row += '<input type="hidden" id="bodega_id" value=' + $('#modal_bodega').val() + ' name="bodega"></input>';
        row += '</td>';
        row += '</tr>';
        $('#productos tbody').append(row);
    }
    }

function validar_modal(){
    var bodega = $('#modal_bodega').val();
    var existencia = $('#modal_existencia').val();
    var cantidad = $('#modal_cantidad').val();
    var precio = $('#modal_precio_1').val();
    var descuento = $('#modal_descuento_1').val();

    if (bodega == "None"){
        $('#msg').empty().append('<span class="alert-danger">Por favor seleccione una bodega...</span>');
    } else if (cantidad > existencia) {
        $('#msg').empty().append('<span class="alert-danger">La cantidad no puede ser mayor que la existencia</span>');
    } else {
        $("#myModal").modal('hide');
    if ($("#myModal").data('number')!= undefined){
        var num = $("#myModal").data('number');
        var fil = $("#productos tbody").find("tr[number=" + num +"]");

        fil.find('#id_producto_cantidad').val(cantidad);
        fil.find('#id_producto_precio').val(precio);
        fil.find('#id_producto_descuento').val(descuento);

        $("#myModal").data('number', undefined);
    } else {
        add_detail_product();
    }

    calcular();

    }
}
/*Buscar los datos del Item seleccionado en la Grilla*/
var buscar_prod = function () {
    var _self = $(this);
    if($.trim($(_self).val()) != '') {
        $(_self).autocomplete({
            minLength: 2,
            source: "/facturacion/buscar_producto",
            select: function(event, ui) {
                $('#modal_id').val(ui.item.obj.id);
                $('#modal_codigo').val(ui.item.obj.code);
                $('#modal_descripcion').val(ui.item.obj.name);
                $('#modal_precio').val(ui.item.obj.precio);
                $('#modal_precio_pop').val(ui.item.obj.precio);
                $('#modal_precio_1').val(ui.item.obj.precio);
            }
        });
    }
}

$(document).on('ready', function(){
    $('#id_ir').change(function() {
        calcular();
    });

    $('#id_al').change(function() {
        calcular();
    });

    $('#id_excento').change(function() {
        calcular();
    });

    $('#modal_cantidad').focus(function() {
        $(this).select();
    });



    $("#exitencia").on("click", "td", function() {
        $("#exitencia>tbody>tr").removeClass("selected");
        $( this ).parent().addClass("selected");
        var bodega = $(this).parent().attr("row");
        var existencia = $(this).parent().find('#existencia_existencia').html();
        document.getElementById("modal_bodega").value = bodega;
        document.getElementById("modal_existencia").value = existencia;
    });

    $('#id_buscador_productos').autocomplete({
        minLength: 2,
        source: "/facturacion/buscar_producto",
        select: function( event, ui ) {
            var codigo = ui.item.obj.code;

            $('#modal_id').val(ui.item.obj.id);
            $('#modal_codigo').val(ui.item.obj.code);
            $('#modal_descripcion').val(ui.item.obj.name);
            $('#modal_precio').val(ui.item.obj.precio);
            $('#modal_precio_pop').val(ui.item.obj.precio);
            $('#modal_precio_1').val(ui.item.obj.precio);

            producto_bodega({
                code: codigo,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            });

            $("#myModal").modal('show');
        }
    });
    /*Buscar detalles del producto desde la grilla en el Evento Double Click*/
    $('#productos tbody').on('dblclick', '.fila', function(e){
        var codigo = $(this).find('#id_producto_codigo').val();
        e.stopPropagation();

        $("#modal_cantidad").val($(this).find('#id_producto_cantidad').val());
        $("#modal_descuento_1").val($(this).find('#id_producto_descuento').val());
        $("#modal_precio_1").val($(this).find('#id_producto_precio').val());
        $('#msg').empty().append('<span class="alert-danger"></span>');

        producto_bodega({
            code: codigo,
            buscar_prod()
        });

        $("#myModal")
        .data('number', $(this).attr('number'))
        .modal('show');
    });

});
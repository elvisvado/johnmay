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
    row.data('nuevo', true);
    row.attr('id', obj.id);
    row.append($('<td><input type="input" id="id_producto_codigo" class="form-control" readonly name="producto_codigo" value="' + obj.code + '"></td>'));
    row.append($('<td><input type="input" id="id_producto_nombre" class="form-control" readonly name="producto_nombre" value="'+obj.name+'"></td>'));
    row.append($('<td><input type="input" id="id_producto_bodega" class="form-control" readonly name="producto_bodega" value="0"></td>'));
    row.append($('<td><input type="input" id="id_producto_cantidad" class="form-control" readonly name="producto_cantidad" value="1"></td>'));
    row.append($('<td><input type="input" id="id_producto_costo" class="form-control" readonly name="producto_costo" value="'+obj.costo+'"></td>'));
    row.append($('<td><input type="input" id="id_producto_precio" class="form-control" readonly name="producto_precio" value="'+obj.precio+'"></td>'));
    row.append($('<td><input type="input" id="id_producto_descuento" class="form-control" readonly name="producto_descuento" value="0"></td>'));
    row.append($('<td><input type="input" id="id_total" class="form-control" readonly name="producto_total" value="'+obj.precio+'"></td>'));
    var oculta = $('<td></td>');
    oculta.append($('<input type="hidden" id="bodega_id" name="bodega"></input>'));
    row.append(oculta);
    //$('#productos tbody').append(row);
    return row;
}
var complete_producto = function () {
    var _self = $(this);
    if($.trim($(_self).val()) != '') {
        $(_self).autocomplete({
            minLength: 2,
            source: "/facturacion/buscar_producto",
            select: function(i, o) {
                var row = create_row(o.item.obj);
                var obj = JSON.parse($(row).data('producto'));

                if (vericar_duplicado(row) == false) {
                  $('#productos tbody').append(row);
                  load_modal(row);
                }
            }
        });
    }
}
var vericar_duplicado = function(row){
    var codigo = $(row).find('#id_producto_codigo').val();
    var id = $(row).attr('id');
    var result = false;

    $("#productos tbody tr").each(function(){
      if($(this).attr('id') == id && codigo == $(this).find('#id_producto_codigo').val()) {
        result = true;
        }
        else {
          result = false;
          }
    })
    return result;
}
var load_modal = function(row){
    var obj = JSON.parse($(row).data('producto'));
    $('#myModal').data('producto', $(row).data('producto'));
    $('#myModal').data('nuevo', $(row).data('nuevo'));
    $('#modal_bodega').val(row.find('#bodega_id').val());
    $('#modal_codigo').val(obj.code);
    $('#modal_descripcion').val(obj.name);
    $('#modal_precio_pop').val(obj.precio);
    $('#modal_precio_1').val(row.find('#id_producto_precio').val());
    $('#modal_cantidad').val(row.find('#id_producto_cantidad').val());
    $('#modal_descuento_1').val(row.find('#id_producto_descuento').val());
    var bodega_id = $(row).find('#bodega_id').val();

    $('#msg').empty().append('<span class="alert-danger"></span>');
    load_existencias(obj, bodega_id);
    $('#myModal').modal('show');

    try {
        if(parseFloat($(row).find('#producto_precio').val()) == 0){
            $('#modal_precio_1').val(
                parseFloat($(row).find('#producto_precio').val()));
        }
    }
    catch (e) {
       console.log(e);
    }

    return row
}
var load_existencias = function (obj, bodega_id){
    $.ajax("/facturacion/existencias_producto/", {
        type: 'POST',
        data: {'code': obj.code},
        success: function(data){
            var exist = $("#exitencia>tbody");
            exist.empty();
            $.each(data, function(i, o){
                if (bodega_id == o.bodega_id){
                  var row = $('<tr class="selected"></tr>')
                } else {
                  var row = $('<tr></tr>')
                }
                row.data('pk', o.bodega_id);
                row.append($('<td id="bodega_bodega"></td>').html(o.bodega_nombre));
                row.append($('<td id="bodega_existencia"></td>').html(o.existencia));
                exist.append(row);
            });
        }
    });
}
var save_fila = function (){
    var modal = $('#myModal');
    var obj = JSON.parse(modal.data('producto'));
    var row = $('#'+obj.id);
    row.find('#bodega_id').val($('#modal_bodega').val());
    row.find('#id_producto_bodega').val($('#exitencia tbody').find('.selected #bodega_bodega').html());
    row.find('#id_producto_precio').val($('#modal_precio_1').val());
    row.find('#id_producto_cantidad').val($('#modal_cantidad').val());
    row.find('#id_producto_descuento').val($('#modal_descuento_1').val());
    row.data('nuevo', false);
    modal.modal('hide');
    calcular_factura();
}
var update_fila = function(){
    load_modal($(this));
}
var selected_fila = function(){
  $("#exitencia>tbody>tr").removeClass("selected");
  $(this).addClass("selected");
  $('#modal_bodega').val($(this).data('pk'));
}
var validar_modal = function(){
  var bodega = $('#modal_bodega').val();
  var existencia = parseFloat($('#exitencia tbody').find('.selected #bodega_existencia').html());
  var cantidad = parseFloat($('#modal_cantidad').val());
  var precio = parseFloat($('#modal_precio_1').val());
  var descuento = parseFloat($('#modal_descuento_1').val());

  if (bodega == ""){
    $('#msg').empty().append('<span class="alert-danger">Por favor seleccione una bodega...</span>');
  } else if (cantidad > existencia) {
    $('#msg').empty().append('<span class="alert-danger">La cantidad no puede ser mayor que la existencia</span>');
  } else {
    save_fila();
  }
}
var calcular_factura = function(){
  var Subtotal = 0;
  var Descuento = 0;
  var Iva = 0;
  var Retencion = 0;
  var Total = 0;
  var Costo = 0;

  $('#productos>tbody tr').each(function(){
      $this = $(this);
      var cantidad = $(this).find("#id_producto_cantidad").val();
      var precio = $(this).find("#id_producto_precio").val();
      var descuento = parseFloat($(this).find("#id_producto_descuento").val());
      var costo = parseFloat($(this).find("#id_producto_costo").val());
      var total_descuento = (cantidad*precio)-(cantidad*descuento);

      $(this).find("#id_total").val(total_descuento.toFixed(2));

      Subtotal += cantidad * precio;
      Descuento += cantidad * descuento;
      Costo += cantidad * costo;
  });

  $('#id_factura_ir').val('0.0');
  $('#id_factura_al').val('0.0');
  if($('#id_excento').is(':checked')) {
      Iva = 0;
  } else {
      Iva = (Subtotal - Descuento) * 0.15;
  }
  if($('#id_ir').is(':checked')) {
    if((Subtotal - Descuento) > 1000){
      Retencion += (Subtotal - Descuento) * 0.02;
      $('#id_factura_ir').val((Subtotal - Descuento) * 0.02);
    }
  }
  if($('#id_al').is(':checked')) {
    if((Subtotal - Descuento) > 1000){
      Retencion += (Subtotal - Descuento) * 0.01;
      $('#id_factura_al').val((Subtotal - Descuento) * 0.01);
    }
  }

  Total = (Subtotal - Descuento) + Iva - Retencion;
  $("#id_factura_subtotal").val(Subtotal.toFixed(2));
  $("#id_factura_descuento").val(Descuento.toFixed(2));
  $("#id_factura_iva").val(Iva.toFixed(2));
  $("#id_factura_retencion").val(Retencion.toFixed(2));
  $("#id_factura_total").val(Total.toFixed(2));
  $("#id_factura_costo").val(Costo.toFixed(2));
  }
var quitar_fila = function(){
  var modal = $('#myModal');
  var obj = JSON.parse(modal.data('producto'));
  var row = $('#'+obj.id);
  if(row.data('nuevo')){
    row.remove();
  }
    calcular_factura();
  }
var eliminar_producto = function() {
  var modal = $('#myModal');
  var obj = JSON.parse(modal.data('producto'));
  var row = $('#'+obj.id);
  modal.modal('hide');
  row.remove();
    calcular_factura();
}
var get_descuento = function(){
  /*event.defaultPrevented();*/
  if($(this).val().match(/(?:%)$/)){
    var percent = parseFloat($(this).val().replace('%','')) / 100;
    $(this).val((parseFloat($('#modal_precio_1').val()) * percent).toFixed(2));
  }
}

$(document).on('ready', function(){
    $('#id_cliente_nombre').on('keyup', complete_cliente);
    $('#id_buscador_productos').on('keyup', complete_producto);
    $('#productos tbody').on('dblclick', '.detalle', update_fila);
    $('#modal_ok').on('click', validar_modal);
    $('#exitencia').on('click', 'tr', selected_fila);
    $('#id_ir').on('change', calcular_factura);
    $('#id_al').on('change', calcular_factura);
    $('#id_excento').on('change', calcular_factura);
    $('#modal_cantidad').on('focus', $(this).select());
    $('#id_close_modal').on('click', quitar_fila);
    $('#modal_delete').on('click', eliminar_producto);
    $('#modal_descuento_1').on('change', get_descuento);
    $('form').keydown(function(event){
      if(event.keyCode==13){
        event.preventDefault();
        return false;
      }
    });
});

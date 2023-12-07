
$(document).ready(function () {

    
    // Función para agregar producto a la tabla de productos seleccionados y actualizar campos ocultos
    function agregarProductoATabla(id, nombre,  cantidad, precio) {
        // Crear fila con el producto
        var fila = '<tr>' +
            '<td>' + id + '</td>' +
            '<td>' + nombre + '</td>' +
            '<td>' + cantidad + '</td>' +
            '<td>' + precio + '</td>' +
            '<td><button type="button" class="btn btn-danger btn-sm eliminar-producto">Eliminar</button></td>' +
            '</tr>';

        // Agregar la fila a la tabla de productos seleccionados
        $('#tabla_productos_seleccionados').append(fila);

        // Actualizar los campos ocultos del formulario
        actualizarCamposOcultos();
        var precioTotalActual = parseFloat($('#precio-total').text());
        precioTotalActual += parseFloat(precio) * cantidad;
        $('#precio-total').text(precioTotalActual.toFixed(0));

        var cantidadTotalActual = parseInt($('#cantidad-total').text());
        cantidadTotalActual += cantidad;
        $('#cantidad-total').text(cantidadTotalActual);
    }

    // Agregar producto a la tabla de productos seleccionados y campos ocultos
    $(document).on('click', '.btn_agregar_producto', function () {
        var filaEncontrada = $(this).closest('tr');
        var nombreProducto = filaEncontrada.find('td:eq(1)').text();
        var idProducto = filaEncontrada.find('td:eq(0)').text();
        var cantidadSeleccionada = parseInt(filaEncontrada.find('input').val());
        var precioProducto = parseFloat(filaEncontrada.find('td:eq(3)').text());
        var stockDisponible = parseInt($(this).data('stock'));

        // Verificar la cantidad total del producto seleccionado ya agregado
        var cantidadTotalProducto = 0;
        $('#tabla_productos_seleccionados tr').each(function () {
            var nombreProductoSeleccionado = $(this).find('td:eq(0)').text();
            var cantidadProductoSeleccionado = parseInt($(this).find('td:eq(2)').text());

            if (nombreProductoSeleccionado === nombreProducto) {
                cantidadTotalProducto += cantidadProductoSeleccionado;
            }
        });

        // Verificar si la cantidad total excede el stock
        if (cantidadTotalProducto + cantidadSeleccionada > stockDisponible) {
            alert('La cantidad total seleccionada del producto excede el stock disponible.');
            return;
        }

        // Agregar el producto a la tabla de productos seleccionados
        agregarProductoATabla(nombreProducto,idProducto, cantidadSeleccionada, precioProducto);
    });

    // Eliminar producto al hacer clic en el botón "Eliminar"
    $(document).on('click', '.eliminar-producto', function () {
                var filaEliminada = $(this).closest('tr');
                var precioEliminado = parseFloat(filaEliminada.find('td:eq(3)').text());
                var cantidadEliminada = parseInt(filaEliminada.find('td:eq(2)').text());

                var precioTotalActual = parseFloat($('#precio-total').text());
                precioTotalActual -= precioEliminado * cantidadEliminada;
                $('#precio-total').text(precioTotalActual.toFixed(0)); // Mostrar el precio total sin decimales

                var cantidadTotalActual = parseInt($('#cantidad-total').text());
                cantidadTotalActual -= cantidadEliminada;
                $('#cantidad-total').text(cantidadTotalActual);

                filaEliminada.remove(); // Eliminar la fila correspondiente
            });

    // Función para actualizar los campos ocultos con los productos seleccionados
    function actualizarCamposOcultos() {
        // Limpiar los campos ocultos existentes
        $('[name^="productos_seleccionados_ids"]').remove();
        $('[name^="cantidad_producto_"]').remove();

        // Iterar sobre las filas de productos seleccionados y actualizar los campos ocultos
        $('#tabla_productos_seleccionados tr').each(function () {
            var nombreProducto = $(this).find('td:eq(0)').text();
            var cantidadProducto = $(this).find('td:eq(2)').text();
            var idProducto = $(this).find('td:eq(1)').text().trim(); // Obtener el ID como texto y quitar espacios en blanco
            idProducto = idProducto === '' ? null : parseInt(idProducto);

            // Verificar si el ID es un número válido antes de proceder
            if (!isNaN(idProducto) && idProducto !== null) {
                // Crear campos ocultos para el producto y su cantidad
                var campoProductoId = '<input type="hidden" name="productos_seleccionados_ids" value="' + idProducto + '">';
                var campoCantidadProducto = '<input type="hidden" name="cantidad_producto_' + idProducto + '" value="' + cantidadProducto + '">';

                // Agregar los campos ocultos al formulario
                $('#detalle-orden-form').append(campoProductoId);
                $('#detalle-orden-form').append(campoCantidadProducto);
            } else {
                // Manejar caso donde el ID no es un número válido
                console.error('El ID del producto no es un número válido:', idProducto);
            }
        });
    }
    
    $(document).on('click', '#btn_buscar', function () {
            var query = $('#id_buscar_producto').val();
            var url = $(this).data('url');
            if (query !== '') {
                $.ajax({
                    url: url,  // URL de la vista para buscar productos
                    method: 'GET',
                    data: { 'query': query },
                    dataType: 'json',
                    success: function (data) {
                        if (Array.isArray(data.productos)) {
                            $('#tabla_productos_buscados').empty();
                            data.productos.forEach(function (producto) {
                                var fila = '<tr>' +
                                    '<td>' + producto.id + '</td>' +
                                    '<td>' + producto.nombre + '</td>' +
                                    '<td>' + producto.cantidad + '</td>' +
                                    '<td>' + producto.precio + '</td>' +
                                    '<td><button type="button" class="btn btn-primary btn_agregar_producto" data-stock="' + producto.cantidad + '">Agregar</button></td>' +
                                    '<td><div class="input-group mb-3" style="width: 130px;">' +
                                    '<button type="button" class="input-group-text" data-stock="' + producto.cantidad + '">-</button>' +
                                    '<input type="text" class="form-control text-center bg-white" value="1" disabled>' +
                                    '<button type="button" class="input-group-text" data-stock="' + producto.cantidad + '">+</button>' +
                                    '</div></td>' +
                                    '</tr>';
                                $('#tabla_productos_buscados').append(fila);
                            });
                        } else {
                            alert('No se encontraron productos.');
                        }
                    },
                    error: function () {
                        alert('Error al buscar productos.');
                    }
                });
            }
        });
        $(document).on('click', '.input-group-text', function (event) {
            var input = $(this).siblings('input');
            var valor = parseInt(input.val());
            var stock = parseInt($(this).data('stock'));

            if ($(this).text() === '+' && valor < stock) {
                input.val(valor + 1);
            } else if ($(this).text() === '-' && valor > 1) {
                input.val(valor - 1);
            }

            $(this).siblings('input').attr('data-cantidad-seleccionada', input.val());
        });
        

    
});


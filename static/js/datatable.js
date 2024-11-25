$(function () {
  // Inicializa el DataTable en el elemento con ID example1
  $("#example1").DataTable({
    "responsive": true, // Hace que la tabla sea adaptable a diferentes tamaños de pantalla
    "lengthChange": false, // Deshabilita la opción para cambiar el número de registros por página
    "autoWidth": true, // Deshabilita el ajuste automático del ancho de las columnas
    "lengthMenu": [10, 25, 100], // Define las opciones del menú desplegable para el número de registros por página
    "pageLength": 5, // Establece el número de registros por página a 5

    // Configura la traducción de los textos del DataTable al español
    "language": {
      "sProcessing": "Procesando...", // Texto mostrado durante el procesamiento
      "sLengthMenu": "Mostrar _MENU_ registros", // Texto para el menú de longitud de página
      "sZeroRecords": "No se encontraron resultados", // Texto cuando no se encuentran registros
      "sEmptyTable": "Ningún dato disponible en esta tabla", // Texto cuando la tabla está vacía
      "sInfo": "_START_ al _END_ de _TOTAL_ registros", // Texto de información de registros mostrados
      "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros", // Texto cuando no hay registros que mostrar
      "sInfoFiltered": "(filtrado de un total de _MAX_ registros)", // Texto de información de registros filtrados
      "sInfoPostFix": "", // Sufijo para la información de registros (vacío en este caso)
      "sSearch": "Buscar:", // Texto para la etiqueta de búsqueda
      "sUrl": "", // URL para cargar datos adicionales (no se usa aquí)
      "sInfoThousands": ",", // Separador de miles
      "sLoadingRecords": "Cargando...", // Texto mostrado mientras se cargan los registros
      "oPaginate": {
        "sFirst": "Primero", // Texto para el botón de paginación "Primero"
        "sLast": "Último", // Texto para el botón de paginación "Último"
        "sNext": "Siguiente", // Texto para el botón de paginación "Siguiente"
        "sPrevious": "Anterior" // Texto para el botón de paginación "Anterior"
      },
      "oAria": {
        "sSortAscending": ": Activar para ordenar la columna de manera ascendente", // Texto para accesibilidad (orden ascendente)
        "sSortDescending": ": Activar para ordenar la columna de manera descendente" // Texto para accesibilidad (orden descendente)
      }
    }
  });
});
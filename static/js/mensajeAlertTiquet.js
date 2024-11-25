(function () {
  // Selecciona todos los elementos con la clase 'btnEditar' y los almacena en la constante btnsEditar
  const btnsEditar = document.querySelectorAll('.btnEditar'); // btnEditar hace referencia a un botón que se le puso una clase de nombre btnEditar

  // Itera sobre cada botón en la lista de btnsEditar
  btnsEditar.forEach((btn) => {
      // Añade un evento 'click' a cada botón
      btn.addEventListener('click', function () {
          // Muestra una alerta personalizada usando SweetAlert2
          Swal.fire({
              //position: 'top-end', // Posición de la alerta (comentada)
              title: 'Excelente', // Título de la alerta
              //titleText: 'Your work has been saved 2', // Texto del título (comentado)
              text: 'Los cambios fueron realizados', // Texto del mensaje
              icon: 'success', // Tipo de ícono (éxito)
              showConfirmButton: true, // Muestra el botón de confirmación
              // confirmButtonText: 'Ok', // Texto personalizado para el botón de confirmación (si se desea personalizar)
              timer: 1700 // Duración en milisegundos antes de que la alerta se cierre automáticamente
          });
          //confirmarComprar(); // Llama a la función confirmarComprar (comentada)
      });
  });
})();

// Ejemplo de uso de SweetAlert2 para una alerta simple (comentado)
/*
Swal.fire(
  'Deleted!', // Título
  'Your file has been deleted.', // Texto del mensaje
  'success' // Tipo de ícono (éxito)
)
*/

// Asigna el id 'btn1' a un botón y añade un evento 'click' que muestra una alerta simple
$("#btn1").click(function(){
  alert("prueba"); // Muestra una alerta con el texto "prueba"
});
// Escucha el evento 'DOMContentLoaded' que se dispara cuando el DOM ha terminado de cargarse
document.addEventListener('DOMContentLoaded', function() {
    // Selecciona el formulario con el ID 'requerimiento-form'
    const form = document.getElementById('requerimiento-form');
  
    // Añade un evento 'submit' al formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Previene el envío normal del formulario
  
        // Crea un objeto FormData a partir del formulario
        const formData = new FormData(form);
  
        // Realiza una solicitud fetch al action del formulario utilizando el método POST y enviando formData
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Indica que la solicitud es una petición AJAX
            }
        })
        .then(response => response.json()) // Convierte la respuesta a JSON
        .then(data => {
            if (data.success) { // Si la respuesta indica éxito
                Swal.fire({
                    title: 'Excelente', // Título de la alerta
                    text: 'El tiquet es: ' + data.id, // Mensaje de la alerta que incluye el ID del tiquet
                    icon: 'success', // Ícono de éxito
                    showConfirmButton: true, // Muestra el botón de confirmación
                    confirmButtonText: 'Ok' // Texto del botón de confirmación
                }).then((result) => {
                    if (result.isConfirmed) { // Si el usuario hace clic en "Ok"
                        window.location.reload(); // Recarga la página
                    }
                });
            } else { // Si la respuesta indica error
                // Maneja los errores de validación aquí
                let errorMessages = ''; // Inicializa un string para almacenar los mensajes de error
                for (const [field, errors] of Object.entries(data.errors)) { // Itera sobre los errores recibidos
                    errorMessages += `${field}: ${errors.join(', ')}\n`; // Agrega cada error al string de mensajes
                }
                Swal.fire({
                    title: 'Error', // Título de la alerta de error
                    text: errorMessages, // Mensaje de error
                    icon: 'error', // Ícono de error
                    showConfirmButton: true, // Muestra el botón de confirmación
                    confirmButtonText: 'Ok' // Texto del botón de confirmación
                });
            }
        })
        .catch(error => { // Maneja errores en la solicitud fetch
            console.error('Error:', error); // Muestra el error en la consola
            Swal.fire({
                title: 'Error', // Título de la alerta de error
                text: 'Ocurrió un error al enviar el formulario.', // Mensaje de error
                icon: 'error', // Ícono de error
                showConfirmButton: true, // Muestra el botón de confirmación
                confirmButtonText: 'Ok' // Texto del botón de confirmación
            });
        });
    });
  });
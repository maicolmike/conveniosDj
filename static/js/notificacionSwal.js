// Define una función de flecha llamada notificacionSwal que toma cuatro parámetros: titleText, text, icon, confirmButtonText
const notificacionSwal = (titleText, text, icon, confirmButtonText) => {
    // Llama a SweetAlert2 para mostrar una alerta con los parámetros proporcionados
    Swal.fire({
        titleText: titleText,         // Establece el texto del título de la alerta
        text: text,                   // Establece el texto del cuerpo de la alerta
        icon: icon,                   // Establece el ícono de la alerta (puede ser 'success', 'error', 'warning', 'info', 'question')
        confirmButtonText: confirmButtonText // Establece el texto del botón de confirmación
    });
};
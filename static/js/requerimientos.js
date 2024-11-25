document.addEventListener('DOMContentLoaded', function () {
    // Obtener referencias a los elementos del formulario
    const clasificacion = document.getElementById('clasificacion');
    const subClasificacion = document.getElementById('sub_clasificacion');
    const form = document.querySelector('form');

    // Definir las subclasificaciones disponibles para cada clasificación
    const subClasificaciones = {
        '': [],
        'Software': [
            { value: '', text: 'Seleccionar' },
            { value: 'linix', text: 'Linix' },
            { value: 'workmanager', text: 'Workmanager' },
            { value: 'administrativo visionamos adminweb', text: 'Administrativo visionamos adminweb' },
            { value: 'multiportal', text: 'Multiportal' },
            { value: 'aplicativo convenios', text: 'Aplicativo convenios' },
            { value: 'aplicativo PEPS', text: 'Aplicativo PEPS' },
            { value: 'pasarela ACH colombian', text: 'Pasarela ACH colombian' },
            { value: 'consulta web', text: 'Consulta web' },
            { value: 'correo electronico institucional', text: 'Correo electronico institucional' }
        ],
        'Hardware': [
            { value: '', text: 'Seleccionar' },
            { value: 'computadores', text: 'Computadores' },
            { value: 'impresoras y validadoras', text: 'Impresoras y validadoras' },
            { value: 'UPS', text: 'UPS' },
            { value: 'estabilizadores', text: 'Estabilizadores' },
            { value: 'planta electrica', text: 'Planta eléctrica' },
            { value: 'instalaciones electricas', text: 'Instalaciones eléctricas' },
            { value: 'datafonos', text: 'Datafonos' },
            { value: 'aire acondicionado', text: 'Aire acondicionado' },
            { value: 'DVR', text: 'DVR' },
            
        ],
        'Comunicaciones': [
            { value: '', text: 'Seleccionar' },
            { value: 'internet', text: 'Internet' },
            { value: 'equipos de comunicacion', text: 'Equipos de comunicación' },
            { value: 'puntos de red de datos', text: 'Puntos de red de datos' },
            { value: 'conexion remota data center', text: 'Conexión remota data center' }
        ],'Transaccional': [
            { value: '', text: 'Seleccionar' },
            { value: 'retiros', text: 'Retiros' },
            { value: 'transferencias', text: 'Transferencias' },
            { value: 'cupo rotativo', text: 'Cupo rotativo' },
            { value: 'tarjetas', text: 'Tarjetas' },
            { value: 'recaudos PSE', text: 'Recaudos PSE' },
            { value: 'recaudos supergiros', text: 'Recaudos supergiros' },
        ]
        
    };

    // Manejar el evento de cambio en el campo de clasificación
    clasificacion.addEventListener('change', function () {
        const selected = this.value;  // Obtener el valor seleccionado
        const options = subClasificaciones[selected] || [];  // Obtener las subclasificaciones correspondientes
        
        subClasificacion.innerHTML = '';  // Limpiar las opciones actuales
        subClasificacion.disabled = false;  // Habilitar el campo de subclasificación

        // Añadir las nuevas opciones de subclasificación
        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option.value;
            opt.text = option.text;
            subClasificacion.appendChild(opt);
        });
    });

    // Manejar el evento de envío del formulario
    form.addEventListener('submit', function (event) {
        // Verificar si el campo de subclasificación está vacío
        if (subClasificacion.value === '') {
            event.preventDefault(); // Prevenir el envío del formulario
            alert('Debe seleccionar una subclasificación.'); // Mostrar alerta
            //clasificacion.value = ''; // Resetear el campo de clasificación a "Seleccionar"
        }
    });
});
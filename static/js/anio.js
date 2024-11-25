// Obtiene el año actual utilizando el objeto Date y el método getFullYear()
var anio = new Date().getFullYear(); // Crea un nuevo objeto Date y obtiene el año actual

// Encuentra el elemento con el ID "anio_actual" y establece su contenido HTML con el año actual
document.getElementById("anio_actual").innerHTML = anio;
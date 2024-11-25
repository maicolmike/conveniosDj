document.addEventListener('DOMContentLoaded', function() {
    const itemsPerPage = 5; // Define el número de elementos por página

    document.querySelectorAll('.modal').forEach(modal => {
      const modalId = modal.getAttribute('id').replace('modalDetalleRequerimiento', ''); // Obtiene el ID del modal
      const rows = document.querySelectorAll(`.detalle-row-${modalId}`); // Selecciona las filas de detalles
      const totalItems = rows.length + 1; // Incluye el requerimiento principal en el conteo total
      const totalPages = Math.ceil(totalItems / itemsPerPage); // Calcula el número total de páginas
      const pagination = document.getElementById(`pagination-${modalId}`); // Elemento de paginación
      const rangeInfo = document.getElementById(`range-info-${modalId}`); // Información de rango de registros
      const requerimientoPrincipal = document.querySelector(`#table-div-${modalId} .requerimiento-principal`); // Fila del requerimiento principal

      // Función para actualizar la información de rango
      function updateRangeInfo(page, totalItems, itemsPerPage) {
        const start = (page - 1) * itemsPerPage + 1;
        const end = Math.min(start + itemsPerPage - 1, totalItems);
        rangeInfo.textContent = `${start} - ${end} de ${totalItems} registros`;
      }

      // Función para mostrar la página seleccionada
      function showPage(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        // Muestra el requerimiento principal y los primeros detalles en la primera página
        if (page === 1) {
          requerimientoPrincipal.style.display = 'flex';
          rows.forEach((row, index) => {
            row.style.display = (index < itemsPerPage - 1) ? 'flex' : 'none';
          });
        } else { // Muestra solo los detalles en las páginas siguientes
          requerimientoPrincipal.style.display = 'none';
          rows.forEach((row, index) => {
            row.style.display = (index >= start - 1 && index < end - 1) ? 'flex' : 'none';
          });
        }

        // Limpia la paginación actual
        pagination.innerHTML = '';

        // Botón para la primera página
        const firstPageItem = document.createElement('li');
        firstPageItem.className = 'page-item' + (page === 1 ? ' disabled' : '');
        const firstPageLink = document.createElement('a');
        firstPageLink.className = 'page-link';
        firstPageLink.textContent = 'Primero';
        firstPageLink.href = '#';
        firstPageLink.addEventListener('click', (e) => {
          e.preventDefault();
          showPage(1);
        });
        firstPageItem.appendChild(firstPageLink);
        pagination.appendChild(firstPageItem);

        // Botón para la página anterior
        const prevPageItem = document.createElement('li');
        prevPageItem.className = 'page-item' + (page === 1 ? ' disabled' : '');
        const prevPageLink = document.createElement('a');
        prevPageLink.className = 'page-link';
        prevPageLink.textContent = 'Anterior';
        prevPageLink.href = '#';
        prevPageLink.addEventListener('click', (e) => {
          e.preventDefault();
          showPage(page - 1);
        });
        prevPageItem.appendChild(prevPageLink);
        pagination.appendChild(prevPageItem);

        // Botones para las páginas
        for (let i = 1; i <= totalPages; i++) {
          const li = document.createElement('li');
          li.className = 'page-item' + (i === page ? ' active' : '');
          const a = document.createElement('a');
          a.className = 'page-link';
          a.textContent = i;
          a.href = '#';
          a.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(i);
          });
          li.appendChild(a);
          pagination.appendChild(li);
        }

        // Botón para la siguiente página
        const nextPageItem = document.createElement('li');
        nextPageItem.className = 'page-item' + (page === totalPages ? ' disabled' : '');
        const nextPageLink = document.createElement('a');
        nextPageLink.className = 'page-link';
        nextPageLink.textContent = 'Siguiente';
        nextPageLink.href = '#';
        nextPageLink.addEventListener('click', (e) => {
          e.preventDefault();
          showPage(page + 1);
        });
        nextPageItem.appendChild(nextPageLink);
        pagination.appendChild(nextPageItem);

        // Botón para la última página
        const lastPageItem = document.createElement('li');
        lastPageItem.className = 'page-item' + (page === totalPages ? ' disabled' : '');
        const lastPageLink = document.createElement('a');
        lastPageLink.className = 'page-link';
        lastPageLink.textContent = 'Último';
        lastPageLink.href = '#';
        lastPageLink.addEventListener('click', (e) => {
          e.preventDefault();
          showPage(totalPages);
        });
        lastPageItem.appendChild(lastPageLink);
        pagination.appendChild(lastPageItem);

        // Actualiza la información de rango
        updateRangeInfo(page, totalItems, itemsPerPage);
      }

      // Muestra la primera página por defecto
      showPage(1);
    });
  });
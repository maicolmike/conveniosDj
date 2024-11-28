from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # Restringe el acceso a la vista solo a usuarios autenticados
from .forms import ConsultaAsociado  # Importar el formulario personalizado para la consulta
from django.db import connections  # Para manejar múltiples bases de datos, en este caso Oracle

# Vista protegida por login
@login_required(login_url='login')
def consulta(request):
    # Inicializamos 'resultado' como None para manejar casos donde no se realiza ninguna consulta
    resultado = None

    # Creamos una instancia del formulario y llenamos los datos si se trata de una solicitud POST
    form = ConsultaAsociado(request.POST or None)

    # Si el método de la solicitud es POST y los datos del formulario son válidos
    if request.method == 'POST' and form.is_valid():
        # Obtener el dato de identificación del formulario
        identificacion = form.cleaned_data['identificacion']
        
        # Realizar la conexión con la base de datos Oracle y ejecutar la consulta
        with connections['oracle'].cursor() as cursor:
            # Consulta SQL para obtener información del asociado y calcular valores de vencimientos
            query = """
            SELECT ap014.aanumnit, ap014.nnasocia,
                   (SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                    FROM dr041mgdocumen
                    WHERE dr041mgdocumen.k_tipodr = '1'
                      AND dr041mgdocumen.k_idterc = ap014.k_idterc
                      AND dr041mgdocumen.i_cancel = 'N') ven_aportes, -- Deuda de aportes vencidos
                   (SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                    FROM dr041mgdocumen
                    WHERE dr041mgdocumen.k_tipodr = '3'
                      AND dr041mgdocumen.k_idterc = ap014.k_idterc
                      AND dr041mgdocumen.i_cancel = 'N') ven_contractual, -- Deuda contractual vencida
                   (SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                    FROM dr041mgdocumen
                    WHERE dr041mgdocumen.k_tipodr = 'CMT'
                      AND dr041mgdocumen.k_idterc = ap014.k_idterc
                      AND dr041mgdocumen.i_cancel = 'N') ven_cuotamanejo, -- Deuda de cuota de manejo vencida
                   (SELECT SUM(PK_CA_FUNCION.FU_CONCEPTO('CAPITAL','VENCIDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL))
                    FROM ca090mgsolcred
                    WHERE ap014.k_idterc = ca090mgsolcred.k_idterc
                      AND ca090mgsolcred.a_tipodr = '10'
                      AND PK_CA_FUNCION.FU_CONCEPTO('CAPITAL','SALDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL) > 0
                      AND ca090mgsolcred.i_estsol = 'C'
                      AND ca090mgsolcred.i_anulad = 'N')
                   + (SELECT SUM(PK_CA_FUNCION.FU_CONCEPTO('INTERES','VENCIDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL))
                      FROM ca090mgsolcred
                      WHERE ap014.k_idterc = ca090mgsolcred.k_idterc
                        AND ca090mgsolcred.a_tipodr = '10'
                        AND PK_CA_FUNCION.FU_CONCEPTO('CAPITAL','SALDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL) > 0
                        AND ca090mgsolcred.i_estsol = 'C'
                        AND ca090mgsolcred.i_anulad = 'N')
                   + (SELECT SUM(PK_CA_FUNCION.FU_CONCEPTO('SEGURO_VIDA','VENCIDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL))
                      FROM ca090mgsolcred
                      WHERE ap014.k_idterc = ca090mgsolcred.k_idterc
                        AND ca090mgsolcred.a_tipodr = '10'
                        AND PK_CA_FUNCION.FU_CONCEPTO('CAPITAL','SALDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL) > 0
                        AND ca090mgsolcred.i_estsol = 'C'
                        AND ca090mgsolcred.i_anulad = 'N') ven_credito -- Deuda de crédito vencida
            FROM ap014mcliente ap014
            WHERE ap014.aanumnit = :identificacion -- Buscar por identificación
              AND PK_AP_AFILIACION.FU_CLIENTE_ACTIVO(ap014.k_idterc, SYSDATE) = 'ACTIVO' -- Validar que el cliente esté activo
            """
            # Ejecutar la consulta con el valor proporcionado
            cursor.execute(query, {'identificacion': identificacion})
            # Obtener todos los resultados de la consulta
            resultado = cursor.fetchall()

    # Renderizar el template y pasar los datos del formulario y los resultados
    return render(request, 'consulta/consulta.html', {
        'title': "Consultar asociado",  # Título de la página
        'form': form,  # El formulario para renderizar en la vista
        'resultado': resultado,  # Los resultados de la consulta
    })

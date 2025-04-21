from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ConsultaAsociado
from django.db import connections

@login_required(login_url='login')
def consulta(request):
    resultado = None
    estado_aptitud = None
    mensaje = ""
    mensaje2 = ""
    form = ConsultaAsociado(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        identificacion = form.cleaned_data['identificacion']
        
        # Realizar consulta en la base de datos
        with connections['oracle'].cursor() as cursor:
            query = """
            SELECT ap014.aanumnit, ap014.nnasocia,
                   NVL((SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                        FROM dr041mgdocumen
                        WHERE dr041mgdocumen.k_tipodr = '1'
                          AND dr041mgdocumen.k_idterc = ap014.k_idterc
                          AND dr041mgdocumen.i_cancel = 'N'), 0) ven_aportes,
                   NVL((SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                        FROM dr041mgdocumen
                        WHERE dr041mgdocumen.k_tipodr = '3'
                          AND dr041mgdocumen.k_idterc = ap014.k_idterc
                          AND dr041mgdocumen.i_cancel = 'N'), 0) ven_contractual,
                   NVL((SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                        FROM dr041mgdocumen
                        WHERE dr041mgdocumen.k_tipodr = 'CMT'
                          AND dr041mgdocumen.k_idterc = ap014.k_idterc
                          AND dr041mgdocumen.i_cancel = 'N'), 0) ven_cuotamanejo,
                   NVL((SELECT SUM(PK_CA_FUNCION.FU_CONCEPTO('CAPITAL','VENCIDO',ca090mgsolcred.a_tipodr, ca090mgsolcred.a_obliga, SYSDATE, NULL, NULL))
                        FROM ca090mgsolcred
                        WHERE ap014.k_idterc = ca090mgsolcred.k_idterc
                          AND ca090mgsolcred.a_tipodr = '10'
                          AND ca090mgsolcred.i_estsol = 'C'
                          AND ca090mgsolcred.i_anulad = 'N'), 0) ven_credito
            FROM ap014mcliente ap014
            WHERE ap014.AANUMNIT IN (:identificacion) 
            AND (PK_AP_AFILIACION.FU_CLIENTE_ACTIVO(AP014.K_IDTERC,SYSDATE)='EN_SOLICITUD_RETIRO'
            OR PK_AP_AFILIACION.FU_CLIENTE_ACTIVO(AP014.K_IDTERC,SYSDATE)='CON_NOVEDAD'
            OR PK_AP_AFILIACION.FU_CLIENTE_ACTIVO(AP014.K_IDTERC,SYSDATE)='ACTIVO')
            """
            cursor.execute(query, {'identificacion': identificacion})
            resultado = cursor.fetchone()

        # Procesar los resultados
        if resultado:
            identificacion = resultado[0]
            nombre = resultado[1]
            deuda_aportes = resultado[2]
            deuda_contractual = resultado[3]
            deuda_cuota = resultado[4]
            deuda_credito = resultado[5]

            if deuda_aportes <= 0 and deuda_contractual <= 0 and deuda_cuota <= 0 and deuda_credito <= 0:
                estado_aptitud = "HABIL"
                mensaje = f"{identificacion} {nombre}"
                mensaje2 = "La persona es apta para convenios."
            else:
                estado_aptitud = "INHABIL"
                mensaje = f"{identificacion} {nombre}"
                mensaje2 = "La persona NO es apta para convenios, pendiente el pago de alguna de sus obligaciones."
        else:
            estado_aptitud = "no_encontrada"
            mensaje = f"No se encontraron resultados para la identificación {identificacion}."

        # Manejar respuestas AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'estado': estado_aptitud, 'mensaje': mensaje, 'mensaje2': mensaje2})

    # Renderizar la plantilla para solicitudes normales
    return render(request, 'consulta/consulta.html', {
        'title': "Consultar asociado",
        'form': form,
        'estado_aptitud': estado_aptitud,
        'mensaje': mensaje,
        'mensaje2': mensaje2,
    })

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # vista basada en funciones que no permita acceder a paginas donde no se ha logeado
from .forms import ConsultaAsociado
from django.db import connections  # PARA QUE TOME LA BD ORACLE

@login_required(login_url='login')
def consulta(request):
    resultado = None
    form = ConsultaAsociado(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identificacion = form.cleaned_data['identificacion']
        
        # Realizar la conexión a Oracle y ejecutar la consulta
        with connections['oracle'].cursor() as cursor:
            query = """
            SELECT ap014.aanumnit, ap014.nnasocia,
                   (SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                    FROM dr041mgdocumen
                    WHERE dr041mgdocumen.k_tipodr = '1'
                      AND dr041mgdocumen.k_idterc = ap014.k_idterc
                      AND dr041mgdocumen.i_cancel = 'N') ven_aportes,
                   (SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                    FROM dr041mgdocumen
                    WHERE dr041mgdocumen.k_tipodr = '3'
                      AND dr041mgdocumen.k_idterc = ap014.k_idterc
                      AND dr041mgdocumen.i_cancel = 'N') ven_contractual,
                   (SELECT SUM(pk_dr_vencimiento.FU_V_VENCIDO_DOCUMENTO(dr041mgdocumen.k_tipodr, dr041mgdocumen.k_numdoc, SYSDATE))
                    FROM dr041mgdocumen
                    WHERE dr041mgdocumen.k_tipodr = 'CMT'
                      AND dr041mgdocumen.k_idterc = ap014.k_idterc
                      AND dr041mgdocumen.i_cancel = 'N') ven_cuotamanejo,
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
                        AND ca090mgsolcred.i_anulad = 'N') ven_credito
            FROM ap014mcliente ap014
            WHERE ap014.aanumnit = :identificacion
              AND PK_AP_AFILIACION.FU_CLIENTE_ACTIVO(ap014.k_idterc, SYSDATE) = 'ACTIVO'
            """
            cursor.execute(query, {'identificacion': identificacion})
            resultado = cursor.fetchall()  # Obtén todos los resultados

    return render(request, 'consulta/consulta.html', {
        'title': "Consultar asociado",
        'form': form,
        'resultado': resultado,  # Pasar el resultado al template
    })

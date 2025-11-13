# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# ------------------------------------------------------------------------------
# CONTROLADOR: ListaSocios
# Este controlador devuelve todos los socios del sistema en formato JSON.
# URL: http://localhost:8069/gestion/socio
# ------------------------------------------------------------------------------

class ListaSocios(http.Controller):

    @http.route('/gestion/<modelo>', auth='public', cors='*', type='http')
    def obtenerDatosSocios(self, modelo, **kw):
        """
        Devuelve una lista de todos los registros del modelo indicado.
        Este ejemplo está pensado específicamente para el modelo 'socio'.
        """

        # ----------------------------------------------------------------------
        # Validación básica: comprobar que el modelo existe y es accesible
        # ----------------------------------------------------------------------
        try:
            request.env[modelo].sudo()
        except KeyError:
            return http.Response(
                json.dumps({'error': f"Modelo '{modelo}' no encontrado o no accesible"}),
                status=404,
                mimetype='application/json'
            )
        # ----------------------------------------------------------------------
        # Buscar todos los registros del modelo (ej. 'socio')
        # ----------------------------------------------------------------------
        socios = request.env[modelo].sudo().search([])

        # ----------------------------------------------------------------------
        # Generar lista en formato JSON simple
        # Cada socio se convierte en una lista: [num_socio, nombre, apellidos, foto, código barras]
        # ----------------------------------------------------------------------
        lista_socios = []
        for s in socios:
            lista_socios.append([
                s.num_socio,
                s.nombre,
                s.apellidos,
                str(s.foto or ''),            # Convertir imagen binaria a string (base64)
                str(s.barcode_carnet or '')
            ])

        # Devolver el JSON con la lista de socios
        return http.Response(
            json.dumps(lista_socios, default=str, indent=2),
            status=200,
            mimetype='application/json'
        )

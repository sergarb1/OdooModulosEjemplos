# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# ------------------------------------------------------------------------------
# CONTROLADOR API REST
# Permite realizar operaciones CRUD sobre el modelo 'socio' mediante llamadas HTTP.
# Ejemplos de uso:
# - POST: crear socio
# - PUT/PATCH: modificar socio
# - GET: consultar socio
# - DELETE: eliminar socio
# ------------------------------------------------------------------------------

class ApiRest(http.Controller):

    # --------------------------------------------------------------------------
    # RUTA PARA: POST (crear), PUT / PATCH (modificar)
    # --------------------------------------------------------------------------
    @http.route('/gestion/apirest/<model>', auth="none", cors='*', csrf=False,
                methods=["POST", "PUT", "PATCH"], type='http')
    def apiPost(self, model, **args):
        """
        Crear o modificar un registro del modelo indicado vía API REST.
        """
        # Extraemos los datos del parámetro 'data', que es un JSON en formato texto
        # Intentar leer los datos desde la URL (?data=...) o desde el cuerpo (Body JSON)
        if 'data' in args:
            dicDatos = json.loads(args['data'])
        else:
            raw_data = request.httprequest.data.decode('utf-8')
            dicDatos = json.loads(raw_data or '{}')

        # Verificamos que se haya enviado un número de socio
        if not dicDatos.get("num_socio"):
            return http.Response(json.dumps({'estado': 'SOCIONOINDICADO'}), status=400, mimetype='application/json')

        # Preparamos el criterio de búsqueda para localizar el socio
        search = [('num_socio', '=', int(dicDatos["num_socio"]))]

        # ----------------------------------------------------------------------
        # CASO POST → Crear nuevo socio
        # ----------------------------------------------------------------------
        if request.httprequest.method == 'POST':
            # Creamos el nuevo registro
            record = request.env[model].sudo().create(dicDatos)

            # Devolvemos los datos creados como JSON
            return http.Response(
                json.dumps(record.read(), default=str),
                status=200,
                mimetype='application/json'
            )

        # ----------------------------------------------------------------------
        # CASO PUT / PATCH → Modificar socio existente
        # ----------------------------------------------------------------------
        elif request.httprequest.method in ['PUT', 'PATCH']:
            record = request.env[model].sudo().search(search)
            if record:
                record[0].write(dicDatos)
                return http.Response(
                    json.dumps(record.read(), default=str),
                    status=200,
                    mimetype='application/json'
                )
            else:
                return http.Response(json.dumps({'estado': 'NOTFOUND'}), status=404, mimetype='application/json')

        # Si no es ninguno de los métodos esperados, devolvemos sesión
        return request.env['ir.http'].session_info()

    # --------------------------------------------------------------------------
    # RUTA PARA: GET (consultar), DELETE (eliminar)
    # --------------------------------------------------------------------------
    @http.route('/gestion/apirest/<model>', auth="none", cors='*', csrf=False,
                methods=["GET", "DELETE"], type='http')
    def apiGet(self, model, **args):
        """
        Consultar o eliminar un socio vía API REST.
        """
        # Convertimos el contenido de 'data' a diccionario
        dicDatos = json.loads(args.get('data', '{}'))

        # Si no se indica num_socio, devolvemos error
        if not dicDatos.get("num_socio"):
            return http.Response(json.dumps({'estado': 'SOCIONOINDICADO'}), status=400, mimetype='application/json')

        search = [('num_socio', '=', int(dicDatos["num_socio"]))]

        # ----------------------------------------------------------------------
        # CASO GET → Consultar datos del socio
        # ----------------------------------------------------------------------
        if request.httprequest.method == 'GET':
            record = request.env[model].sudo().search(search)
            if record:
                return http.Response(
                    json.dumps(record[0].read(), default=str),
                    status=200,
                    mimetype='application/json'
                )
            return http.Response(json.dumps({'estado': 'NOTFOUND'}), status=404, mimetype='application/json')

        # ----------------------------------------------------------------------
        # CASO DELETE → Eliminar registro del socio
        # ----------------------------------------------------------------------
        elif request.httprequest.method == 'DELETE':
            record = request.env[model].sudo().search(search)
            if record:
                # Guardamos los datos antes de borrar
                data_deleted = record[0].read()
                record[0].unlink()
                return http.Response(
                    json.dumps(data_deleted, default=str),
                    status=200,
                    mimetype='application/json'
                )
            return http.Response(json.dumps({'estado': 'NOTFOUND'}), status=404, mimetype='application/json')

        return request.env['ir.http'].session_info()

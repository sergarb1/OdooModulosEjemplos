# -*- coding: utf-8 -*-
# Importamos clases necesarias de Odoo para definir controladores HTTP
from odoo import http
from odoo.http import request

# Importamos bibliotecas externas necesarias para generar imágenes en memoria
import base64                    # Para codificar la imagen en base64 (para mostrarla en HTML)
from io import BytesIO           # Para trabajar con flujos de memoria

# Importamos la librería de generación de códigos de barras
# NOTA: Esta librería debe instalarse por pip: python-barcode y python-barcode[images]
import barcode
from barcode.writer import ImageWriter


# Clase controladora para las rutas HTTP que expone nuestro módulo
class GenerarBarcode(http.Controller):

    '''
    Este método permite generar un código de barras EAN-13 desde una URL,
    sin necesidad de autenticación. Ideal para integración con otras apps o para pruebas.

    Ejemplo de uso:
    http://localhost:8069/generador/123456789012

    Mostrará una imagen HTML con el código de barras generado.
    '''

    # Ruta expuesta públicamente (auth='public'), sin restricciones CORS (cors='*')
    @http.route('/generador/<codigo>', auth='public', cors='*', type='http')
    def crearBarcode(self, codigo, **kw):
        # Obtenemos la clase del tipo de código de barras que vamos a usar (EAN13)
        EAN = barcode.get_barcode_class('ean13')

        # Aseguramos que el código tenga 12 dígitos rellenando con ceros a la izquierda
        # NOTA: El EAN-13 requiere 12 dígitos + 1 dígito de control (calculado automáticamente)
        codigo_ean = str(codigo).zfill(12)

        # Creamos el objeto del código de barras, pasándole el escritor de imágenes
        ean = EAN(codigo_ean, writer=ImageWriter())

        # Creamos un flujo en memoria para guardar la imagen generada
        fp = BytesIO()

        # Escribimos la imagen del código de barras en el flujo
        ean.write(fp)

        # Codificamos el flujo de bytes en base64 para poder usarlo en HTML
        img_str = base64.b64encode(fp.getvalue()).decode("utf-8")

        # Devolvemos una pequeña vista HTML que muestra la imagen generada
        return '<div><img src="data:image/png;base64,' + img_str + '"/></div>'

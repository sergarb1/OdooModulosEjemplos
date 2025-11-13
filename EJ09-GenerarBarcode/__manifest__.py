# -*- coding: utf-8 -*-
{
    'name': "Generador de códigos de barras a partir de un número",  # Nombre del módulo
    'summary': "Genera un código de barras desde una llamada web pública",  # Breve descripción

    'description': """
    Generador de códigos de barras vía HTTP
    =======================================
    Este módulo expone una ruta web para generar códigos de barras en formato EAN-13
    a partir de un número proporcionado en la URL. Ideal para pruebas o integración
    con otras aplicaciones.
    """,

    'application': True,                   # Indica que es una aplicación independiente en Odoo
    'author': "Sergi García",
    'website': "http://apuntesfpinformatica.es",
    'category': 'Tools',                  # Categoría en el menú de apps de Odoo
    'version': '0.1',
    'depends': ['base'],                  # Dependencias del módulo. Este depende solo del módulo base.

    # DEPENDENCIAS EXTERNAS: necesarias para que funcione la generación de códigos de barras.
    # Si usas Docker Compose:
    # 1. Entra al contenedor: docker-compose exec web bash
    # 2. Instala las dependencias: pip3 install python-barcode python-barcode[images]

    'external_dependencies': {
        "python": [
            'python-barcode'
        ],
        "bin": []
    },

    'data': [
        # Este módulo no tiene vistas, modelos o datos XML
    ],

    # Demo data opcional (no usado en este caso)
    # 'demo': [
    #     'demo.xml'
    # ],
}

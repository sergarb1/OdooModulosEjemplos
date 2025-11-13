# -*- coding: utf-8 -*-
{
    # Nombre del módulo que aparecerá en la interfaz de Odoo
    'name': "API REST to manage members",

    # Breve descripción que aparece en la lista de módulos
    'summary': "Manage members through Odoo views and a custom REST API.",

    # Descripción larga del módulo
    'description': """
Custom module to manage members using both Odoo views (tree, form, kanban) and a RESTful API.
Features:
 - Member listing and form
 - REST API to Create, Read, Update, Delete members
""",

    # Indicamos que este módulo es una aplicación principal
    'application': True,

    # Información del autor del módulo
    'author': "Sergi García",
    'website': "http://apuntesfpinformatica.es",

    # Categoría del módulo (puede ser: 'Sales', 'Inventory', 'Human Resources', etc.)
    'category': 'Tools',

    # Versión del módulo (conviene actualizar al hacer cambios mayores)
    'version': '1.0.0',

    # Dependencias: Este módulo necesita que esté instalado 'base' (core de Odoo)
    'depends': ['base'],

    # Archivos de datos que se cargarán al instalar el módulo
    'data': [
        'security/ir.model.access.csv',  # Permisos de acceso
        'views/socio.xml',               # Vistas del modelo 'socio'
    ],

    # Archivos opcionales de demo (no incluidos aquí)
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

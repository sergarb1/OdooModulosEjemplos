# -*- coding: utf-8 -*-  # Indicamos que este archivo puede contener caracteres especiales como acentos

{
    # Nombre del módulo que aparecerá en la vista de aplicaciones de Odoo
    'name': "Lista de tareas",

    # Descripción corta que se mostrará debajo del nombre
    'summary': "Módulo educativo para crear una lista de tareas simples",

    # Descripción larga. Es útil para documentar el propósito del módulo.
    'description': """
        Este módulo permite crear tareas con prioridad, urgencia calculada y estado de realización.
        Ideal como primer proyecto de desarrollo en Odoo.
    """,

    # Autor del módulo (puede ser un nombre real, grupo de trabajo o entidad educativa)
    'author': "Tu Nombre",

    # Sitio web asociado (puede ser un portafolio, escuela o GitHub del proyecto)
    'website': "https://tusitio.com",

    # Esta línea indica que es una aplicación (aparecerá en la lista de Apps principales)
    'application': True,

    # Categoría a la que pertenece. Se usa para agrupar módulos en el App Store de Odoo.
    'category': 'Productivity',

    # Versión del módulo (puedes usar 0.1 para proyectos educativos o de prueba)
    'version': '0.1',

    # Tipo de licencia. 'LGPL-3' es libre y compatible con los estándares de Odoo.
    'license': 'LGPL-3',

    # Si es True, el módulo puede instalarse desde la interfaz de Odoo
    'installable': True,

    # Lista de módulos de los que depende este para funcionar correctamente.
    # 'base' es el mínimo necesario para que cualquier módulo funcione.
    'depends': ['base'],

    # Archivos que deben cargarse al instalar el módulo (vistas, seguridad, datos, etc.)
    'data': [
        # Permisos de acceso al modelo
        'security/ir.model.access.csv',

        # Archivo XML con las vistas, menús y acciones del modelo
        'views/views.xml',
    ]
}

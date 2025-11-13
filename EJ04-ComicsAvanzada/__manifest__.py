# -*- coding: utf-8 -*-
{
    # ===============================
    # Información básica del módulo
    # ===============================
    'name': "Biblioteca Comics",  # Título que verá el usuario
    'summary': "Gestión de cómics con categorías y autores",  # Resumen corto

    'description': """
Gestor de Biblioteca de Cómics
-------------------------------------------------
- Crea, clasifica y gestiona cómics.
- Soporte para jerarquías de categorías.
- Relación con autores (partners).
- Sistema de archivado lógico.
- Cómputo de días desde lanzamiento.
    """,

    'author': "Sergi García",
    'website': "http://apuntesfpinformatica.es",
    'category': 'Tools',   # Categoría donde se clasifica en la app store de Odoo
    'version': '0.1',      # Versión de desarrollo inicial

    # ===============================
    # Indicamos que es una aplicación completa
    # ===============================
    'application': True,

    # ===============================
    # Dependencias: otros módulos que deben estar instalados
    # ===============================
    'depends': ['base'],  # Módulo base de Odoo

    # ===============================
    # Archivos cargados con el módulo
    # ===============================
    'data': [
        # -----------------------------------------
        # Seguridad: primero se cargan los permisos
        # -----------------------------------------
        'security/ir.model.access.csv',     # Permisos de acceso a los modelos

        # -----------------------------------------
        # Vistas del modelo biblioteca.comic
        # -----------------------------------------
        'views/biblioteca_comic.xml',

        # -----------------------------------------
        # Vistas del modelo biblioteca.comic.categoria
        # -----------------------------------------
        'views/biblioteca_comic_categoria.xml',
    ],
}

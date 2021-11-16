# -*- coding: utf-8 -*-
{
    'name': "Biblioteca Comics",  # Titulo del módulo
    'summary': "Gestionar comics :)",  # Resumen de la funcionaliadad
    'description': """
Gestor de bibliotecas
==============
    """,  

    #Indicamos que es una aplicación
    'application': True,
    'author': "Sergi García",
    'website': "http://apuntesfpinformatica.es",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/biblioteca_comic.xml',
        'views/biblioteca_comic_categoria.xml'
    ],
    # Fichero con data de demo si se inicializa la base de datos con "demo data" (No incluido en ejemplo)
    # 'demo': [
    #     'demo.xml'
    # ],
}

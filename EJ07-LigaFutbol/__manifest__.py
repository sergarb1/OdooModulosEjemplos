# -*- coding: utf-8 -*-
{
    'name': "Gestionar liga de futbol",  # Titulo del módulo
    'summary': "Gestionar una liga de futbol :) (Version avanzada)",  # Resumen de la funcionaliadad
    'description': """
    Gestor de Liga de futbol (Version avanzada)
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
        #'security/groups.xml',
        'security/ir.model.access.csv',
        'views/liga_equipo.xml',
        'views/liga_partido.xml'
    ],
    # Fichero con data de demo si se inicializa la base de datos con "demo data" (No incluido en ejemplo)
    # 'demo': [
    #     'demo.xml'
    # ],
}

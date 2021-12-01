# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigaPartido(models.Model):
    #Nombre y descripcion del modelo
    _name = 'liga.partido'
    _description = 'Un partido de la liga'


    #Atributos del modelo


    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR LOS Many2One en Vistas
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
    #Indicamos que atributo sera el que se usara para mostrar nombre.
    #Por defecto es "name", pero si no hay un atributo que se llama name, aqui lo indicamos
    #Aqui indicamos que se use el atributo "nombre"
    _rec_name = 'nombre'

    #Nombre categoria
    nombre = fields.Char('Nombre partido')

    #Booleano indicando si se ha disputado
    disputado=fields.Boolean()

    #Nombre del equipo que juega en casa casa
    equipo_casa = fields.Many2one(
        'liga.equipo',
        string='Equipo de casa',
    )
    #Goles equipo de casa
    goles_casa= fields.Integer()

    #Nombre del equipo que juega fuera
    equipo_fuera = fields.Many2one(
        'liga.equipo',
        string='Equipo de fuera',
    )
    #Goles equipo de casa
    goles_fuera= fields.Integer()
    
     #Constraints de atributos
    @api.constrains('equipo_casa')
    def _check_mismo_equipo(self):
        for record in self:
            if record.equipo_casa and record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes')


    #API onchange para cuando se modifica un partido
    #Aunque onchange envia un registro, hacemos codigo para recalcular 
    #http://www.geninit.cn/developer/reference/orm.html  
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizoRegistrosEquipo(self):
        #Recorremos partidos y equipos
        for recordEquipo in self.env['liga.equipo'].search([]):
            #Como recalculamos todo, ponemos de cada equipo todo a cero
            recordEquipo.victorias=0
            recordEquipo.empates=0
            recordEquipo.derrotas=0
            recordEquipo.goles_a_favor=0
            recordEquipo.goles_en_contra=0
            
            for recordPartido in self.env['liga.partido'].search([]):  
        
                #Si es el equipo de casa
                if recordPartido.equipo_casa.nombre==recordEquipo.nombre:
                    
                    #Miramos si es victoria o derrota
                    if recordPartido.goles_casa>recordPartido.goles_fuera:
                        recordEquipo.victorias=recordEquipo.victorias+1
                    elif recordPartido.goles_casa<recordPartido.goles_fuera:
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                        
                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_casa
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_fuera

                #Si es el equipo de fuera
                if recordPartido.equipo_fuera.nombre==recordEquipo.nombre:
                    
                    #Miramos si es victoria o derrota
                    if recordPartido.goles_casa<recordPartido.goles_fuera:
                        recordEquipo.victorias=recordEquipo.victorias+1
                    elif recordPartido.goles_casa>recordPartido.goles_fuera:
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                    
                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_fuera
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_casa


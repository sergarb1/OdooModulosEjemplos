# -*- coding: utf-8 -*-
from odoo import models, fields


class LigaEquipoWizard(models.TransientModel):
    _name = 'liga.equipo.wizard'

    nombre = fields.Char()
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)

    def add_liga_equipo(self):
        ligaEquipoModel = self.env['liga.equipo']
        for wiz in self:
            ligaEquipoModel.create({
                'nombre': wiz.nombre,
                'descripcion': wiz.descripcion,
            })

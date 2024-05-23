# -*- coding: utf-8 -*-
from odoo import models, fields, api

class OwlTtodo(models.Model):
    _name = 'owl.todo.list'
    _description = 'Lista de tareas'
    
    #definiendo los campos
    name = fields.Char(string="Tarea", required=True)
    description = fields.Text(String="Descripción") 
    completed = fields.Boolean()
    color = fields.Char()
   # description = fields.Text()

    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100
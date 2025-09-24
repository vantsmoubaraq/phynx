# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class phynx_careers(models.Model):
#     _name = 'phynx_careers.phynx_careers'
#     _description = 'phynx_careers.phynx_careers'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


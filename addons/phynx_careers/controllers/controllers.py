# -*- coding: utf-8 -*-
# from odoo import http


# class PhynxCareers(http.Controller):
#     @http.route('/phynx_careers/phynx_careers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phynx_careers/phynx_careers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('phynx_careers.listing', {
#             'root': '/phynx_careers/phynx_careers',
#             'objects': http.request.env['phynx_careers.phynx_careers'].search([]),
#         })

#     @http.route('/phynx_careers/phynx_careers/objects/<model("phynx_careers.phynx_careers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phynx_careers.object', {
#             'object': obj
#         })


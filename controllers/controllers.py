# -*- coding: utf-8 -*-
# from odoo import http


# class CcbmTransit(http.Controller):
#     @http.route('/ccbm_transit/ccbm_transit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ccbm_transit/ccbm_transit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ccbm_transit.listing', {
#             'root': '/ccbm_transit/ccbm_transit',
#             'objects': http.request.env['ccbm_transit.ccbm_transit'].search([]),
#         })

#     @http.route('/ccbm_transit/ccbm_transit/objects/<model("ccbm_transit.ccbm_transit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ccbm_transit.object', {
#             'object': obj
#         })

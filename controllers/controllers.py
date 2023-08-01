# -*- coding: utf-8 -*-
# from odoo import http


# class WeakestLink(http.Controller):
#     @http.route('/weakest_link/weakest_link/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/weakest_link/weakest_link/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('weakest_link.listing', {
#             'root': '/weakest_link/weakest_link',
#             'objects': http.request.env['weakest_link.weakest_link'].search([]),
#         })

#     @http.route('/weakest_link/weakest_link/objects/<model("weakest_link.weakest_link"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('weakest_link.object', {
#             'object': obj
#         })

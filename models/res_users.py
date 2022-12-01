# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Users(models.Model):
    _inherit = 'res.users'

    # ### Used to log into the system
    # login
    # ### Keep empty if you don't want the user to be able to connect on the system.
    # password
    # ### Specify a value only when creating a user or if you're changing the user's password, otherwise leave empty.
    # ### After a change of password, the user has to login again
    # new_password
    # ### Partner-related data of the user
    # partner_id

    service_id = fields.Many2one('transit.service')
    #responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsable", index=True)
    # service_id = fields.Many2one('transit.service', required=True, ondelete='restrict',
    #                              auto_join=True, index=True, string='Service lie')
    # service_id = fields.Many2many('transit.service', 'res_services_users_rel', 'uid', 'sid', string='Services')
    is_intervener = fields.Boolean(default=True)

    # active = fields.Boolean(default=True)
    # active_partner = fields.Boolean(related='partner_id.active', readonly=True, string="Partner is Active")



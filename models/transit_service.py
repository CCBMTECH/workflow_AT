# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Service(models.Model):
    _name = "transit.service"
    _description = "Service/Department"
    #_inherit = 'hr.department'
    _order = "name"

    name = fields.Char('Service', required=True)
    active = fields.Boolean('Active', default=True)
    manager_id = fields.Many2one('res.users', string='Chef Service',
                                 # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
                                 )

    note = fields.Text('Note')
    color = fields.Integer('Color Index')

    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    parent_id = fields.Many2one('transit.service', string='Service Parent', index=True,
                                # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
                                )
    # intervenants
    # member_ids = fields.Many2many('res.users', 'res_services_users_rel', 'sid', 'uid')
    member_ids = fields.One2many('res.users', 'service_id', string='Intervenants')


    # total_employee = fields.Integer(compute='_compute_total_employee', string='Total Intervenant')
    # company_id = fields.Many2one('res.company', string='Entreprise', index=True, default=lambda self: self.env.company)

    # master_department_id = fields.Many2one(
    #     'hr.department', 'Master Department', compute='_compute_master_department_id', store=True)

    # def _compute_total_employee(self):
    #     emp_data = self.env['hr.employee']._read_group([('department_id', 'in', self.ids)], ['department_id'],
    #                                                    ['department_id'])
    #     result = dict((data['department_id'][0], data['department_id_count']) for data in emp_data)
    #     for department in self:
    #         department.total_employee = result.get(department.id, 0)



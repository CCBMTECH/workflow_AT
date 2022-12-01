from odoo.exceptions import ValidationError
from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    is_client = fields.Boolean('Est Client', default=False)
    cpt_client = fields.Char('Compte Client')
    ppm = fields.Char('code ppm')
    ninea = fields.Char('NINEA')
    cni_passport = fields.Binary('CNI/Passport')
    num_cni_passport = fields.Char('Numero piece', required=True)
    type_piece = fields.Selection(
        [('cni', 'CNI'), ('passport', 'Passport')],
        required=True, index=True)

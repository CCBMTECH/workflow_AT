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

    def _compute_user_transit(self):
        if (self.env.user.has_group('ccbm_transit.group_ccbmtransit_manager')
                | self.env.user.has_group('ccbm_transit.group_ccbmtransit_user')
                | self.env.user.has_group('ccbm_transit.group_ccbmtransit_assistant')
                | self.env.user.has_group('ccbm_transit.group_ccbmtransit_sm')):
            return True

    user_transit = fields.Boolean(default=_compute_user_transit, store=False)

    # Les conditions de paiement
    # property_supplier_payment_term_id

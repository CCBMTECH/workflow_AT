from datetime import timedelta
from itertools import groupby
from markupsafe import Markup

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, format_amount, format_date, html_keep_url, is_html_empty
from odoo.tools.sql import create_index


READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'dga', 'dg', 'transit', 'rl', 'dga_honoraires', 'transit_devis', 'dga_cond_paie', 'dg_devis'}
}
#
LOCKED_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'dga', 'dg', 'transit', 'rl', 'dga_honoraires', 'transit_devis', 'dga_cond_paie', 'dg_devis'}
}


# done == terminé
# cancel == retouner
class Dossier(models.Model):
    _name = "dossier"
    _description = "Dossier"

    # # Pipeline/Circuit
    @api.model
    def _default_transit_stage(self):
        Stage = self.env['transit.stage']
        return Stage.search([], limit=1)

    # === FIELDS ===#

    name = fields.Char('Dossier', required=True, copy=False, readonly=False, index='trigram',
                       #states={'assistant': [('readonly', False)]},
                       #states=READONLY_FIELD_STATES,
                       default=lambda self: _('Identifiant'))
    repertoire = fields.Char('Repertoire', store=True, index=True, tracking=1)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        compute='_compute_user_id',
        store=True, readonly=False, precompute=True, index=True,
        tracking=True,
        # domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
        #      self.env.ref("sales_team.group_sale_salesman").id)
    )

    # user_id = fields.Many2one(
    #     'res.users', string='Intervenant', default=lambda self: self.env.user,
    #     check_company=True, index=True, tracking=True,
    #     domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
    # )
    # le cielnt <client_id>
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Client",
        required=True, readonly=False, change_default=True, index=True,
        tracking=1,
        states=READONLY_FIELD_STATES,
        domain="[('type', '!=', 'note_details'), ('company_id', 'in', (False, company_id))]"
    )

    description = fields.Html('Notes')
    active = fields.Boolean('Active', default=True, tracking=True)
    type = fields.Selection([
        ('dossier', 'Dossier'), ('note_details', 'Note de Details')], required=True, index=True,
        default=lambda self: 'note_details' if self.env['res.users'].has_group(
            'ccbm_transit.group_ccbmtransit_sm') else 'dossier')

    client_ref_id = fields.Char(related='partner_id.client_ref', readonly=True, string="Reference Client")
    ordre_transit = fields.Binary(string='Ordre de Transit OT', store=True)
    connaissement = fields.Char(string='Connaissement', store=True)
    reference = fields.Char(string="Reference Commercial", copy=False)
    assurance = fields.Char(string='Assurance')

    regime = fields.Char(string='Regime')
    num_navire = fields.Char(string='Numero Navire')
    cht_lta = fields.Char(string="CHT | LTA")
    expert = fields.Char(string="Expert")
    destination = fields.Char(string="Destination")
    nb_colis = fields.Integer(string="Nombre de Colis")
    qty_complementary = fields.Char(string='Quantite Complementaire')

    # Masse
    poids_net = fields.Float('Poids Net')
    poids_brut = fields.Float('Poids Brut')

    currency_id = fields.Many2one('res.currency', string='Monnaie')
    honoraires = fields.Monetary(string="Honoraires",  currency_field='currency_id', copy=False)
    amount_negotiate = fields.Monetary(string="Montant Négocié",  currency_field='currency_id', store=True,  tracking=True)
    amount_passer = fields.Monetary(string="Montant Passeur",  currency_field='currency_id', store=True, tracking=True)



    # === Date
    # Date de creation du dossier
    create_date = fields.Datetime(  # Override of default create_date field from ORM
        string="Creation Date", index=True, readonly=True)
    # Date de livraison
    commitment_date = fields.Datetime(string="Date de livraison", copy=False,
                                      states=LOCKED_FIELD_STATES)
    date_closed = fields.Datetime('Closed Date', readonly=True, copy=False)

    # # Pipeline management
    # priority = fields.Selection(
    #     transit_stage.AVAILABLE_PRIORITIES, string='Priority', index=True,
    #     default=transit_stage.AVAILABLE_PRIORITIES[0][0])
    stage_id = fields.Many2one('transit.stage', default=_default_transit_stage)
    color = fields.Integer('Color Index', default=0)

    state = fields.Selection(
        [('assistant', 'Assistant'),
         ('dga', 'GDA contole dossier'),
         ('dg', 'DG valide ddossier'),
         ('transit', 'Transit Droits de douane'),
         ('rl', 'RL Jointure factures '),
         ('dga_honoraires', 'GDA honoraires'),
         ('transit_devis', 'proposition Devis '),
         ('dga_cond_paie', 'DGA cond paie'),
         ('dg_devis', 'DG valide Devis')
         ],
        'State', readonly=True, copy=False, index=True, tracking=3,
        default="assistant")



    # === COMPUTE METHODS ===#
    @api.depends('user_id')
    def _compute_date_open(self):
        for dos in self:
            dos.date_open = self.env.cr.now() if dos.user_id else False

    # @api.model
    # def create(self, vals):
    #     doss = super(Dossier, self).create(vals)
    #     if doss.stage_id.dossier_state:
    #         self.state = doss.stage_id.dossier_state
    #     return doss
    #
    # @api.model
    # def write(self, vals):
    #     doss = super(Dossier, self).write(vals)
    #     if self.stage_id.dossier_state:
    #         self.state = self.stage_id.dossier_state
    #     return doss

    @api.depends('partner_id')
    def _compute_user_id(self):
        for dossier in self:
            if not dossier.user_id:
                dossier.user_id = dossier.partner_id.user_id or dossier.partner_id.commercial_partner_id.user_id or self.env.user

    # === CRUD METHODS ===#

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("Identifiant")) == _("Identifiant"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['create_date']), "%Y"
                ) if 'create_date' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'dossier', sequence_date=seq_date) or _("Identifiant")

        return super().create(vals_list)

    # ===================== Workflow ==================== #
    def action_send(self):

        if self.state == 'assistant':
            self.write({'state': 'dga'})
        if self.state == 'dga':
            self.write({'state': 'dg'})
        if self.state == 'dg':
            self.write({'state': 'transit'})
        if self.state == 'transit':
            self.write({'state': 'rl'})
        if self.state == 'rl':
            self.write({'state': 'dga_honoraires'})
        if self.state == 'dga_honoraires':
            self.write({'state': 'transit_devis'})
        if self.state == 'transit_devis':
            self.write({'state': 'dga_cond_paie'})
        if self.state == 'dga_cond_paie':
            self.write({'state': 'dg_devis'})
        if self.write({'state': 'dg_devis'}):
            self.write({'state': 'assistant'})

        #self.send_notification_to_instructor()

    # def send_notification_to_instructor(self):
    #     # Récupération de l'id du template d'envoi de mail à l'instructure
    #     temp_id = self.env.ref('ccbm.session_instructor').id
    #     # Envoi du mail à l'instructeur
    #     self.env['mail.template'].browse(temp_id).send_mail(self.id, force_send=True)

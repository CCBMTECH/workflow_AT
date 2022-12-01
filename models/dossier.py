from odoo import models, fields, api, _


class Dossier(models.Model):
    _name = "dossier"
    _description = "Dossier"

    # # Pipeline/Circuit
    @api.model
    def _default_transit_stage(self):
        Stage = self.env['transit.stage']
        return Stage.search([], limit=1)

    name = fields.Char('Dossier', required=False, readonly=False, store=True)
    user_id = fields.Many2one(
        'res.users', string='Intervenant', default=lambda self: self.env.user,
        check_company=True, index=True, tracking=True,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
    )
    client_id = fields.Many2one('res.partner', 'Client', required=True)

    referred = fields.Char('Referred By')
    description = fields.Html('Notes')
    active = fields.Boolean('Active', default=True, tracking=True)
    type = fields.Selection([
        ('dossier', 'Dossier'), ('note_details', 'Note de Details')], required=True, index=True,
        default=lambda self: 'note_details' if self.env['res.users'].has_group(
            'ccbm_transit.group_ccbmtransit_sm') else 'dossier')

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
         ('dg_devis', 'DG valide Devis'), ],
        'State', default="assistant")

    # Date
    date_closed = fields.Datetime('Closed Date', readonly=True, copy=False)
    # date_action_last = fields.Datetime('Last Action', readonly=True)
    date_open = fields.Datetime('Assignment Date', compute='_compute_date_open', readonly=True, store=True)
    #
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

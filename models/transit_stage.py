from odoo import api, fields, models, _

AVAILABLE_PRIORITIES = [
    ('0', 'Bas'),
    ('1', 'Moyen'),
    ('2', 'Important'),
    ('3', 'Urgent'),
]


class Stage(models.Model):
    """ Modèle pour les étapes d'un dossier.
        Ce modèle modélise les principales étapes d'un flux de gestion de documents.
        Les principaux objets Africa Transit utiliseront désormais uniquement les étapes,
        au lieu de l'état et des étapes.
        Les étapes sont par exemple utilisées pour afficher la vue kanban des dossiers.
    """
    _name = "transit.stage"
    _description = "Transit Stages"
    _order = "sequence, name, id"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    fold = fields.Boolean('Folded in Circuit',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    requirements = fields.Text('Requirements',
                               help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")

    dossier_state = fields.Selection(
        [('assistant', 'Assistant'),
         ('dga', 'GDA contole dossier'),
         ('dg', 'DG valide ddossier'),
         ('transit', 'Transit Droits de douane'),
         ('rl', 'RL Jointure factures '),
         ('dga_honoraires', 'GDA honoraires'),
         ('transit_devis', 'proposition Devis '),
         ('dga_cond_paie', 'DGA cond paie'),
         ('dg_devis', 'DG valide Devis')],
        'State', default="assistant")



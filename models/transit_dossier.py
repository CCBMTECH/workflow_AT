
from odoo import models, fields, api, _

from models import transit_stage


class Dossier(models.Model):
    _name = "transit.dossier"
    _description = "Dossier"



    # Description
    name = fields.Char('Dossier', required=True, readonly=False, store=True)

    #




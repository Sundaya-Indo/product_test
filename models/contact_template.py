from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Partners(models.Model):
    _inherit = 'res.partner'

    # map = fields.Char(Str="map")
    
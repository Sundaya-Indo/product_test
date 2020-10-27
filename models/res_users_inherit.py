from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Users(models.Model):
    _inherit = 'res.users'

    signature_image = fields.Binary('Signature Image')
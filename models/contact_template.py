from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Partners(models.Model):
    _inherit = 'res.partner'

    # is_employee = fields.Boolean(string='Is an Employee', default="false")
    
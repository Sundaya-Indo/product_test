from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Employees(models.Model):
    _inherit = 'hr.employee'

    # name = fields.Char(string='Label dari Field')
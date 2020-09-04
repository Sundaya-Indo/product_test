from odoo.addons import decimal_precision as dp

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    mrp_qr = fields.Char(string='Item Code', related='product_id.barcode')
    barcode = fields.Char(string='Item Code')
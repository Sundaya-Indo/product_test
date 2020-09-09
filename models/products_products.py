from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode = fields.Char('Item Code', copy=False, oldname='ean13',
        help="International Article Number used for product identification.")
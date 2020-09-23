from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode = fields.Char('Item Code', copy=False, oldname='ean13',)

    total_weight = fields.Float('Total Weight', compute='generate_total_weight', store=True,)

    total_value = fields.Float('Total Value', compute='generate_total_value', store=True,)

    price_gram = fields.Float('Price/gram', compute='generate_price_gram', store=True,)

    @api.depends('weight', 'qty_available')
    def generate_total_weight(self):
        for doc in self:
            doc.total_weight = doc.weight * doc.qty_available

    @api.depends('standard_price', 'qty_available')
    def generate_total_value(self):
        for doc in self:
            doc.total_value = doc.standard_price * doc.qty_available

    @api.depends('standard_price', 'weight')
    def generate_price_gram(self):
        for doc in self:
            if doc.standard_price > 0 and doc.weight > 0:
                doc.price_gram = doc.standard_price / doc.weight
            else:
                pass
                

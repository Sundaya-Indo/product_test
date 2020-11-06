from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode = fields.Char('Item Code', copy=False, oldname='ean13',)
    length = fields.Float(string='Length')
    total_length = fields.Float('Total Length', compute='generate_total_length', store=True,)
    price_meter = fields.Float('Price/Meter', compute='generate_price_meter', store=True,)
    total_weight = fields.Float('Total Weight', compute='generate_total_weight', store=True,)
    total_value = fields.Float('Total Value', compute='generate_total_value', store=True,)
    price_gram = fields.Float('Price/gram', compute='generate_price_gram', store=True,)
    audit_item = fields.Boolean('Audit', default=False)
    audit_qty = fields.Float('Audit Quantity')
    qty_dif = fields.Float('Difference', compute='generate_difference', store=True,)
    

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

    @api.depends('length', 'qty_available')
    def generate_total_length(self):
        for doc in self:
            doc.total_length = doc.length * doc.qty_available
    
    @api.depends('standard_price', 'length')
    def generate_price_meter(self):
        for doc in self:
            if doc.standard_price > 0 and doc.length > 0:
                doc.price_meter = doc.standard_price / doc.length
            else:
                pass

    @api.depends('audit_qty', 'qty_available')
    def generate_difference(self):
        for doc in self:
            doc.qty_dif = doc.audit_qty - doc.qty_available






class ProductAudit(models.Model):
    _name = 'product.audit'

    name = fields.Char('Audit No')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('done', 'Done'),
            ('cancel', 'Cancel')
        ], string='Status', default='draft')

    @api.multi
    def button_approve(self, force=False):
        self.write({'state': 'open', 'date_approve': fields.Date.context_today(self)})
        return {}

                

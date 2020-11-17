from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp
import datetime

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
    last_product_audit = fields.Date(string='Audit Date',)
    

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



class ProductAudit(models.Model):
    _name = 'product.audit'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    READONLY_STATES = {
        'open': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    name = fields.Char('Audit No')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('done', 'Done'),
            ('cancel', 'Cancel')
        ], string='Status', default='draft')
    audit_date_order = fields.Date('Order Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', 'Auditor', store=True)
    user_id = fields.Many2one('res.users', 'Approved By', store=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.user.company_id.id)
    order_line = fields.One2many('product.audit.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    product_id = fields.Many2one('product.product', related='order_line.product_id', string='Product', readonly=False)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.user.company_id.id)
    date_done = fields.Date('Date Finished', readonly=1, index=True, copy=False, store=True,)

    @api.multi
    def button_approve(self, force=False):
        self.write({'state': 'open', 'audit_date_order': fields.Date.context_today(self)})
        return {}

    @api.multi
    def button_done(self, force=False):
        self.write({'state': 'done', 'date_done': fields.Date.context_today(self)})

class ProductAuditLine(models.Model):
    _name = 'product.audit.line'
    _description = 'Product Audit line'

    name = fields.Text(string='Description')
    order_id = fields.Many2one('product.audit', string='Audit Reference', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True, required=True)
    partner_id = fields.Many2one('res.partner', related='order_id.partner_id', string='Partner', readonly=True, store=True)
    company_id = fields.Many2one('res.company', related='order_id.company_id', string='Company', store=True, readonly=True)
    state = fields.Selection(related='order_id.state', store=True, readonly=False)
    product_qty = fields.Float(related='product_id.qty_available', digits=dp.get_precision('Product Unit of Measure'))
    product_uom = fields.Many2one(related='product_id.uom_id', string='Unit of Measure')
    item_code = fields.Char(related='product_id.barcode', string='Item Code')
    image_small_id = fields.Binary(related='product_id.image_small', string='Image Small', compute='_compute_images', inverse='_set_image_small')
    audit_qty = fields.Float(string='Audit Quantity', digits=dp.get_precision('Product Unit of Measure'))
    rel_date_done = fields.Date(related='order_id.date_done')
    difference_qty = fields.Float(string='Difference Quantity', compute='generate_difference', digits=dp.get_precision('Product Unit of Measure'))
    last_audit_date = fields.Date(string='Audit Date')
    days_difference = fields.Integer(string='Days Difference', store=True)
    last_audited = fields.Char(string='Last Audit',)

    @api.depends('audit_qty', 'product_qty')
    def generate_difference(self):
        for doc in self:
            doc.difference_qty = doc.audit_qty - doc.product_qty

    @api.onchange
    def generate_date_done(self):
        for doc in self:
            temp = doc.rel_date_done
            doc.last_audit_date = temp

    # @api.depends('last_product_audit')
    # def generate_days_diff(self):
    #     for doc in self:
    #         doc.days_difference = (datetime.datetime.now() - doc.last_product_audit).days
            
    # @api.depends('days_difference')
    # def generate_last_audit(self):
    #     for doc in self:
    #         doc.last_audited =  str(doc.days_difference) + " Days ago"    

                

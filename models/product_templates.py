from odoo.addons import decimal_precision as dp

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sample_product = fields.Boolean('Sample', default=True)
    stock_product = fields.Boolean('Stock', default=False)
    asset_product = fields.Boolean('Asset', default=False)
    item_type = fields.Char(string='Item Type')
    item_brand = fields.Char(string='Brand')
    long_desc = fields.Char(string='Description')
    # qr_code = fields.Char(string='QR Code')

    # stock_total_value = fields.Float(
    #     digits = dp.get_precision('Product Price'),
    #     string='Stock Value', compute='hitung', store=True,)

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', store=True,)

    # stock_value_ids = fields.Many2one('product.product', 'Value ID')
    # kanban_stock_value = fields.Float(string='Value', related='stock_value_ids.stock_value')

    # @api.depends('qty_available','standard_price')
    # def hitung(self):
    #     for doc in self:
    #         doc.stock_total_value = doc.standard_price * doc.qty_available

    file_datasheet = fields.Many2many(
        comodel_name="ir.attachment",
        relation="m2m_ir_file_datasheet",
        column1="m2m_id",
        column2="attachment_id",
        string="Datasheet File")

    weblinks = fields.Many2many(comodel_name="ir.attachment",
        relation="m2m_ir_file_weblinks",
        column1="m2m_id",
        column2="attachment_id",
        string="Weblinks")






     


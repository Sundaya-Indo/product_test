from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    qr_code = fields.Char(string='QR Code', related='product_id.barcode')
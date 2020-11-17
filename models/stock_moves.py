from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    qr_code = fields.Char(string='Item Code', related='product_id.barcode')
    image_small_id = fields.Binary(related='product_id.image_small', string='Image Small', compute='_compute_images', inverse='_set_image_small')
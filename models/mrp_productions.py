from odoo.addons import decimal_precision as dp

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    mrp_qr = fields.Char(string='Item Code', related='product_id.barcode')
    barcode = fields.Char(string='Item Code')
    image_small_id = fields.Binary(related='product_id.image_small', string='Image', compute='_compute_images', inverse='_set_image_small')
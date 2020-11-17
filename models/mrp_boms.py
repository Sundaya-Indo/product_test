from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, pycompat

from itertools import groupby

class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    image_small_id = fields.Binary(related='product_tmpl_id.image_small', string='Image Small', compute='_compute_images', inverse='_set_image_small')


class MrpBomLine(models.Model):

    _inherit = 'mrp.bom.line'

    image_small_id = fields.Binary(related='product_id.image_small', string='Image Small', compute='_compute_images', inverse='_set_image_small')


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    product_id = fields.Many2one('product.product', 'Product D')


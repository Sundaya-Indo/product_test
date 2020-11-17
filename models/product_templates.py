from odoo.addons import decimal_precision as dp

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)
import base64
import io
try:
    import qrcode

except ImportError:
    _logger.debug('ImportError')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    name = fields.Char('Name', index=True, required=True, translate=True, size=20)
    sample_product = fields.Boolean('Sample', default=True)
    stock_product = fields.Boolean('Stock', default=False)
    asset_product = fields.Boolean('Asset', default=False)
    item_type = fields.Char(string='Item Type')
    item_brand = fields.Char(string='Brand')
    long_desc = fields.Char(string='Description')
    barcode = fields.Char(string='Item Code', size=6,)
        # default= lambda self:_('New'), track_visibility='onchange',)

    # stock_total_value = fields.Float(
    #     digits = dp.get_precision('Product Price'),
    #     string='Stock Value', compute='hitung', store=True,)

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', store=True,)
    rel_warehouse_code = fields.Char(string='Warehouse ID', related='warehouse_id.code')
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
    

    qr_code = fields.Binary('QR Code', compute="_generate_qr_code")
    audit_id = fields.Many2one('product.audit', store=True,)
    rel_audit_done = fields.Date(related='audit_id.date_done',)

    @api.one
    @api.depends('barcode')
    def _generate_qr_code(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
        if self.barcode :
            qr.add_data(self.barcode)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qrcode_img = base64.b64encode(buffer.getvalue())
            self.update({'qr_code': qrcode_img,})

    # @api.model
    # def create(self, vals):
    #         if vals:
    #             vals['barcode'] = self.env['ir.sequence'].next_by_code('barcode.increment') or _('New')
    #             return super(ProductTemplate, self).create(vals)

    



     


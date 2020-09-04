from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
import base64
import io
try:
    import qrcode

except ImportError:
    _logger.debug('ImportError')

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    # additional_attribute = fields.Selection([
    #     ('ehub', 'Ehub'),
    #     ('epack', 'Epack')], string='Additional')

    # raspi_id = fields.Char('Raspi ID')
    # raspi_uid = fields.Char('Raspi UID')
    # dc_board_serial = fields.Char('DC Board Serial')
    # led_board_serial = fields.Char('LED Board Serial')
    # bbc_main_board = fields.Char('DC Board Serial')
    # qc_pass_date = fields.Char('QC Pass Date')
    # asset_loc = fields.Many2one(
    #     comodel_name='crm.lead',
    #     string='Asset Location'
    #     )
    # ip_raspi_backup = fields.Char('IP Raspi Backup')
    # ip_bbc_backup = fields.Char('IP BBC Backup')
    # ip_raspi_site = fields.Char('IP Raspi Site')
    # ip_bbc_site = fields.Char('IP BBC Site')
    # no_js = fields.Char('No JS')

    # testinvis2 = fields.Char('Test')

    # @api.onchange('testbool')
    # def _select_add(self):
    #     if self.testbool:
    #         self.testbool = True
    #     else:
    #         self.testbool = False

    # @api.onchange('additional_attribute')
    # def _select_add(self):
    #     if self.additional_attribute:
    #         self.additional_attribute == 'ehub'
    #     elif self.additional_attribute:
    #         self.additional_attribute == 'epack'

    qr_code = fields.Binary('QR Code', compute="_generate_qr_code")

    @api.one
    @api.depends('refe')
    def _generate_qr_code(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
        if self.refe :
            qr.add_data(self.refe)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qrcode_img = base64.b64encode(buffer.getvalue())
            self.update({'qr_code': qrcode_img,})

    product_qr = fields.Char(string='QR Code', related='product_id.barcode')

    @api.depends('refe')
    def _combine_qr_serial(self):
        temp = self.product_qr
        temp1 = self.name
        self.refe = str(temp) + "-" + str(temp1)

    refe = fields.Char('Serial QR Core', compute="_combine_qr_serial")
            
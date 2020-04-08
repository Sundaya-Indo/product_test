from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Partners(models.Model):
    _inherit = 'res.partner'

    # map = fields.Char(Str="map")

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
    
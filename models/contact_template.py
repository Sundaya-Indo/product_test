from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Partners(models.Model):
    _inherit = 'res.partner'

    file_datasheet_partner = fields.Many2many(
        comodel_name="ir.attachment",
        relation="m2m_ir_file_datasheet_partner",
        column1="m2m_id",
        column2="attachment_id",
        string="Datasheet File")

    weblinks_partner = fields.Many2many(comodel_name="ir.attachment",
        relation="m2m_ir_file_weblinks_partner",
        column1="m2m_id",
        column2="attachment_id",
        string="Weblinks")

    # is_employee = fields.Boolean('Is an Employee', default=False)
    
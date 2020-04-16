from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Leads(models.Model):
    _inherit = 'crm.lead'

    file_datasheet_lead = fields.Many2many(
        comodel_name="ir.attachment",
        relation="m2m_ir_file_datasheet_lead",
        column1="m2m_id",
        column2="attachment_id",
        string="Datasheet File")

    weblinks_lead = fields.Many2many(comodel_name="ir.attachment",
        relation="m2m_ir_file_weblinks_lead",
        column1="m2m_id",
        column2="attachment_id",
        string="Weblinks")
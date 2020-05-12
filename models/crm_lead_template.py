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

    # marker_color_crm = fields.Char(
    #     string='Marker Color', default='red', required=True)
    
    sales_rep = fields.Many2one('res.partner', 'Sales Representative')
    technical_sup = fields.Many2one('res.partner', 'Technical Support')
    referred_by = fields.Many2one('res.partner', 'Referred By')

    marker_color_crm = fields.Selection([ ('red', 'Official Agent'),('yellow', 'New Lead'),('orange', 'Freelance Agent'),
        ('lime', 'Target Lead'),('deep-sky-blue', 'Under Construction'),('blue', 'Operational Site'),],'Location Status', default='red')
    
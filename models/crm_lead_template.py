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
    lead_ref = fields.Char(string="Lead Reference", readonly=True, required=True, copy=False, default=lambda self:_('New'), track_visibility='onchange')
    @api.model
    def create(self, vals):
        if vals:
            vals['lead_ref'] = self.env['ir.sequence'].next_by_code('lead.ref') or _('New')
        result = super(Leads, self).create(vals)
        return result

    marker_color_crm = fields.Selection([ ('red', 'Official Agent'),('orange', 'Freelance Agent'),('yellow', 'New Lead'),
        ('lime', 'Target Lead'),('deep-sky-blue', 'Under Construction'),('blue', 'Operational Site'),],'Location Status', default='yellow')
    
    bbc_id = fields.Many2one(
        comodel_name='stock.production.lot',
        string='Ehub Serial'
        )

    harvest_rat = fields.Float(string="Harvest Ratio")
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    data = fields.Binary(string='data', compute='get_datas')
    
    @api.depends('datas',)
    def get_datas(self):
        for item in self:
            item.data = item.datas
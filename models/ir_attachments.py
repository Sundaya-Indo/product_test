from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    data = fields.Binary(string='data', compute='get_datas')
    
    @api.depends('datas',)
    def get_datas(self):
        for item in self:
            item.data = item.datas

    file_extension = fields.Char(string='File Type', compute='check_file')

    @api.onchange('name')
    def check_file(self):
        for ext in self:
            if ext.name:
                temp = ext.name.split('.')[-1:]
                ext.file_extension = temp[0]
            else:
              pass

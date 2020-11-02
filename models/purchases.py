from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # delivery_date = fields.Datetime('Delivery Date', default=fields.Datetime.now)
    shipping_mode = fields.Selection([ ('by_air', 'By Air'),('by_sea', 'By Sea'),('by_courier', 'By Courier')],'Shipping Mode', default='by_courier')
    res_user_id = fields.Many2one('res.users', compute='sign_po', store=True)
    current_user = fields.Many2one('res.users', 'Current User')

    @api.multi
    def sign_po(self):
        for doc in self:
            if doc.state == 'draft' or doc.state == 'purchase':
                temp = self.env.uid
                doc.res_user_id = temp
            else:
                pass




    
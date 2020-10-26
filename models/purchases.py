from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # delivery_date = fields.Datetime('Delivery Date', default=fields.Datetime.now)
    shipping_mode = fields.Selection([ ('by_air', 'By Air'),('by_sea', 'By Sea'),('by_courier', 'By Courier')],'Shipping Mode', default='by_courier')
    res_user_id = fields.Many2one('res.users', store=True)
    
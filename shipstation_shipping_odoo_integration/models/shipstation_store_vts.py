from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError,Warning

class shipstation_store_vts(models.Model):
    _name='shipstation.store.vts'
    _rec_name='store_name'
    
    store_id = fields.Char(string='Store Id')
    store_name = fields.Char(string='Store Name')
    marketplace_id = fields.Char(string='MarkerPlace Id')
    marketplace_name = fields.Char(string='MarkerPlace Name')
    acc_number = fields.Char(string='Account Number')
    warehouse_id = fields.Many2one("stock.warehouse", "Warehouse")



    
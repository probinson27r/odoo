from odoo import models, fields, api
import datetime


class ShipstationDeliveryCarrierService(models.Model):
    _name = "shipstation.delivery.carrier.service"
    
    name = fields.Char(string='Service Provider Name')
    service_code = fields.Char(string='Service Code')
    service_nature = fields.Selection([('domestic','Domestic'),('international','International')],string='Service Nature')
    delivery_carrier_id = fields.Many2one('shipstation.delivery.carrier',string='Carrier Code')
    residential_address = fields.Boolean(string='Residential Address',default=False)

from odoo import models, fields, api
import datetime


class ShipstationDeliveryCarrier(models.Model):
    _name = "shipstation.delivery.carrier"
    
    name = fields.Char(string='Carrier Name')
    code = fields.Char(string='Carrier Code')
    account_number = fields.Char(string='Account Number')
    shipping_provider_id = fields.Char(string='Shipping Provide Id')
    provider_tracking_link = fields.Char(string="Provider Tracking Link",
                                help="Tracking link(URL) useful to track the shipment or package from this URL.",
                                size=256)


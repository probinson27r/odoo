from odoo import models, fields, api

class ShipstationDeliveryPackage(models.Model):
    _name = "shipstation.delivery.package"

    name = fields.Char(string='Package Name')
    package_code= fields.Char(string='Package Code')
    service_nature = fields.Selection([('domestic','Domestic'),('international','International')],string='Service Nature')
    delivery_carrier_id = fields.Many2one('shipstation.delivery.carrier',string='Carrier Code')
    height=fields.Float("Height",default=0.0)
    width = fields.Float("Width",defult=0.0)
    length = fields.Float("Length",default=0.0)


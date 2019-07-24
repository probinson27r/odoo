from odoo import models, fields, api
import datetime


class ShipstationOperationDetail(models.Model):
    _name = "shipstation.operation.detail"
    _order = 'id desc'
    _inherit = ['mail.thread']

    name = fields.Char("Name")
    shipstation_operation = fields.Selection([('store', 'store'),
                                              ('delivery_carrier','Delivery Carrier'),
                                              ('carrier_package', 'Carrier Package'),
                                              ('carrier_service','Delivery Carrier Service')
                                    #('sale', 'Sales'),
                                    #('delivery_order', 'Delivery Order'),
                                    #('warehouse', 'Warehouse'),
                                    #('stock', 'Stock'),
                                    #('other', 'Other')
], string="Shipstation Operation")
    shipstation_operation_type = fields.Selection([('export', 'Export'),
                                       ('import', 'Import'),
                                       ('update', 'Update'),
                                       ('delete', 'Cancel / Delete')], string="Shipstation Operation Type")
    warehouse_id = fields.Many2one("stock.warehouse", "Warehouse")
    company_id = fields.Many2one("res.company", "Company")
    operation_ids = fields.One2many("shipstation.operation.details", "operation_id", string="Operation")
    shipstation_message = fields.Char("Message")

    @api.model
    def create(self, vals):
        sequence = self.env.ref("shipstation_shipping_odoo_integration.seq_shipstation_operation_detail")
        name = sequence and sequence.next_by_id() or '/'
        company_id = self._context.get('company_id', self.env.user.company_id.id)
        if type(vals) == dict:
            vals.update({'name': name, 'company_id': company_id})
        return super(ShipstationOperationDetail, self).create(vals)


class ShipstationOperationDetails(models.Model):
    _name = "shipstation.operation.details"
    _rec_name = 'operation_id'
    _order = 'id desc'
    operation_id = fields.Many2one("shipstation.operation.detail", "details")

    shipstation_operation = fields.Selection([('store', 'store'),
                                              ('delivery_carrier','Delivery Carrier'),
                                              ('carrier_service','Delivery Carrier Service'),
                                              ('carrier_package', 'Carrier Package')
                                    #('delivery_order', 'Delivery Order'),
                                    #('warehouse', 'Warehouse'),
                                    #('stock', 'Stock'),
                                    #('other', 'Other')
    ], string="Shipstation Operation")
    shipstation_operation_type = fields.Selection([('export', 'Export'),
                                       ('import', 'Import'),
                                       ('update', 'Update'),
                                       ('delete', 'Cancel / Delete')], string="Shipstation Operation Type")

    warehouse_id = fields.Many2one("stock.warehouse", "Warehouse", related="operation_id.warehouse_id")
    company_id = fields.Many2one("res.company", "Company")
    shipstation_request_message = fields.Char("Request Message")
    shipstation_response_message = fields.Char("Response Message")
    fault_operaion = fields.Boolean("Fault Operation", default=False)

    
    @api.model
    def create(self, vals):
        if type(vals) == dict:
            operation_id = vals.get('operation_id')
            operation = operation_id and self.env['shipstation.operation.detail'].browse(operation_id) or False
            company_id = operation and operation.company_id.id or self.env.user.company_id.id
            vals.update({'company_id': company_id})
        return super(ShipstationOperationDetails, self).create(vals)

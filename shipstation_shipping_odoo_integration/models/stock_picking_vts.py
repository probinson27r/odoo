from odoo import fields,models,api,_
import binascii
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipstation_order_id = fields.Char(string="Shipstation Order ID",copy=False)
    shipstation_order_key=fields.Char(string="Shipstation Order Key",copy=False)
    shipstation_shipment_id=fields.Char(string="Shipstation Order Key",copy=False)

    def update_order_in_shipstation(self):
        self.ensure_one()
        if not self.carrier_id:
            raise ValidationError("Please set proper delivery method")
        try:
            body=self.carrier_id and self.carrier_id.create_or_update_order(self)
            response_data=self.carrier_id and self.carrier_id.api_calling_function("/orders/createorder", body)
            if response_data.status_code == 200:
                responses = response_data.json()
                order_id = responses.get('orderId')
                order_key = responses.get('orderKey')
                if order_id:
                    self.shipstation_order_id = order_id
                    self.shipstation_order_key = order_key
            else:
                error_code = "%s" % (response_data.status_code)
                error_message = response_data.reason
                error_detail = {'error': error_code + " - " + error_message + " - "}
                if response_data.json():
                    error_detail = {'error': error_code + " - " + error_message + " - %s"%(response_data.json())}
                raise ValidationError(error_detail)
        except Exception as e:
            raise ValidationError(e)

    def generate_label_from_shipstation(self):
        self.ensure_one()
        if not self.carrier_id:
            raise ValidationError("Please set proper delivery method")
        try:
            body=self.carrier_id and self.carrier_id.generate_label_from_shipstation(self)
            body.update( {"orderId" : self.shipstation_order_id} )
            response_data=self.carrier_id and self.carrier_id.api_calling_function("/orders/createlabelfororder", body)
            if response_data.status_code == 200:
                responses = response_data.json()
                shipment_id = responses.get('shipmentId')
                if shipment_id:
                    self.shipstation_shipment_id=shipment_id
                    label_data=responses.get('labelData')
                    tracking_number = responses.get('trackingNumber')
                    if tracking_number:
                        self.carrier_tracking_ref = tracking_number
                    base_data = binascii.a2b_base64(str(label_data))
                    mesage_ept = (_("Shipstation Tracking Number: </b>%s") % (tracking_number))
                    self.message_post(body=mesage_ept, attachments=[('%s_Shipstation_Tracking_%s.pdf' % (self.name ,tracking_number), base_data)])
            else:
                error_code = "%s" % (response_data.status_code)
                error_message = response_data.reason
                error_detail = {'error': error_code + " - " + error_message + " - "}
                if response_data.json():
                    error_detail = {'error': error_code + " - " + error_message + " - %s"%(response_data.json())}
                raise ValidationError(error_detail)
        except Exception as e:
            raise ValidationError(e)

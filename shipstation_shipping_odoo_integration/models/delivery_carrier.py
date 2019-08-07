import base64
import simplejson as json
from datetime import datetime
from requests import request
import time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    shipstation_carrier_id = fields.Many2one('shipstation.delivery.carrier', string='Shipstation Carrier')
    shipstation_delivery_carrier_service_id = fields.Many2one('shipstation.delivery.carrier.service',
                                                              string='Shipstation Delivey Carrier Service')
    delivery_type = fields.Selection(selection_add=[('shipstation', 'Shipstation')])
    delivery_package_id = fields.Many2one('shipstation.delivery.package', string='Shipstation Package Code')
    weight_uom = fields.Selection([('pounds', 'pounds'), ('ounces', 'ounces'), ('grams', 'grams')], default="pounds",
                                  string='Weight UOM')
    shipstation_dimentions = fields.Selection([('inches', 'inches'), ('centimeters', 'centimeters')], default="inches",
                                              string='Shipstation Dimentions')
    confirmation = fields.Selection(
        [('none', 'None'), ('delivery', 'Delivery'), ('signature', 'Signature'), ('adult_signature', 'adult_signature'),
         ('direct_signature', 'direct_signature')], default="none",
        string='Shipstation Confirmation')
    store_id = fields.Many2one('shipstation.store.vts', "Store")

    def check_order_data(self, order):
        lines_without_weight = order.order_line.filtered(
            lambda line_item: not line_item.product_id.type in ['service',
                                                                'digital'] and not line_item.product_id.weight and not line_item.is_delivery)
        for order_line in lines_without_weight:
            return _("Please define weight in product : \n %s") % order_line.product_id.name
        receiver_address = order.partner_shipping_id
        serder_address = order.warehouse_id.partner_id
        if not receiver_address.zip or not receiver_address.country_id or not receiver_address.city:
            return _("Please define proper receiver address.")
        if not serder_address.zip or not serder_address.country_id or not serder_address.city:
            return _("Please define proper receiver address.")

        return False

    @api.multi
    def api_calling_function(self, url_data, body):
        configuration = self.env['shipstation.odoo.configuration.vts'].search([], limit=1)
        if not configuration:
            raise ValidationError("Configuration Not Done.")
        url = configuration.making_shipstation_url(url_data)
        api_secret = configuration.api_secret
        api_key = configuration.api_key
        data = "%s:%s" % (api_key, api_secret)
        encode_data = base64.b64encode(data.encode("utf-8"))
        authrization_data = "Basic %s" % (encode_data.decode("utf-8"))
        headers = {"Authorization": authrization_data,
                   "Content-Type": "application/json"}
        data = json.dumps(body)
        _logger.info("Request Data: %s" % (data))
        try:
            response_body = request(method='POST', url=url, data=data, headers=headers)
        except Exception as e:
            raise ValidationError(e)
        return response_body

    @api.multi
    def shipstation_rate_shipment(self, order):
        checked_order_data = self.check_order_data(order)
        if checked_order_data:
            return {'success': False, 'price': 0.0, 'error_message': checked_order_data,
                    'warning_message': False}
        receiver_address = order.partner_shipping_id
        serder_address = order.warehouse_id.partner_id

        weight = sum(
            [(line.product_id.weight * line.product_uom_qty) for line in order.order_line if not line.is_delivery])

        pound_for_kg = 2.20462
        ounce_for_kg = 35.274
        grams_for_kg = 1000
        if self.weight_uom == "pounds":
            total_weight = weight
        elif self.weight_uom == "ounces":
            total_weight = weight
        else:
            total_weight = weight

        # https://ssapi.shipstation.com/shipments/getrates
        dict_rate = {
            "carrierCode": "%s" % (
            self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.delivery_carrier_id and self.shipstation_delivery_carrier_service_id.delivery_carrier_id.code),
            "serviceCode": "%s" % (
            self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.service_code),
            "packageCode": "%s" % (self.delivery_package_id and self.delivery_package_id.package_code),
            "fromPostalCode": "%s" % (serder_address.zip),
            "toState": "%s" % (receiver_address.state_id and receiver_address.state_id.code),
            "toCountry": "%s" % (receiver_address.country_id and receiver_address.country_id.code),
            "toPostalCode": "%s" % (receiver_address.zip),
            "toCity": receiver_address.city,
            "weight": {
                "value": total_weight,
                "units": self.weight_uom or "pounds"
            },
            "dimensions": {
                "units": self.shipstation_dimentions or "inches",
                "length": self.delivery_package_id and self.delivery_package_id.length or 0.0,
                "width": self.delivery_package_id and self.delivery_package_id.width or 0.0,
                "height": self.delivery_package_id and self.delivery_package_id.height or 0.0
            },
            "confirmation": self.confirmation or "none",
            "residential": self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.residential_address
        }
        try:

            response_data = self.api_calling_function("/shipments/getrates", dict_rate)

            if response_data.status_code == 200:
                responses = response_data.json()
                _logger.info("Response Data: %s" % (responses))
                for response in responses:
                    if self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.service_code == response.get(
                            'serviceCode'):
                        service_cost = response.get('shipmentCost')
                        return {'success': True, 'price': float(service_cost or 0.0), 'error_message': False,
                                'warning_message': False}
                    else:
                        return {'success': False, 'price': 0.0, 'error_message': "Service Not Supported.",
                                'warning_message': False}

            else:
                error_code = "%s" % (response_data.status_code)
                error_message = response_data.reason
                error_detail = {'error': error_code + " - " + error_message + " - "}
                return {'success': False, 'price': 0.0, 'error_message': error_detail,
                        'warning_message': False}
        except Exception as e:
            return {'success': False, 'price': 0.0, 'error_message': e,
                    'warning_message': False}

    def generate_label_from_shipstation(self, picking):
        picking_receiver_id = picking.partner_id
        picking_sender_id = picking.picking_type_id.warehouse_id.partner_id
        total_value = sum([(line.product_uom_qty * line.product_id.list_price) for line in picking.move_lines])
        weight = picking.shipping_weight
        pound_for_kg = 2.20462
        ounce_for_kg = 35.274
        grams_for_kg = 1000
        if self.weight_uom == "pounds":
            total_weight = round(weight * pound_for_kg, 3)
        elif self.weight_uom == "ounces":
            total_weight = round(weight * ounce_for_kg, 3)
        else:
            total_weight = round(weight * grams_for_kg, 3)
        request_data = {
            "carrierCode": "%s" % (
            self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.delivery_carrier_id and self.shipstation_delivery_carrier_service_id.delivery_carrier_id.code),
            "serviceCode": "%s" % (
            self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.service_code),
            "packageCode": "%s" % (self.delivery_package_id and self.delivery_package_id.package_code or ""),
            "confirmation": self.confirmation or "none",
            "shipDate": "%s" % (time.strftime("%Y-%m-%d")),
            "weight": {
                "value": total_weight,
                "units": self.weight_uom or "pounds",
            },
            "dimensions": {
                "units": self.shipstation_dimentions or "inches",
                "length": self.delivery_package_id and self.delivery_package_id.length or 0.0,
                "width": self.delivery_package_id and self.delivery_package_id.width or 0.0,
                "height": self.delivery_package_id and self.delivery_package_id.height or 0.0
            },
            "shipFrom": {
                "name": "%s" % (picking_sender_id.name),
                "company": "",
                "street1": "%s" % (picking_sender_id.street or ""),
                "street2": "%s" % (picking_sender_id.street2 or ""),
                "city": "%s" % (picking_sender_id.city or ""),
                "state": "%s" % (picking_sender_id.state_id and picking_sender_id.state_id.code or ""),
                "postalCode": "%s" % (picking_sender_id.zip or ""),
                "country": "%s" % (picking_sender_id.country_id and picking_sender_id.country_id.code or ""),
                "phone": "%s" % (picking_sender_id.phone or ""),
                "residential": self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.residential_address
            },
            "shipTo": {
                "name": "%s" % (picking_receiver_id.name),
                "company": "",
                "street1": "%s" % (picking_receiver_id.street or ""),
                "street2": "%s" % (picking_receiver_id.street2 or ""),
                "city": "%s" % (picking_receiver_id.city or ""),
                "state": "%s" % (picking_receiver_id.state_id and picking_receiver_id.state_id.code or ""),
                "postalCode": "%s" % (picking_receiver_id.zip or ""),
                "country": "%s" % (picking_receiver_id.country_id and picking_receiver_id.country_id.code or ""),
                "phone": "%s" % (picking_receiver_id.phone or ""),
                "residential": self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.residential_address
            },
        }
        return request_data

    def get_order_item_details(self, picking):
        res = []
        count = 0
        for move_line in picking.move_lines:
            count = count + 1
            item_dict = {
                "lineItemKey": "%s" % (count),
                "sku": "%s" % (move_line.product_id and move_line.product_id.default_code),
                "name": "%s" % (move_line.product_id and move_line.product_id.name),
                "weight": {
                            "value": "%s" % (move_line.product_id and move_line.product_id.weight),
                            "units": self.weight_uom or "pounds"
                          },
                "quantity": int(move_line.product_uom_qty),
                "unitPrice": "%s" % (move_line.product_id and move_line.product_id.lst_price),
                "productId": "%s" % (move_line.product_id and move_line.product_id.id)}
            res.append(item_dict)
        return res

    def create_or_update_order(self, picking):
        if not self.store_id:
            raise ValidationError("Store Not Configured!")
        picking_receiver_id = picking.partner_id
        picking_sender_id = picking.picking_type_id.warehouse_id.partner_id
        total_value = sum([(line.product_uom_qty * line.product_id.list_price) for line in picking.move_lines])
        weight = picking.shipping_weight
        pound_for_kg = 2.20462
        ounce_for_kg = 35.274
        grams_for_kg = 1000
        if self.weight_uom == "pounds":
            total_weight = round(weight * pound_for_kg, 3)
        elif self.weight_uom == "ounces":
            total_weight = round(weight * ounce_for_kg, 3)
        else:
            total_weight = round(weight * grams_for_kg, 3)
        date_order = picking.scheduled_date
        if date_order:
            order_date_formate =datetime.strptime(str(date_order), "%Y-%m-%d %H:%M:%S")
            order_date = order_date_formate.strftime('%Y-%m-%dT%H:%M:%S')
            request_data = {
                "orderNumber": "%s" % (picking.name),
                "orderDate": "%s" % (order_date),
                "shipByDate": "%s" % (order_date),
                "orderStatus": "awaiting_shipment",
                "customerUsername": "%s" % (picking_receiver_id.name),
                "customerEmail": "%s" % (picking_receiver_id.email),
                "billTo": {
                    "name": "%s" % (picking_receiver_id.name),
                    "company": "",
                    "street1": "%s" % (picking_receiver_id.street),
                    "street2": "%s" % (picking_receiver_id.street2),
                    "city": "%s" % (picking_receiver_id.city),
                    "state": "%s" % (picking_receiver_id.state_id and picking_receiver_id.state_id.code),
                    "postalCode": "%s" % (picking_receiver_id.zip),
                    "country": "%s" % (picking_receiver_id.country_id and picking_receiver_id.country_id.code or ""),
                    "phone": "%s" % (picking_receiver_id.phone),
                    "residential": self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.residential_address
                },
                "shipTo": {
                    "name": "%s" % (picking_receiver_id.name),
                    "company": "",
                    "street1": "%s" % (picking_receiver_id.street),
                    "street2": "%s" % (picking_receiver_id.street2),
                    "city": "%s" % (picking_receiver_id.city),
                    "state": "%s" % (picking_receiver_id.state_id and picking_receiver_id.state_id.code),
                    "postalCode": "%s" % (picking_receiver_id.zip),
                    "country": "%s" % (picking_receiver_id.country_id and picking_receiver_id.country_id.code),
                    "phone": "%s" % (picking_receiver_id.phone),
                    "residential": self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.residential_address
                },
                "items": self.get_order_item_details(picking),
                "amountPaid": total_value,
                "shippingAmount": 0.0,
                "carrierCode": "%s" % (self.shipstation_carrier_id and self.shipstation_carrier_id.code),
                "serviceCode": "%s" % (
                self.shipstation_delivery_carrier_service_id and self.shipstation_delivery_carrier_service_id.service_code),
                "packageCode": "%s" % (self.delivery_package_id and self.delivery_package_id.package_code or ""),
                "confirmation": self.confirmation or "none",
                "shipDate": "%s" % (order_date),
                "weight": {
                    "value": total_weight,
                    "units": "%s" % (self.weight_uom)
                },
                "dimensions": {
                    "units": "%s" % (self.shipstation_dimentions),
                    "length": self.delivery_package_id and self.delivery_package_id.length or 0.0,
                    "width": self.delivery_package_id and self.delivery_package_id.width or 0.0,
                    "height": self.delivery_package_id and self.delivery_package_id.height or 0.0,
                },
                "insuranceOptions": {
                    "provider": "%s" % (self.shipstation_carrier_id and self.shipstation_carrier_id.code),
                    "insureShipment": False,
                    "insuredValue": 0
                },
                # "internationalOptions": {
                #     "contents": picking.name,
                #     "customsItems": ""
                # },
                "advancedOptions": {
                    # TODO We need to send when import wh from shipstation "warehouseId": ,
                    "storeId": self.store_id and self.store_id.store_id or ""
                },
                "tagIds": [picking.id]
            }
        return request_data

    @api.model
    def shipstation_send_shipping(self, pickings):
        for picking in pickings:
            body = self.create_or_update_order(picking)
            try:
                response_data = self.api_calling_function("/orders/createorder", body)
                if response_data.status_code == 200:
                    responses = response_data.json()
                    _logger.info("Response Data: %s" % (responses))
                    order_id = responses.get('orderId')
                    order_key = responses.get('orderKey')
                    if order_id:
                        picking.shipstation_order_id = order_id
                        picking.shipstation_order_key = order_key
                    return [{'exact_price': 0.0, 'tracking_number': ''}]
                else:
                    error_code = "%s" % (response_data.status_code)
                    error_message = response_data.reason
                    error_detail = {'error': error_code + " - " + error_message + " - "}
                    if response_data.json():
                        error_detail = {'error': error_code + " - " + error_message + " - %s" % (response_data.json())}
                    raise ValidationError(error_detail)
            except Exception as e:
                raise ValidationError(e)

    @api.multi
    def shipstation_cancel_shipment(self, picking):
        shipment_id = picking.shipstation_shipment_id
        if not shipment_id:
            raise ValidationError("Shipstation Shipment Id Not Available!")
        req_data = {"shipmentId": shipment_id}
        try:
            response_data = self.api_calling_function("/shipments/voidlabel", req_data)
            if response_data.status_code == 200:
                responses = response_data.json()
                _logger.info("Response Data: %s" % (responses))
                approved = responses.get('approved')
                if approved:
                    picking.message_post(body=_('Shipment Cancelled In Shipstation %s' % (shipment_id)))
            else:
                error_code = "%s" % (response_data.status_code)
                error_message = response_data.reason
                error_detail = {'error': error_code + " - " + error_message + " - "}
                if response_data.json():
                    error_detail = {'error': error_code + " - " + error_message + " - %s" % (response_data.json())}
                raise ValidationError(error_detail)
        except Exception as e:
            raise Warning(e)
        return True

    def shipstation_get_tracking_link(self, pickings):
        res = ""
        for picking in pickings:
            link = "%s"%(picking.carrier_id and picking.carrier_id.shipstation_carrier_id and picking.carrier_id and picking.carrier_id.shipstation_carrier_id.provider_tracking_link)
            if not link:
                raise ValidationError("Provider Link Is not available")
            res = '%s %s' % (link, picking.carrier_tracking_ref)
        return res

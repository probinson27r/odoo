from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError,Warning
import simplejson as json
from requests import request
import base64
import logging
_logger = logging.getLogger(__name__)

class ShipstationOdooIntegationConfig(models.Model):
    _name = "shipstation.odoo.configuration.vts"
    
    api_key = fields.Char(string='API Key',help='Use Your Shipstation API Key.')
    api_secret = fields.Char(string='API Secret',help='Use Your Shipstation Password as API Secret.')
    api_url = fields.Char(string='URL')
    name = fields.Char(string='Name')
    message= fields.Char(string='Message')

    @api.multi
    def api_calling_function(self, url):
        data = "%s:%s" %(self.api_key,self.api_secret)
        encode_data = base64.b64encode(data.encode("utf-8"))
        authrization_data = "Basic %s" % (encode_data.decode("utf-8"))
        headers = {"Authorization": "%s" % authrization_data}
        try:
            response_data = request(method='GET', url=url, headers=headers)
            return response_data
        except Exception as e:
            raise ValidationError(e)

    @api.multi
    def making_shipstation_url(self,api_name):
        if self.api_url:
            url=self.api_url + api_name
            return url
        else:
            raise ValidationError(_("URL is not appropriate."))

    def import_store_from_shipstation(self):
        self.store_create_process()
        self._cr.commit()
        self.carrier_create_process()
        self._cr.commit()
        self.delivery_carrier_service_process()
        self._cr.commit()
        self.delivery_carrier_package_process()
        self.message="Shipstation Import Process Completed Sucessfully.."
        self._cr.commit()


    def delivery_carrier_package_process(self):
        carrier_name = self.env['shipstation.delivery.carrier'].search([])
        for carrier in carrier_name:
            url = self.making_shipstation_url("/carriers/listpackages?carrierCode=%s"%(carrier.code))
            response = self.api_calling_function(url)
            if response.status_code != 200:
                error = "Error Code : %s - %s" % (response.status_code, response.reason)
            shipstation_operation_detail = self.env['shipstation.operation.detail']
            shipstation_operation_details= self.env['shipstation.operation.details']
            shipstation_delivery_carrier_package = self.env['shipstation.delivery.package']
            operation = False
            if not operation:
                operation_id = shipstation_operation_detail.create({
                    'shipstation_operation': 'carrier_package', 'shipstation_operation_type': 'import', 'message': 'Delivery Carrier Package Imported',
                     })
            try :
                responses=response.json()
                for response in responses:
                    shipstation_delivery_carrier_package=shipstation_delivery_carrier_package.search([('package_code','=','package'),('delivery_carrier_id','=',carrier.id)])
                    if not shipstation_delivery_carrier_package:
                        carrier_id = self.env['shipstation.delivery.carrier'].search([('code','=',response.get('carrierCode',False))])
                        shipstation_delivery_carrier_package.create({'name':response.get('name',False),
                                              'package_code':response.get('code',False),
                                              'service_nature':'domestic' if response.get('domestic',False) else 'international',
                                              'delivery_carrier_id':carrier_id.id
                                              })
                        shipstation_operation_details.create(
                        {'operation_id': operation_id.id, 'shipstation_response_message': "%s Delivery Carrier Service Created"%(response.get('name')), 'fault_operaion': False,
                         'shipstation_operation': 'carrier_package'})
                    else:
                        shipstation_operation_details.create(
                            {'operation_id': operation_id.id,
                             'shipstation_response_message': "%s Delivery Carrier Service already exist" % (response.get('name')),
                             'fault_operaion': True,
                             'shipstation_operation': 'carrier_package'})
            except Exception as e:
                shipstation_operation_details.create({'operation_id': operation_id.id, 'message': e, 'fault_operaion': True,
                                        'shipstation_operation': 'carrier_service'})



    def delivery_carrier_service_process(self):
        carrier_name = self.env['shipstation.delivery.carrier'].search([])
        for carrier in carrier_name: 
            url = self.making_shipstation_url("/carriers/listservices?carrierCode=%s"%(carrier.code))
            response = self.api_calling_function(url)
            if response.status_code != 200:
                error = "Error Code : %s - %s" % (response.status_code, response.reason)
            shipstation_operation_detail = self.env['shipstation.operation.detail']
            shipstation_operation_details= self.env['shipstation.operation.details']
            shipstation_delivery_carrier_service =self.env['shipstation.delivery.carrier.service']
            operation = False
            if not operation:
                operation_id = shipstation_operation_detail.create({
                    'shipstation_operation': 'carrier_service', 'shipstation_operation_type': 'import', 'message': 'Delivery Carrier Service Imported',
                     })
            try :
                responses=response.json()
                for response in responses:
                    shipstation_delivery_carrier_service=shipstation_delivery_carrier_service.search([('name','=',response.get('name',False))])
                    if not shipstation_delivery_carrier_service:
                        carrier_id = self.env['shipstation.delivery.carrier'].search([('code','=',response.get('carrierCode',False))])
                        shipstation_delivery_carrier_service.create({'name':response.get('name',False),
                                              'service_code':response.get('code',False),
                                              'service_nature':'domestic' if response.get('domestic',False) else 'international',
                                              'delivery_carrier_id':carrier_id.id
                                              })
                        shipstation_operation_details.create(
                        {'operation_id': operation_id.id, 'shipstation_response_message': "%s Delivery Carrier Service Created"%(response.get('name')), 'fault_operaion': False,
                         'shipstation_operation': 'carrier_service'})
                    else:
                        shipstation_operation_details.create(
                            {'operation_id': operation_id.id,
                             'shipstation_response_message': "%s Delivery Carrier Service already exist" % (response.get('name')),
                             'fault_operaion': True,
                             'shipstation_operation': 'carrier_service'})
            except Exception as e:
                shipstation_operation_details.create({'operation_id': operation_id.id, 'message': e, 'fault_operaion': True,
                                        'shipstation_operation': 'carrier_service'})



    def carrier_create_process(self):
        url = self.making_shipstation_url("/carriers")
        response = self.api_calling_function(url)
        if response.status_code != 200:
            error = "Error Code : %s - %s" % (response.status_code, response.reason)
        shipstation_operation_detail = self.env['shipstation.operation.detail']
        shipstation_operation_details= self.env['shipstation.operation.details']
        shipstation_delivery_carrier =self.env['shipstation.delivery.carrier']
        operation = False
        if not operation:
            operation_id = shipstation_operation_detail.create(
                {'shipstation_operation': 'delivery_carrier', 'shipstation_operation_type': 'import', 'message': 'Delivery Carrier Imported',
                 })
        try :
            responses=response.json()
            for response in responses:
                delivery_carrier=shipstation_delivery_carrier.search([('code','=',response.get('code',False))])
                if not delivery_carrier:
                    shipstation_delivery_carrier.create({'name':response.get('name',False),
                                          'code':response.get('code',False),
                                          'account_number':response.get('accountNumber',False),
                                          'marketplace_name':response.get('shippingProviderId',False)
                                          })
                    shipstation_operation_details.create(
                    {'operation_id': operation_id.id, 'shipstation_response_message': "%s Delivery Carrier Created"%(response.get('name')), 'fault_operaion': False,
                     'shipstation_operation': 'delivery_carrier'})
                else:
                    shipstation_operation_details.create(
                        {'operation_id': operation_id.id,
                         'shipstation_response_message': "%s Delivery Carrier already exist" % (response.get('name')),
                         'fault_operaion': True,
                         'shipstation_operation': 'delivery_carrier'})
        except Exception as e:
            shipstation_operation_details.create({'operation_id': operation_id.id, 'message': e, 'fault_operaion': True,
                                    'shipstation_operation': 'delivery_carrier'})


    def store_create_process(self):
        url=self.making_shipstation_url("/stores?stores?showInactive=false")
        response=self.api_calling_function(url)
        if response.status_code != 200:
            raise ValidationError("Error Code : %s - %s" % (response.status_code, response.reason))
        shipstation_operation_detail = self.env['shipstation.operation.detail']
        shipstation_operation_details= self.env['shipstation.operation.details']
        shipstation_store=self.env['shipstation.store.vts']
        operation = False
        if not operation:
            operation_id = shipstation_operation_detail.create(
                {'shipstation_operation': 'store', 'shipstation_operation_type': 'import', 'message': 'Store Imported',
                 })
        try :
            responses=response.json()
            for response in responses:
                store=shipstation_store.search([('store_id','=',response.get('storeId',False))])
                if not store:
                    shipstation_store.create({'store_id':response.get('storeId',False),
                                          'store_name':response.get('storeName',False),
                                          'marketplace_id':response.get('marketplaceId',False),
                                          'marketplace_name':response.get('marketplaceName',False),
                                          'acc_number':response.get('accountName',False)})
                    shipstation_operation_details.create(
                    {'operation_id': operation_id.id, 'shipstation_response_message': "%s Store Created"%(response.get('storeName')), 'fault_operaion': False,
                     'shipstation_operation': 'store'})
                else:
                    shipstation_operation_details.create(
                        {'operation_id': operation_id.id,
                         'shipstation_response_message': "%s Store already exist" % (response.get('storeName')),
                         'fault_operaion': True,
                         'shipstation_operation': 'store'})
        except Exception as e:
            shipstation_operation_details.create({'operation_id': operation_id.id, 'message': e, 'fault_operaion': True,
                                    'shipstation_operation': 'store'})









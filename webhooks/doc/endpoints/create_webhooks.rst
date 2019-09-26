.. _create-records:

Create a new Webhook
====================

Webhooks of a model are created by mapping of fields to values.

.. http:post:: /restapi/1.0/webhooks?vals={values_for_the_object's_fields}

   **Request**:

   .. sourcecode:: http

      POST /restapi/1.0/webhooks?vals={'name':'Delivery Order Updation','model':'stock.picking','kind':'on_write','address':'https://requestb.in/152eq5l1','format':'json','language':'en_US','condition':[('state', '=', 'done'), ('picking_type_id.code', '=', 'outgoing')]} HTTP/1.1
      Host: <your Odoo server url>

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': {
            'id': 20, 
            'name': 'Delivery Order Updation',
            'model': 'stock.picking', 
            'kind': 'on_write',
            'address': 'https://requestb.in/152eq5l1',
            'format': 'json',
            'language': 'en_US',  
            'fields': [],
            'condition': [('state', '=', 'done'), ('picking_type_id.code', '=', 'outgoing')],
            'create_date': '2017-11-28 15:10:36',
            'write_date': '2017-11-28 15:10:36'
        }
      }

   :query vals: values for the object's fields, as a dictionary:: ``{'field_name': field_value, ...}`` see `write() <https://www.odoo.com/documentation/10.0/reference/orm.html#odoo.models.Model.write>`_ for details.
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
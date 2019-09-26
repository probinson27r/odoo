Update an existing Webhook
==========================

.. note:: **API endpoints:**

    * :ref:`PUT {your_Odoo_server_url}/restapi/1.0/webhooks/{id}?vals={fields_and_values_to_update} <update-single-webhook>` (Update a single webhook by its id)
    * :ref:`PUT {your_Odoo_server_url}/restapi/1.0/webhooks?ids={comma_separated_ids}&vals={fields_and_values_to_update} <update-webhook-set>` (Update a list of webhooks of particular ids)

.. _update-single-webhook:

Update a single webhook by its id
---------------------------------

Give a single webhook id and a mapping of updated fields to values.

.. http:put:: /restapi/1.0/webhooks/{id}?vals={fields_and_values_to_update}

   **Request**:

   .. sourcecode:: http

      PUT /restapi/1.0/webhooks/7?vals={'address':'https://requestb.in/152eq5l1'} HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': {
            'id': 7, 
            'name': 'Product Update',
            'model': 'product.product', 
            'kind': 'on_write',
            'address': 'https://requestb.in/152eq5l1',
            'format': 'json',
            'language': 'en_US',  
            'fields': [],
            'create_date': '2017-11-02 12:15:47',
            'write_date': '2017-11-29 11:10:14'
        }
      }

   :query vals: fields to update and the value to set on them:: ``{'field_name': field_value, ...}`` see `write() <https://www.odoo.com/documentation/10.0/reference/orm.html#odoo.models.Model.write>`_ for details.
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise

.. _update-webhook-set:

Update a list of webhooks of particular ids
-------------------------------------------

Give a list of webhook ids and a mapping of updated fields to values.

.. warning:: Multiple webhooks can be updated simultanously, but they will all get the same values for the fields being set. It is not currently possible to perform **computed** updates (where the value being set depends on an existing value of a webhook).

.. http:put:: /restapi/1.0/webhooks?ids={comma_separated_ids}&vals={fields_and_values_to_update}

   **Request**:

   .. sourcecode:: http

      PUT /restapi/1.0/webhooks?ids=7,12&vals={'address':'https://requestb.in/152eq5l1'} HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': [
            {
                'id': 7, 
                'name': 'Product Update',
                'model': 'product.product', 
                'kind': 'on_write',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US',  
                'fields': [],
                'create_date': '2017-11-02 12:15:47',
                'write_date': '2017-11-29 11:10:14'
            },
            {
                'id': 12, 
                'name': 'Product Deletion',
                'model': 'product.product', 
                'kind': 'on_unlink',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US',  
                'fields': [],
                'create_date': '2017-11-02 12:15:47',
                'write_date': '2017-11-29 11:10:14'
            }
        ]
      }

   :query vals: fields to update and the value to set on them:: ``{'field_name': field_value, ...}`` see `write() <https://www.odoo.com/documentation/10.0/reference/orm.html#odoo.models.Model.write>`_ for details.
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
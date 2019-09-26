Get a count of Webhooks
=======================

Get the number of all webhooks by default and by passing `domain <https://www.odoo.com/documentation/10.0/reference/orm.html#reference-orm-domains>`_ filter optionally, retrieve only the number of webhooks matching the query.

.. http:get:: /restapi/1.0/webhooks/count

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks/count?domain=[('model','=','product.product')] HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'count': 3
      }

   :query domain: `A search domain <https://www.odoo.com/documentation/10.0/reference/orm.html#reference-orm-domains>`_. Use an empty
                     list to match all webhooks.
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
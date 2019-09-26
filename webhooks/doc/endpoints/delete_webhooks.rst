Delete a Webhook from the database
==================================

.. note:: **API endpoints:**

    * :ref:`DELETE {your_Odoo_server_url}/restapi/1.0/webhooks/{id} <delete-single-webhook>` (Delete a single webhook by its id)
    * :ref:`DELETE {your_Odoo_server_url}/restapi/1.0/webhooks?ids={comma_separated_ids} <delete-webhook-set>` (Delete a list of webhooks of particular ids)

.. _delete-single-webhook:

Delete a single webhook by its id
---------------------------------

Give a single webhook id to delete.

.. http:delete:: /restapi/1.0/webhooks/{id}

   **Request**:

   .. sourcecode:: http

      DELETE /restapi/1.0/webhooks/7 HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {}
      
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise

.. _delete-webhook-set:

Delete a list of webhooks of particular ids
-------------------------------------------

Give a list of webhook ids to delete.

.. http:delete:: /restapi/1.0/webhooks?ids={comma_separated_ids}

   **Request**:

   .. sourcecode:: http

      DELETE /restapi/1.0/webhooks?ids=7,12 HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {}

   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
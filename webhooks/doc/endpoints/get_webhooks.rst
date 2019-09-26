Get a Webhooks
==============

.. note:: **API endpoints:**

    * :ref:`GET {your_Odoo_server_url}/restapi/1.0/webhooks <read-all-webhook>` (Get a list of all webhooks)
    * :ref:`GET {your_Odoo_server_url}/restapi/1.0/webhooks/{id} <read-single-webhook>` (Get a single webhook by its id)
    * :ref:`GET {your_Odoo_server_url}/restapi/1.0/webhooks?ids={comma_separated_ids} <read-webhook-set>` (Get a list of webhooks of particular ids)
    * :ref:`GET {your_Odoo_server_url}/restapi/1.0/webhooks/?domain={comma_separated_list_of_args} <read-specific-webhook>` (Get a list of specific webhooks using domain filter)

.. _read-all-webhook:

Get a list of all webhooks
--------------------------

By default, it will fetch all the webhooks and relavent fields the current user can read. Give an optionally a list of specific fields to fetch.

.. http:get:: /restapi/1.0/webhooks

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': [
            {
                'id': 3, 
                'name': 'Product Creation',
                'model': 'product.product', 
                'kind': 'on_create',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US',  
                'fields': [],
                'create_date': '2017-11-02 12:15:47',
                'write_date': '2017-11-02 14:12:40'
            },
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
                'write_date': '2017-11-02 14:12:40'
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
                'write_date': '2017-11-02 14:12:40'
            },
            ...
            ...
            ...
        ]
      }

   :query fields: OPTIONAL. list of field names to return (default is all fields).
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
   
Conversely, picking only six fields deemed interesting.

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks?fields=['name','model', 'kind', 'address', 'format', 'language'] HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': [
            {
                'id': 3, 
                'name': 'Product Creation',
                'model': 'product.product', 
                'kind': 'on_create',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US',  
            },
        ...
        ...
        ...
        ]
      }
      
   .. note:: even if the ``id`` field is not requested, it is always returned

.. _read-single-webhook:

Get a single webhook by its id
------------------------------

Give a single webhook id and optionally a list of fields to fetch. By default, it will fetch all the fields the current user can read.

.. http:get:: /restapi/1.0/webhooks/{id}

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks/7 HTTP/1.1
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
            'write_date': '2017-11-02 14:12:40'
        }
      }

   :query fields: OPTIONAL. list of field names to return (default is all fields).
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
   
Conversely, picking only six fields deemed interesting.

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks/7?fields=['name','model', 'kind', 'address', 'format', 'language'] HTTP/1.1
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
            'language': 'en_US'
        }
      }
      
   .. note:: even if the ``id`` field is not requested, it is always returned
   
.. _read-webhook-set:

Get a list of webhooks of particular ids
----------------------------------------

Give a list of webhook ids and optionally `domain <https://www.odoo.com/documentation/10.0/reference/orm.html#reference-orm-domains>`_ filter and a list of fields to fetch. By default, it will fetch all the fields the current user can read.

.. http:get:: /restapi/1.0/webhooks?ids={comma_separated_ids}

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks?ids=3,12 HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': [
            {
                'id': 3, 
                'name': 'Product Creation',
                'model': 'product.product', 
                'kind': 'on_create',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US',  
                'fields': [],
                'create_date': '2017-11-02 12:15:47',
                'write_date': '2017-11-02 14:12:40'
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
                'write_date': '2017-11-02 14:12:40'
            }
        ]
      }
      
   :query fields: OPTIONAL. list of field names to return (default is all fields).
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise
   
Conversely, picking only six fields deemed interesting.

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks?ids=3,12&fields=['name', 'model', 'kind', 'address', 'format', 'language'] HTTP/1.1
      Host: {your_Odoo_server_url}

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

      {
        'webhook': [
            {
                'id': 3, 
                'name': 'Product Creation',
                'model': 'product.product', 
                'kind': 'on_create',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US'
            },
            {
                'id': 12, 
                'name': 'Product Deletion',
                'model': 'product.product', 
                'kind': 'on_unlink',
                'address': 'https://requestb.in/152eq5l1',
                'format': 'json',
                'language': 'en_US'
            }
        ]
      }
      
   .. note:: even if the ``id`` field is not requested, it is always returned
   
.. _read-specific-webhook:

Get a list of specific webhooks using domain filter
---------------------------------------------------

Give a `Domain <https://www.odoo.com/documentation/10.0/reference/orm.html#reference-orm-domains>`_ filter and optionally a list of fields to fetch. By default, it will fetch all the webhooks and relavent fields the current user can read.

.. http:get:: /restapi/1.0/webhooks/?domain={comma_separated_list_of_args}

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks?domain=[('model','=','product.product'),('kind','=','on_write')] HTTP/1.1
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
                'write_date': '2017-11-02 14:12:40'
            }
        ]
      }

   :query domain: OPTIONAL. `A search domain <https://www.odoo.com/documentation/10.0/reference/orm.html#reference-orm-domains>`_. Use an empty
                     list to match all webhooks.
   :query fields: OPTIONAL. list of field names to return (default is all fields).
   :query offset: OPTIONAL. Number of results to ignore (default: none)
   :query limit: OPTIONAL. Maximum number of webhooks to return (default: all)
   :query order: OPTIONAL. Sort string
   :query count: OPTIONAL. if True, only counts and returns the number of matching webhooks (default: False)
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: The OAuth protocol parameters to authenticate.
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there’s no resource
   :statuscode 401: authentication failed
   :statuscode 403: if any error raise

Conversely, picking only six fields deemed interesting.

   **Request**:

   .. sourcecode:: http

      GET /restapi/1.0/webhooks?domain=[('model','=','product.product'),('kind','=','on_write')]&fields=['name', 'model', 'kind', 'address', 'format', 'language']&limit=5 HTTP/1.1
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
                'language': 'en_US'
            }
        ]
      }
      
   .. note:: even if the ``id`` field is not requested, it is always returned
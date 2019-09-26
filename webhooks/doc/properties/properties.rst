.. _properties:

Properties
==========

============================    ============
Field                           Description
============================    ============
name                            **'name': 'Product Creation'**

                                User friendly name of the webhook.
create_date                     **'create_date': '2016-10-05 10:31:39'**

                                The date and time when the webhook was created.
write_date                      **'write_date': '2016-10-05 12:09:20'**

                                The date and time when the webhook was last updated.                              
                                
model                           **'model': 'product.product'**

                                Name of Odoo object.
                                
                                .. warning:: Model name cannot be modified in update of webhook.
kind                            **'kind': 'on_create'**

                                The event that will trigger the webhook. 
                                
                                .. note:: Valid values are: ``on_create``, ``on_write`` and ``on_unlink``
language                        **'language': 'en_US'**

                                The language in which the webhook should send the data.
address                         **'address': 'https://example.com/payload'**

                                The URI where the webhook should send the POST request when the event occurs.
format                          **'format': 'json'**

                                The format in which the webhook should send the data. 
                                
                                .. note:: Valid values are ``json`` and ``xml``.
fields                          **'fields': ['name', 'default_code', 'list_price', 'qty_available']**

                                (Optional) An array of fields which should be included in webhooks.
condition                       **'condition': [('type', '=', 'product')]**

                                (Optional) This must be specified before webhook send the POST request when the 
                                event occurs.                        
============================    ============ 
.. Odoo Webhooks: Version 1.0 documentation master file, created by
   sphinx-quickstart on Fri Jul 28 15:46:54 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.  

Odoo Webhooks: Version 1.0 documentation
========================================

Webhooks(**A user-defined HTTP callbacks**) are a useful tool for apps that want to execute code after a specific event happens on an Odoo, for example, after a warehouse manager creates a new product, updates a stock quantity for existing products or sales manager confirm the quotation.

Instead of telling your app to make an API call every X number of minutes to check if a specific event has occured on an Odoo, you can register webhooks, which send an HTTP request from the Odoo telling your app that the event has occurred. This uses many less API requests overall, allowing you to build more robust apps, and update your app instantly after a webhook is received.

Webhook event data can be stored as JSON or XML, and is commonly used when:

    * Placing an order
    * Changing a product's price
    * Collecting data for data-warehousing
    * Integrating your accounting software
    * Filtering the order items and informing various shippers about the order
    
Another, less-obvious, case for using webhooks is when you're dealing with data that isn't easily searchable through the Odoo API. For example, re-requesting an entire product catalog or order history would benefit from using webhooks since it requires a lot of API requests and takes a lot of time.

Think of it this way, if you would otherwise have to poll for a substantial amount of data, you should be using webhooks.

Get the module
==============

The module **webhook** is available on **Odoo App Store**, Here are links for:
    
    * `Version 9.0 (Community & Enterprise) <https://www.odoo.com/apps/modules/9.0/webhooks/>`_
    * `Version 10.0 (Community & Enterprise) <https://www.odoo.com/apps/modules/10.0/webhooks/>`_
    * `Version 11.0 (Community & Enterprise) <https://www.odoo.com/apps/modules/11.0/webhooks/>`_
    
Dependencies
============

The module **webhook** is depend on **restapi** module, which is also available on **Odoo App Store**, Here are links for:
    
    * `Version 9.0 (Community & Enterprise) <https://www.odoo.com/apps/modules/9.0/restapi/>`_
    * `Version 10.0 (Community & Enterprise) <https://www.odoo.com/apps/modules/10.0/restapi/>`_
    * `Version 11.0 (Community & Enterprise) <https://www.odoo.com/apps/modules/11.0/restapi/>`_
    
.. note:: Odoo REST API documentation is available `here <http://odoo-restapi.readthedocs.io>`_, which will give you complete guide for how to install and work with **restapi** module.

Installation
============

There are two ways to install module:

Directly from App store
-----------------------

1. Activate **Developer Mode**
2. Navigate to the **Apps** menu
3. Click on second **Apps** menu if you are using version 9.0 otherwise **App Store** menu in left side bar
4. Remove **Featured [x]** filter from search bar
5. search module **webhook**
6. Click on **Install** button.

By puting module in addons
--------------------------

1. Unzip **webhook** module to **custom addons** directory
2. Restart odoo server
3. Activate **Developer Mode**
4. Navigate to the **Apps** menu
5. Click on **Update Apps List** menu in left side bar
6. Once apps list is updated, click on **Apps** menu in left side bar
7. Search module **webhook**
8. Click on **Install** button.

Getting Started
===============

.. toctree::
   :maxdepth: 2

   configuration
   properties/properties
   endpoints/endpoints
   receive_webhook
   respond_to_webhook

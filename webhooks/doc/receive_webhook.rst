Receive a webhook
=================

Once you register a webhook URL with Odoo, it will issue a HTTP POST request to the URL specified every time that event occurs. The request's POST parameters will contain XML/JSON data relevant to the event that triggered the request.
    
The trouble with testing your webhooks is that you need a publicly visible URL to handle them.

.. _webhook-tool:

There are a couple of tools that make working with webhooks during development much easier such as `RequestBin <https://requestb.in>`_, `Pagekite <https://pagekite.net>`_ and `ngrok <https://ngrok.com>`_.

.. figure::  images/requestbin-logo.png
   :align:   center

`RequestBin <https://requestb.in>`_ allows you to create a URL that will collect any requests made to it. You can then inspect your requests and see the values returned. The URL provided is **temporary** and can only be used for 20 requests or for 48 hours (whichever comes first).

.. figure::  images/pagekite-logo.png
   :align:   center

`Pagekite <https://pagekite.net>`_ makes local websites or SSH servers publicly accessible in mere seconds and works over any internet connection.

.. figure::  images/ngrok-logo.png
   :align:   center

`ngrok <https://ngrok.com>`_ creates a tunnel from the public internet (http://subdomain.ngrok.com) to a port on your local machine. You can give this URL to anyone to allow them to try out a web site you're developing without doing any deployment.

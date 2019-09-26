Respond to a webhook
====================

Your webhook acknowledges that it received data by sending a **200 OK** response. Any response outside of the 200 range will let Odoo know that you did not receive your webhook. Odoo has implemented a configurable ``timeout period`` and a ``retry period`` for subscriptions under **Settings** **‣** **General Settings** **‣** **Webhook Configuration**. 

We wait for a response to each request till configured timeout period (default is 5 seconds), and if there isn't one or we get an error, we retry the connection for configured retry periods (default is 5 times). A webhook request job will be deleted if there are N number of consecutive failures for the exact same webhook (N being a configured retry period, default is 5 times). You should monitor the admin of your :ref:`webhook tool <webhook-tool>` for failing webhooks.

If you're receiving an Odoo webhook, the most important thing to do is respond quickly. There have been several historical occurrences of apps that do some lengthy processing when they receive a webhook that triggers the timeout. This has led to situations where webhooks were removed from functioning apps.

To make sure that apps don't accidentally run over the timeout limit, we now recommend that apps defer processing until after the response has been sent.
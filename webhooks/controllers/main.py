# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.http import Response
from ..utils import dicttoxml
import json
import werkzeug
# from urlparse import urljoin
from urllib.parse import urljoin
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessError
from odoo.addons.restapi.controllers.main import RestApi

class Webhook(RestApi):

    @http.route(['/restapi/1.0/webhooks','/restapi/1.0/webhooks/<int:id>', \
          '/restapi/1.0/webhooks/<int:id>/<string:method>'], \
        type="http", auth="public", csrf=False, website=True)
    def webhook(self, id=None, method=None, **kwargs):
        """
        CURD webhook
        """
        auth, auth_user, invalid = self.valid_authentication(kwargs)
        if not auth_user or invalid:
            return self.get_response(401, str(401), {'code': 401, 'message': 'Authentication required'})
        kwargs.update(self.evaluate(request.httprequest.data) or {})
        kwargs, invalid = self.validate_arguments(id=id, kwargs=kwargs)
        if invalid:
            return invalid
        kwargs['context'] = {'auth_id': auth.id, 'from_webhook': True}
        if kwargs.get('fields'):
            kwargs['context'].update({'fields': True})
        return self.perform_request('webhook.webhook', method=method, id=id, kwargs=kwargs, user=auth_user)
    
    @http.route(['/restapi/1.0/webhooks/<string:method>'], \
        type="http", auth="public", csrf=False, website=True)
    def webhook_method(self, method=None, **kwargs):
        """
        CURD webhook
        """
        auth, auth_user, invalid = self.valid_authentication(kwargs)
        if not auth_user or invalid:
            return self.get_response(401, str(401), {'code': 401, 'message': 'Authentication required'})
        kwargs.update(self.evaluate(request.httprequest.data) or {})
        kwargs, invalid = self.validate_arguments(id=None, kwargs=kwargs)
        if invalid:
            return invalid
        kwargs['context'] = {'auth_id': auth.id, 'from_webhook': True}
        if kwargs.get('fields'):
            kwargs['context'].update({'fields': True})
        return self.perform_request('webhook.webhook', method=method , kwargs=kwargs, user=auth_user)

    @http.route(['/restapi/1.0/webhooks/count'], \
        type="http", auth="public", csrf=False, website=True)
    def webhook_count(self, **kwargs):
        """
        Count Webhook.
        """
        auth, auth_user, invalid = self.valid_authentication(kwargs)
        if not auth_user or invalid:
            return self.get_response(401, str(401), {'code': 401, 'message': 'Authentication required'})

        return self.perform_request('webhook.webhook', method='search_count', kwargs=kwargs, user=auth_user)

    def validate_arguments(self, id=None, kwargs={}):
        args = kwargs.get('vals') or {}
        if kwargs.get('ids'):
            ids = list(map(self.evaluate, kwargs['ids'].split(',')))
            model_ids = []
            webhooks = request.env['webhook.webhook'].sudo().search([('id', 'in', ids)])
            if webhooks:
                for webhook in webhooks:
                    if webhook.model_id.id not in model_ids:
                        model_ids.append(webhook.model_id.id)
                    if len(model_ids) > 1:
                        return kwargs, self.get_response(403, '403', {'code': 403, 'message': 'model of record ids must be same'})
        if kwargs.get('vals') and not id and not kwargs.get('ids'):
            args = self.evaluate(kwargs['vals'])
            if args.get('model') and not args.get('model_id'):
                model = args['model']
                model_id = request.env['ir.model'].sudo().search([('model', '=', model)]).id
                if not model_id:
                    return kwargs, self.get_response(401, '401', {'code': 401, 'message': 'model not found'})
                args.update({'model_id': model_id})
            elif args.get('model'):
                model = request.env['ir.model'].search([('id', '=', args.get('model_id'))]).model
                if args.get('model') and args['model'] != model:
                    return kwargs, self.get_response(401, '401', {'code': 401, 'message': 'model and model_id mismatch'})
                elif not model:
                    return kwargs, self.get_response(401, '401', {'code': 401, 'message': 'model does not exists'})
            elif not args.get('model_id'):
                return kwargs, self.get_response(401, '401', {'code': 401, 'message': 'model_id is required'})
            if args.get('language'):
                lang_id = request.env['res.lang'].search([('code', 'ilike', args['language'])])
                args.update({'lang_id': lang_id.id})
                args.pop('language')
            else:
                args.update({'lang_id': 1})
            args.pop('model', False)
        kwargs['vals'] = args
        return kwargs, False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
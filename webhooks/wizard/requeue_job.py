# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models

class RequeueJob(models.TransientModel):
    """Multiple jobs requeue Wizard"""
    _name = 'webhook.requeue.job'
    _description = 'Wizard to requeue a selection of jobs'

    @api.model
    def _default_job_ids(self):
        res = False
        context = self.env.context
        if (context.get('active_model') == 'webhook.job' and
                context.get('active_ids')):
            res = context['active_ids']
        return res

    job_ids = fields.Many2many(comodel_name='webhook.job',
                               string='Jobs',
                               default=_default_job_ids)

    @api.multi
    def requeue(self):
        jobs = self.job_ids
        jobs.requeue()
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:s
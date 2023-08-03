# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeakestSession(models.Model):
    _name = 'weakest.link.session'
    _description = 'Weakest link game'
    _rec_name = 'name'

    name = fields.Char(string="Value")
    players = fields.Integer(string="Players", required=True, default=8)
    players_ids = fields.Many2many('res.users', string="Users", required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    global_value = fields.Monetary(currency_field="currency_id", string="Total", compute="get_total_value")
    round_ids = fields.One2many('survey.survey', 'session_id', string="Sessions")

    @api.model
    def create(self, vals):
        res = super(WeakestSession, self).create(vals)
        for line in list(range(res.players)):
            self.env['weakest.link'].create({'name': res.name + ' Round ' + str(line + 1), 'session_id': res.id,
                                             'players_ids': res.players_ids.ids, 'objective': False})
        return res

    def get_total_value(self):
        for record in self:
            record.global_value = sum(record.round_ids.mapped('global_value'))


class Weakestlink(models.Model):
    _inherit = 'survey.survey'
    _description = 'Weakest link session'

    session_id = fields.Many2one('weakest.link.session', string="Session")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    global_value = fields.Monetary(currency_field="currency_id", string="Total")
    line_ids = fields.One2many('weakest.link.line', 'link_id', string="Lines")
    current_line_id = fields.Many2one('weakest.link.line', string="Current line")
    objective = fields.Boolean(string="Objective")
    players_ids = fields.Many2many('res.users', string="Users")
    deleted_player_id = fields.Many2one('res.users', string="Deleted user")

    @api.model
    def create(self, vals):
        res = super(Weakestlink, self).create(vals)
        a = self.env['weakest.link.values'].search([])
        for line in a:
            self.env['weakest.link.line'].create({'sequence': line.sequence, 'value': line.value, 'link_id': res.id})
        return res

    def correct(self):
        for record in self:
            if len(record.line_ids.filtered(lambda c: c.sums is not True)):
                record.line_ids.filtered(lambda c: c.sums is not True)[0].write({'sums': True})

    def incorrect(self):
        for record in self:
            record.line_ids.write({'sums': False})

    def bank(self):
        for record in self:
            if record.line_ids.filtered(lambda c: c.sums is True):
                record.current_line_id = record.line_ids.filtered(lambda c: c.sums is True)[-1].id
                if record.global_value + record.current_line_id.value > record.line_ids[-1].value:
                    record.global_value = record.line_ids[-1].value
                else:
                    record.global_value = record.global_value + record.current_line_id.value
                if record.global_value == record.line_ids[-1].value:
                    record.objective = True
                record.line_ids.write({'sums': False})


class Weakestline(models.Model):
    _name = 'weakest.link.line'
    _description = 'Weakest link line'
    _rec_name = 'value'

    sequence = fields.Integer(string="Sequence")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    value = fields.Monetary(currency_field="currency_id")
    sums = fields.Boolean(string="Sum")
    link_id = fields.Many2one('survey.survey', string="Line")


class Weakest_values(models.Model):
    _name = 'weakest.link.values'
    _rec_order = 'sequence'
    _description = 'Weakest link values'

    sequence = fields.Integer(string="Sequence")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    value = fields.Monetary(currency_field="currency_id")
    sums = fields.Boolean(string="Sum")
    link_id = fields.Many2one('survey.survey', string="Line")


class Weakest_question(models.Model):
    _inherit = 'survey.question'
    _description = 'Weakest link questions'

    topic_id = fields.Many2one('weakest.link.topic', string="Topic")
    question = fields.Text()
    player_id = fields.Many2one('res.users')


class Weakest_topic(models.Model):
    _name = 'weakest.link.topic'
    _description = 'Weakest link topic'

    name = fields.Char(required=True)
    question_ids = fields.One2many('survey.question', 'topic_id')

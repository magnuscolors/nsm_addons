# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from openerp import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp


from openerp import models, fields as fields2, api, _
from openerp.exceptions import UserError



# class hr_expense_expense(osv.osv):
#     _inherit = 'hr.expense.expense'

class hr_expense_expense(osv.osv):
    _inherit = 'hr.expense'

    def _journal_get(self, cr, uid, context=None):
        if context is None:
            context = {}
        user = self.pool.get('res.users').browse(cr, uid, [uid], context=context)[0]
        return user.company_id.decl_journal_id.id
    

    _columns = {
        # 'line_ids': fields.one2many('hr.expense.line', 'expense_id', 'Expense Lines', readonly=True, states={'draft':[('readonly',False)],'confirm':[('readonly',False)]}),
        'account_id': fields.many2one('account.account', 'Account', readonly=True, help="The partner account used for this expense."),
        'date_confirm': fields.date('Date Submitted', select=True,
                                    help="Date of submission of the sheet expense. It's filled when the button Confirm is pressed."),
        # 'state': fields.selection([
        #     ('draft', 'New'),
        #     ('cancelled', 'Refused'),
        #     ('confirm', 'Waiting Finance'),
        #     ('done', 'Waiting Approval'),
        #     ('accepted', 'Waiting Payment'),
        #     ('paid', 'Paid'),
        #     ],
        #     'Status', readonly=True, track_visibility='onchange',
        #     help='When the expense request is created the status is \'Draft\'.\n It is confirmed by the user and request is sent to Finance, the status is \'Waiting Finance\'.\
        #     \nIf Finance made accounting entries, the status is \'Waiting Approval\'.\n If the Manager has given approval, the status is \'Waiting Payment\'.'),

    }
    _defaults = {
        'journal_id': _journal_get,
    }


    # method renamed to "action_move_create"
    # def action_receipt_create(self, cr, uid, ids, context=None):
    #     '''
    #     main function that is called when trying to create the accounting entries related to an expense, inherited from hr_expense
    #     '''
    #     super(hr_expense_expense, self).action_receipt_create(cr, uid, ids, context=context)
    #     for exp in self.browse(cr, uid, ids, context=context):
    #         acc = exp.employee_id.address_home_id.property_account_payable.id
    #         self.write(cr, uid, ids, {'account_id': acc }, context=context)
    #     return True

    
    # def move_line_get(self, cr, uid, expense_id, context=None):
    #     res = []
    #     tax_obj = self.pool.get('account.tax')
    #     cur_obj = self.pool.get('res.currency')
    #     if context is None:
    #         context = {}
    #     exp = self.browse(cr, uid, expense_id, context=context)
    #     company_currency = exp.company_id.currency_id.id
    #
    #     for line in exp.line_ids:
    #         mres = self.move_line_get_item(cr, uid, line, context)
    #         if not mres:
    #             continue
    #         res.append(mres)
    #
    #         #Calculate tax according to default tax on product
    #         taxes = []
    #         #Taken from product_id_onchange in account.invoice
    #         if line.product_id:
    #             fposition_id = False
    #             fpos_obj = self.pool.get('account.fiscal.position')
    #             fpos = fposition_id and fpos_obj.browse(cr, uid, fposition_id, context=context) or False
    #             product = line.product_id
    #             taxes = product.supplier_taxes_id
    #             #If taxes are not related to the product, maybe they are in the account
    #             if not taxes:
    #                 a = product.property_account_expense.id #Why is not there a check here?
    #                 if not a:
    #                     a = product.categ_id.property_account_expense_categ.id
    #                 a = fpos_obj.map_account(cr, uid, fpos, a)
    #                 taxes = a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False
    #         if not taxes:
    #             continue
    #         tax_l = []
    #         base_tax_amount = line.total_amount
    #         #Calculating tax on the line and creating move?
    #         for tax in tax_obj.compute_all(cr, uid, taxes,
    #                 line.unit_amount ,
    #                 line.unit_quantity, line.product_id,
    #                 exp.user_id.partner_id)['taxes']:
    #             tax_code_id = tax['base_code_id']
    #             if not tax['amount'] and not tax['tax_code_id']:
    #                 continue
    #             res[-1]['tax_code_id'] = tax_code_id
    #             ##
    #             is_price_include = tax_obj.read(cr,uid,tax['id'],['price_include'],context)['price_include']
    #             if is_price_include:
    #                 ## We need to deduce the price for the tax
    #                 res[-1]['price'] = res[-1]['price'] - tax['amount']
    #                 # tax amount countains base amount without the tax
    #                 base_tax_amount = (base_tax_amount - tax['amount']) * tax['base_sign']
    #             else:
    #                 base_tax_amount = base_tax_amount * tax['base_sign']
    #
    #             assoc_tax = {
    #                          'type':'tax',
    #                          'name':tax['name'],
    #                          'price_unit': tax['price_unit'],
    #                          'quantity': 1,
    #                          'price': tax['amount'] or 0.0,
    #                          'account_id': tax['account_collected_id'] or mres['account_id'],
    #                          'tax_code_id': tax['tax_code_id'],
    #                          'tax_amount': tax['amount'] * tax['base_sign'],
    #                          }
    #             tax_l.append(assoc_tax)
    #
    #         res[-1]['tax_amount'] = cur_obj.compute(cr, uid, exp.currency_id.id, company_currency, base_tax_amount, context={'date': exp.date_confirm})
    #         res += tax_l
    #     return res

    # -- below method is deprecated in Odoo 9
    # Workflow stuff
    #################
    # return the ids of the move lines which has the same account than the invoice
    # whose id is in ids
    # def move_line_id_payment_get(self, cr, uid, ids, *args):
    #     if not ids: return []
    #     result = self.move_line_id_payment_gets(cr, uid, ids, *args)
    #     return result.get(ids[0], [])

    # -- below method is deprecated in Odoo 9
    # def move_line_id_payment_gets(self, cr, uid, ids, *args):
    #     res = {}
    #     if not ids: return res
    #     cr.execute('SELECT i.id, l.id '\
    #                'FROM account_move_line l '\
    #                'LEFT JOIN hr_expense_expense i ON (i.account_move_id=l.move_id) '\
    #                'WHERE i.id IN %s '\
    #                'AND l.account_id=i.account_id',
    #                (tuple(ids),))
    #     for r in cr.fetchall():
    #         res.setdefault(r[0], [])
    #         res[r[0]].append( r[1] )
    #     return res

    # -- below method is deprecated in Odoo 9
    # def test_paid(self, cr, uid, ids, *args):
    #     res = self.move_line_id_payment_get(cr, uid, ids)
    #     if not res:
    #         return False
    #     ok = True
    #     for id in res:
    #         cr.execute('select reconcile_id from account_move_line where id=%s', (id,))
    #         ok = ok and  bool(cr.fetchone()[0])
    #     return ok
    
    def confirm_paid(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state':'paid'}, context=context)
        return True

    # -- below method is deprecated in Odoo 9
    # def expense_accept(self, cr, uid, ids, context=None):
    #     move_obj = self.pool.get('account.move')
    #     for expense in self.browse(cr, uid, ids, context=context):
    #         if expense.account_move_id:
    #             move_obj.button_validate(cr, uid, [expense.account_move_id.id], context)
    #     return self.write(cr, uid, ids, {'state': 'accepted', 'date_valid': time.strftime('%Y-%m-%d'), 'user_valid': uid}, context=context)

    def expense_redone(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('account.move')
        for expense in self.browse(cr, uid, ids, context=context):
            if expense.account_move_id:
                move_obj.button_cancel(cr, uid, [expense.account_move_id.id], context)
        return self.write(cr, uid, ids, {'state': 'post'}, context=context)

    # -- below method is deprecated in Odoo 9
    # def expense_canceled(self, cr, uid, ids, context=None):
    #     for expense in self.browse(cr, uid, ids, context=context):
    #         if expense.account_move_id:
    #             for move_line in expense.account_move_id.line_id:
    #                 if move_line.reconcile_id or move_line.reconcile_partial_id:
    #                      raise osv.except_osv(
    #                              _('Error!'),
    #                              _('Please unreconcile payment accounting entries before cancelling this expense'))
    #             ### Then we unlink the move line
    #             self.pool.get('account.move').unlink(cr, uid, [expense.account_move_id.id], context=context)
    #     return self.write(cr, uid, ids, {'state': 'cancelled'}, context=context)

# -- object deprecated in Odoo 9
# class hr_expense_line(osv.osv):
#      _inherit = 'hr.expense.line'
#
#      def onchange_product_id(self, cr, uid, ids, product_id, context=None):
#         res = {}
#         return {'value': res}


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    state = fields2.Selection([('draft', 'To Submit'),
                              ('submit', 'Waiting Finance'),
                              ('post', 'Waiting Approval'),
                              ('approve', 'Waiting Payment'),
                              ('done', 'Paid'),
                              ('cancel', 'Refused')
                              ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft', required=True,
            help='When the expense request is created the status is \'To Submit\'.\n It is confirmed by the user and request is sent to Finance, the status is \'Waiting Finance\'.\
            \nIf Finance made accounting entries, the status is \'Waiting Approval\'.\n If the Manager has given approval, the status is \'Waiting Payment\'.')


    def action_move_create(self, cr, uid, ids, context=None):
        super(HrExpense, self).action_move_create(cr, uid, ids, context=context)
        for exp in self.browse(cr, uid, ids, context=context):
            acc = exp.employee_id.address_home_id.property_account_payable_id.id
            self.write(cr, uid, ids, {'account_id': acc }, context=context)
        return True



    # -- below method is deprecated in Odoo 9
    # def move_line_get(self, cr, uid, expense_id, context=None):
    #     res = []
    #     tax_obj = self.pool.get('account.tax')
    #     cur_obj = self.pool.get('res.currency')
    #     if context is None:
    #         context = {}
    #     exp = self.browse(cr, uid, expense_id, context=context)
    #     company_currency = exp.company_id.currency_id.id
    #
    #     for line in exp.line_ids:
    #         mres = self.move_line_get_item(cr, uid, line, context)
    #         if not mres:
    #             continue
    #         res.append(mres)
    #
    #         #Calculate tax according to default tax on product
    #         taxes = []
    #         #Taken from product_id_onchange in account.invoice
    #         if line.product_id:
    #             fposition_id = False
    #             fpos_obj = self.pool.get('account.fiscal.position')
    #             fpos = fposition_id and fpos_obj.browse(cr, uid, fposition_id, context=context) or False
    #             product = line.product_id
    #             taxes = product.supplier_taxes_id
    #             #If taxes are not related to the product, maybe they are in the account
    #             if not taxes:
    #                 a = product.property_account_expense.id #Why is not there a check here?
    #                 if not a:
    #                     a = product.categ_id.property_account_expense_categ.id
    #                 a = fpos_obj.map_account(cr, uid, fpos, a)
    #                 taxes = a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False
    #         if not taxes:
    #             continue
    #         tax_l = []
    #         base_tax_amount = line.total_amount
    #         #Calculating tax on the line and creating move?
    #         for tax in tax_obj.compute_all(cr, uid, taxes,
    #                 line.unit_amount ,
    #                 line.unit_quantity, line.product_id,
    #                 exp.user_id.partner_id)['taxes']:
    #             tax_code_id = tax['base_code_id']
    #             if not tax['amount'] and not tax_code_id:
    #                 continue
    #             res[-1]['tax_code_id'] = tax_code_id
    #             ##
    #             is_price_include = tax_obj.read(cr,uid,tax['id'],['price_include'],context)['price_include']
    #             if is_price_include:
    #                 ## We need to deduce the price for the tax
    #                 res[-1]['price'] = res[-1]['price'] - tax['amount']
    #                 # tax amount countains base amount without the tax
    #                 base_tax_amount = (base_tax_amount - tax['amount']) * tax['base_sign']
    #             else:
    #                 base_tax_amount = base_tax_amount * tax['base_sign']
    #
    #             assoc_tax = {
    #                          'type':'tax',
    #                          'name':tax['name'],
    #                          'price_unit': tax['price_unit'],
    #                          'quantity': 1,
    #                          'price': tax['amount'] or 0.0,
    #                          'account_id': tax['account_collected_id'] or mres['account_id'],
    #                          'tax_code_id': tax['tax_code_id'],
    #                          'tax_amount': tax['amount'] * tax['base_sign'],
    #                          }
    #             tax_l.append(assoc_tax)
    #
    #         res[-1]['tax_amount'] = cur_obj.compute(cr, uid, exp.currency_id.id, company_currency, base_tax_amount, context={'date': exp.date_confirm})
    #         res += tax_l
    #     return res


    # Overridden:
    @api.multi
    def action_move_create(self):
        '''
        main function that is called when trying to create the accounting entries related to an expense
        '''
        # if any(expense.state != 'approve' for expense in self):
        #     raise UserError(_("You can only generate accounting entry for approved expense(s)."))

        if any(expense.employee_id != self[0].employee_id for expense in self):
            raise UserError(_("Expenses must belong to the same Employee."))

        if any(not expense.journal_id for expense in self):
            raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))

        journal_dict = {}
        maxdate = False
        for expense in self:
            if expense.date > maxdate:
                maxdate = expense.date
            jrn = expense.bank_journal_id if expense.payment_mode == 'company_account' else expense.journal_id
            journal_dict.setdefault(jrn, [])
            journal_dict[jrn].append(expense)

            acc = expense.employee_id.address_home_id.property_account_payable_id.id
            expense.write({'account_id': acc })

        for journal, expense_list in journal_dict.items():
            #create the move that will contain the accounting entries
            move = self.env['account.move'].create({
                'journal_id': journal.id,
                'company_id': self.env.user.company_id.id,
                'date': maxdate,
            })
            for expense in expense_list:
                company_currency = expense.company_id.currency_id
                diff_currency_p = expense.currency_id != company_currency
                #one account.move.line per expense (+taxes..)
                move_lines = expense._move_line_get()

                #create one more move line, a counterline for the total on payable account
                total, total_currency, move_lines = expense._compute_expense_totals(company_currency, move_lines, maxdate)
                if expense.payment_mode == 'company_account':
                    if not expense.bank_journal_id.default_credit_account_id:
                        raise UserError(_("No credit account found for the %s journal, please configure one.") % (expense.bank_journal_id.name))
                    emp_account = expense.bank_journal_id.default_credit_account_id.id
                else:
                    if not expense.employee_id.address_home_id:
                        raise UserError(_("No Home Address found for the employee %s, please configure one.") % (expense.employee_id.name))
                    emp_account = expense.employee_id.address_home_id.property_account_payable_id.id

                move_lines.append({
                        'type': 'dest',
                        'name': expense.employee_id.name,
                        'price': total,
                        'account_id': emp_account,
                        'date_maturity': expense.date,
                        'amount_currency': diff_currency_p and total_currency or False,
                        'currency_id': diff_currency_p and expense.currency_id.id or False,
                        'ref': expense.employee_id.address_home_id.ref or False
                        })

                #convert eml into an osv-valid format
                lines = map(lambda x:(0, 0, expense._prepare_move_line(x)), move_lines)
                move.write({'line_ids': lines})
                expense.write({'account_move_id': move.id, 'state': 'post'})
                if expense.payment_mode == 'company_account':
                    expense.paid_expenses()
            # move.post()
        return True

    # Overridden:
    @api.multi
    def refuse_expenses(self, reason):

        for expense in self:
            if expense.account_move_id:
                for aml in expense.account_move_id.line_ids:
                    if aml.reconciled:
                         raise UserError(
                             _('Please unreconcile payment accounting entries before cancelling this expense'))
                ### Then we unlink the move line
                expense.account_move_id.unlink()

        self.write({'state': 'cancel'})
        if self.employee_id.user_id:
            body = (_("Your Expense %s has been refused.<br/><ul class=o_timeline_tracking_value_list><li>Reason<span> : </span><span class=o_timeline_tracking_value>%s</span></li></ul>") % (self.name, reason))
            self.message_post(body=body, partner_ids=[self.employee_id.user_id.partner_id.id])

    # Overridden:
    @api.multi
    def approve_expenses(self):
        for expense in self:
            if expense.account_move_id:
                expense.account_move_id.button_validate()
        self.write({'state': 'approve'})


    # -- deep: added
    @api.multi
    def action_open_move(self):
        self.ensure_one()
        if not self.account_move_id:
            return False

        view = self.env.ref('account.view_move_form')
        return {
            'name': _('Journal Entry'),
            'context': self._context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.account_move_id.id,
            'views': [(view.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


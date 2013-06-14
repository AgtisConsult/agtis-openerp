# -*- encoding: utf-8 -*-
#################################################################################
#                                                                               #
# Copyright (C) 2013 Agtis Consultoria                                          #
#                                                                               #
#This program is free software: you can redistribute it and/or modify           #
#[M 4#it under the terms of the GNU Affero General Public License as published by#
#the Free Software Foundation, either version 3 of the License, or              #
#(at your option) any later version.                                            #
#                                                                               #
#This program is distributed in the hope that it will be useful,                #
#but WITHOUT ANY WARRANTY; without even the implied warranty of                 #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                  #
#GNU Affero General Public License for more details.                            #
#                                                                               #
#You should have received a copy of the GNU Affero General Public License       #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.          #
#################################################################################



from lxml import etree
from lxml.etree import ElementTree
from lxml.etree import Element, SubElement
from osv import fields, osv
from pprint import pprint
import decimal_precision as dp
import re, string
from unicodedata import normalize
import netsvc
import base64






class invoice(osv.osv):
    _inherit = "account.invoice"
    

    def action_move_create(self, cr, uid, ids, context=None):
        prod_obj = self.pool.get('product.product')
        inv_obj = self.pool.get('account.invoice')
        res = super(invoice, self).action_move_create(cr, uid, ids)
        for inv in inv_obj.browse(cr, uid, ids):
            if inv.ind_is_charging:
                for line in inv.invoice_line:
                    prod_obj.write(cr, uid, line.product_id.id, vals={'list_price': line.price_unit })
        return res
    
    def _get_agtis_industry_values(self, cr, uid, ids, field_name, arg, context):
        res = {}
        
        inv_brw = self.browse(cr, uid, ids)
        for inv in inv_brw:
            
            inv_is_shipment =False 
            inv_is_return = False
            inv_is_charging = False
            
            res[inv.id] = {}
            
            res[inv.id]['ind_shipment_invoice_ids'] = []
            res[inv.id]['ind_return_invoice_ids'] = []
            res[inv.id]['ind_charging_invoice_ids'] = []
            
            # para ver o que é a nota em questão (remessa, retorno, cobrança, outros)            
            for cfop in inv.cfop_ids:
                if cfop.code in ['1901','2901','3901']:
                    inv_is_shipment = True
                if cfop.code in ['5902','6902','7902','5903','6903','7903']:
                    inv_is_return = True
                if cfop.code in ['5124','6124','7124']:
                    inv_is_charging = True
                    
            res[inv.id]['ind_is_shipment'] = inv_is_shipment
            res[inv.id]['ind_is_return'] = inv_is_return
            res[inv.id]['ind_is_charging'] = inv_is_charging
        
            for rel_ind_inv in inv.ind_invoice_ids:
                 
                # tem retorno
                has_return = False
                # tem cobranca
                has_charge = False
                
                for cfop in rel_ind_inv.cfop_ids:
                    if cfop.code in ['1901','2901','3901']:
                        res[inv.id]['ind_shipment_invoice_ids'].append(rel_ind_inv.id)
                    if cfop.code in ['5902','6902','7902','5903','6903','7903']:
                        
                        has_return = True
                        res[inv.id]['ind_return_invoice_ids'].append(rel_ind_inv.id)
                    if cfop.code in ['5124','6124','7124']:
                        has_charge = True
                        res[inv.id]['ind_charging_invoice_ids'].append(rel_ind_inv.id)
                
                res[inv.id]['ind_return_state'] = ''
                res[inv.id]['ind_charging_state'] = ''
                
                if inv_is_shipment:
                    if has_return:
                        # retornada
                        res[inv.id]['ind_return_state'] = 'returned'  
                    else:
                        # sem retorno
                        res[inv.id]['ind_return_state'] = 'no_return'
                if inv_is_return:
                    if has_charge:
                        # cobrada
                        res[inv.id]['ind_charging_state'] = 'charged'
                    else:
                        # sem cobrança
                        res[inv.id]['ind_charging_state'] = 'no_charge'
            

        
        return res
            
    _columns = {
        'ind_invoice_ids':fields.many2many(
                        'account.invoice',
                        'account_invoice_industry_rel',
                        'actual_invoice_id',
                        'other_invoice_id',
                        'Faturas Relacionadas - Industrialização'
                        ),
        'ind_shipment_invoice_ids': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'one2many',
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Faturas de entrada p/ industrialização',
                                    multi='agtis_industry'
                                                    ),
            
        'ind_return_invoice_ids': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'one2many',
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Faturas de retorno',
                                    multi='agtis_industry'
                                                    ),
                
        'ind_charging_invoice_ids': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'one2many',
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Faturas de Cobrança',
                                    multi='agtis_industry'
                                                    ),
        'ind_return_state': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'char',
                                    size = 32,
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Status',
                                    multi='agtis_industry'
                                                    ),
        'ind_charging_state': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'char',
                                    size = 32,
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Status',
                                    multi='agtis_industry'
                                                    ),
                
        'ind_is_shipment': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'boolean',
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Status',
                                    store = True,
                                    multi='agtis_industry'
                                                    ),
                
        'ind_is_return': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'boolean',
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Status',
                                    store = True,
                                    multi='agtis_industry'
                                                    ),
                
        'ind_is_charging': fields.function(
                                    _get_agtis_industry_values,
                                    type = 'boolean',
                                    obj = 'account.invoice',
                                    method = True,
                                    string = 'Status',
                                    store = True,
                                    multi='agtis_industry'
                                                    ),
                
                }
    
    
    
    def create_return_invoice(self, cr, uid, ids, context=None):
        

        if not isinstance(ids, list):
            ids = [ids]
        
        obj_invoice = self.pool.get('account.invoice') 
        obj_invoice_line = self.pool.get('account.invoice.line')
        obj_account = self.pool.get('account.account')
        obj_serie = self.pool.get('l10n_br_account.document.serie')
        
        in_invoice = obj_invoice.browse(cr,uid,ids[0])
 
        
        #TODO: VERIFICAR CONTA PARA RETORNO NAO INDUSTRIALIZADO
        line_account_id = obj_account.search(cr,uid,args=[('name','like','Industriazalição de Mercadorias')])[0]
        fiscal_document_id = self.pool.get('l10n_br_account.fiscal.document').search(cr,uid,args=[('code','=','55')])
	
        serie_id = obj_serie.search(cr,uid,args=[('fiscal_document_id','=',fiscal_document_id),('company_id','=',in_invoice.company_id.id)])
        
	obj_fo = self.pool.get('l10n_br_account.fiscal.operation')
        cfop_obj = self.pool.get('l10n_br_account.cfop')
        
        fo_id = context.get('fiscal_operation_id',False)
        if not fo_id:
            cfop_id = cfop_obj.search(cr,uid,args=[('code','=','5902')])[0]
            fo_id = obj_fo.search(cr,uid,args=[('cfop_id','=',cfop_id)])[0]  
        fo_brw = obj_fo.browse(cr,uid,fo_id)
        cfop_id = fo_brw.cfop_id.id
        
        comment=''
        if fo_brw.inv_copy_note:
            date_vals =  in_invoice.date_invoice.split('-')
            date = "%s/%s/%s"%(date_vals[2],date_vals[1],date_vals[0])
            comment = fo_brw.note.replace('*numero*',in_invoice.internal_number).replace('*dataemissao*',date)
            
        
        
        
        vals = {'journal_id':fo_brw.fiscal_operation_category_id.journal_ids[0].id,
                'document_serie_id':serie_id[0],
                'partner_id':in_invoice.partner_id.id,
                'address_invoice_id': in_invoice.address_invoice_id.id,
                'own_invoice':True,
                'account_id':fo_brw.account_id.id,
                'currency_id':in_invoice.currency_id.id,
                'state':'draft',
                'company_id':in_invoice.company_id.id,
                'fiscal_type':'product',
                'fiscal_document_id':in_invoice.fiscal_document_id.id,
                'fiscal_operation_category_id':fo_brw.fiscal_operation_category_id.id,
                'fiscal_operation_id':fo_id,
                'comment':comment,
                'ind_is_return': True
                }

        out_invoice_id = obj_invoice.create(cr,uid,vals=vals,context={'type':'out_invoice'})
        out_invoice = obj_invoice.browse(cr,uid,out_invoice_id)
        
        out_invoice.write({'ind_invoice_ids':[(4, in_invoice.id)]})
        in_invoice.write({'ind_invoice_ids':[(4, out_invoice.id)]})
                    
        for line in in_invoice.invoice_line:
            
            line_vals = {
                'product_id':line.product_id.id,
                'name':line.product_id.name,
                'quantity':line.quantity,
                'price_unit':line.price_unit,
                'discount':line.discount,
                'price_subtotal': line.price_subtotal,
                'price_total': line.price_total,
                'invoice_id': out_invoice.id,
                'fiscal_operation_category_id':fo_brw.fiscal_operation_category_id.id,
                'fiscal_operation_id':fo_id,
                'cfop_id':fo_brw.cfop_id.id,
                'account_id':line_account_id,
                'calculate_taxes':True,
                'uos_id':line.uos_id.id,
                

            }
            #TODO: REVISAR CAMPOS DE IMPOSTOS A PARTIR DA TELA DE L10N_BR IMPOSTOS NO ITENS
            new_line_id = obj_invoice_line.create(cr,uid,line_vals)
            new_line_brw = obj_invoice_line.browse(cr,uid,new_line_id)
            

            new_line_brw.write({
                #'icms_cst':line.icms_cst,
                'icms_base':line.icms_base,
                'icms_value':line.icms_value,
                'icms_percent':line.icms_percent,
                #'icms_st_cst':line.icms_st_cst,
                'icms_st_base':line.icms_st_base,
                'icms_st_base_other':line.icms_st_base_other,
                #'line.icms_st_base_type':line.icms_st_base_type,
                'icms_st_value':line.icms_st_value,
                'icms_st_percent':line.icms_st_percent,
                #'icms_st_percent_reduction':line.icms_st_percent_reduction,
                #'ipi_cst':line.ipi_cst,
                'ipi_base':line.ipi_base,
                'ipi_value':line.ipi_value,
                'ipi_percent':line.ipi_percent,
                #'pis_cst':line.pis_cst,
                'pis_base':line.pis_base,
                'pis_value':line.pis_value,
                'pis_percent':line.pis_percent,
                #'cofins_cst':line.cofins_cst,
                'cofins_base':line.cofins_base,
                'cofins_value':line.cofins_value,
                'cofins_percent':line.cofins_percent,}) 
            

            view_id = self.pool.get('ir.ui.view').search(cr,uid,[('name', '=', 'account.invoice.form')])
            
	return {'type':'ir.actions.act_window',
		'res_model': 'account.invoice',
		'name':'Retorno de industrialização',
		'res_id':out_invoice.id,
		'view_id':view_id,
		'view_type':'form',
		'view_mode':'form',
		'context':{'type':'out_invoice', 'journal_type':'sale'}}
	    
    
    
        
    
    def create_charging_invoice(self, cr, uid, ids, context=None):
        if not isinstance(ids, list):
            ids = [ids]

        obj_invoice = self.pool.get('account.invoice')
        obj_invoice_line=self.pool.get('account.invoice.line')
        obj_fo = self.pool.get('l10n_br_account.fiscal.operation')
        cfop_obj = self.pool.get('l10n_br_account.cfop')
        
        
        
        cfop_id = cfop_obj.search(cr,uid,args=[('code','=','5124')])[0]
        fo_id = obj_fo.search(cr,uid,args=[('cfop_id','=',cfop_id)])[0]  
        fo_brw = obj_fo.browse(cr,uid,fo_id)
        
        
        comment=''
        if fo_brw.inv_copy_note:
            comment = fo_brw.note
        
        vals = {'fiscal_operation_category_id':fo_brw.fiscal_operation_category_id.id,
                'fiscal_operation_id':fo_id,
                'account_id':fo_brw.account_id.id,
                'comment':comment,
                'ind_is_charging':True}
        
        other_inv_ids = ids[:]
        first_invoice_id = other_inv_ids.pop(0)
                        
        charging_id = obj_invoice.copy(cr,uid,first_invoice_id,default = vals)
        charding_invoice = obj_invoice.browse(cr,uid,charging_id)
    
        # aqui é revisao na primeira nf da lista
        for line in charding_invoice.invoice_line:
            line.write({
                'calculate_taxes': True,
                'fiscal_operation_category_id': fo_brw.fiscal_operation_category_id.id,
                'fiscal_operation_id':fo_id,
                'cfop_id':fo_brw.cfop_id.id,
                'price_unit':line.product_id.list_price,}) 
        
        return_invoices_brw = obj_invoice.browse(cr,uid,ids)        
        
        for return_invoice in return_invoices_brw:
            if return_invoice.id != first_invoice_id:
                for other_inv_line in return_invoice.invoice_line:
                    obj_invoice_line.copy(cr,uid,other_inv_line.id,
                        default={
                            'invoice_id':charding_invoice.id,
                            'calculate_taxes': True,
                            'fiscal_operation_category_id': fo_brw.fiscal_operation_category_id.id,
                            'fiscal_operation_id':fo_id,
                            'cfop_id':fo_brw.cfop_id.id,
                            'price_unit':other_inv_line.product_id.list_price,
                        }
                    )
            charding_invoice.write({'ind_invoice_ids':[(4, return_invoice.id)]})
            return_invoice.write({'ind_invoice_ids':[(4, charding_invoice.id)]})
        
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[('name', '=', 'account.invoice.form')])
        return {'type':'ir.actions.act_window',
                    'res_model': 'account.invoice',
                    'name':'Cobrança de industrialização',
                    'res_id':charding_invoice.id,
                    'view_id':view_id,
                    'view_type':'form',
                    'view_mode':'form',
                    'context':{'type':'out_invoice', 'journal_type':'sale'}}
          
          
    

         
invoice()


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"
    
    def _amount_line_ex(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = super(account_invoice_line,self)._amount_line(cr, uid, ids, prop, unknow_none, unknow_dict)        
        for line in self.browse(cr,uid,ids):
            if (not line.invoice_id.own_invoice) or (not line.calculate_taxes):
                cr.execute("""             
                    SELECT 
                        cofins_base    ,
                        cofins_base_other    ,
                        cofins_cst    ,
                        cofins_percent    ,
                        cofins_value    ,
                        icms_base    ,
                        icms_base_other    ,
                        icms_cst    ,
                        icms_percent    ,
                        icms_percent_reduction    ,
                        icms_st_base    ,
                        icms_st_base_other    ,
                        icms_st_mva    ,
                        icms_st_percent    ,
                        icms_st_value    ,
                        icms_value    ,
                        ipi_base    ,
                        ipi_base_other    ,
                        ipi_cst    ,
                        ipi_percent    ,
                        ipi_type    ,
                        ipi_value    ,
                        pis_base    ,
                        pis_base_other    ,
                        pis_cst    ,
                        pis_percent    ,
                        pis_value    ,
                        price_subtotal,
                        price_total
                    FROM account_invoice_line
                    WHERE id=%s
                """ % (line.id ) )
                ret_line = cr.dictfetchone()
                res[line.id].update(ret_line)                    
        return res
    
    def _amount_line_write_ex(self, cr, uid, ids, prop, values, unknow_none, unknow_dict):
        
        if isinstance(values, unicode) or isinstance(values, str):
            valupd = "'" + values + "'"
        else:
            valupd = values
            
        
        upd_cmd = """
            UPDATE account_invoice_line
            SET %s=%s
            WHERE id=%s
        """ % (prop,valupd or 'NULL' ,ids)
        cr.execute(upd_cmd)
        
    
    _columns = {
                'calculate_taxes': fields.boolean('Calcular os Impostos'),
                'price_subtotal': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Subtotal', type="float",
                                                  digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'price_total': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Total', type="float",
                                               digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_base': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base ICMS', type="float",
                                             digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_base_other': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base ICMS Outras', type="float",
                                             digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_value': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Valor ICMS', type="float",
                                              digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_percent': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Perc ICMS', type="float",
                                                digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_percent_reduction': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Perc Redução de Base ICMS', type="float",
                                                digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_st_value': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Valor ICMS ST', type="float",
                                              digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_st_base': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base ICMS ST', type="float",
                                              digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_st_percent': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Percentual ICMS ST', type="float",
                                              digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_st_mva': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='MVA ICMS ST', type="float",
                                              digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_st_base_other': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base ICMS ST Outras', type="float",
                                              digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'icms_cst': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='CST ICMS', type="char", size=3,
                                              store=True, multi='all'),
                'ipi_type': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Tipo do IPI', type="char", size=64,
                                              store=True, multi='all'),
                'ipi_base': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base IPI', type="float",
                                            digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'ipi_base_other': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base IPI Outras', type="float",
                                            digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'ipi_value': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Valor IPI', type="float",
                                                  digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'ipi_percent': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Perc IPI', type="float",
                                               digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'ipi_cst': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='CST IPI', type="char", size=2,
                                           store=True, multi='all'),
                'pis_base': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base PIS', type="float",
                                                  digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'pis_base_other': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base PIS Outras', type="float",
                                                  digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'pis_value': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Valor PIS', type="float",
                                             digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'pis_percent': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Perc PIS', type="float",
                                               digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'pis_cst': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='CST PIS', type="char", size=2,
                                           store=True, multi='all'),
                'cofins_base': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base COFINS', type="float",
                                               digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'cofins_base_other': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Base COFINS Outras', type="float",
                                               digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'cofins_value': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Valor COFINS', type="float",
                                                digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'cofins_percent': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Perc COFINS', type="float",
                                                  digits_compute= dp.get_precision('Account'), store=True, multi='all'),
                'cofins_cst': fields.function(_amount_line_ex, fnct_inv=_amount_line_write_ex, method=True, string='Valor COFINS', type="char", size=2,
                                              store=True, multi='all'),
    }
    _defaults = {
                 'calculate_taxes': True,
                 }
    
    def copy(self,cr, uid, id, default=None, context=None):
        default = default or {}
        line = self.browse(cr, uid, id)
        default.update({
            'price_total':line.price_total,
            'price_subtotal':line.price_subtotal,
            'discount':line.discount,
        })
        return super(account_invoice_line, self).copy(cr, uid, id, default, context)
    
    
    def uos_id_change(self, cr, uid, ids, product, uom, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, address_invoice_id=False, currency_id=False, context=None, company_id=None,fiscal_operation_category_id=None,fiscal_operation_id=None):

        if context is None:
            context = {}   
        result =  super(account_invoice_line, self).uos_id_change( cr, uid, ids, product, uom, qty, name, type, partner_id, fposition_id, price_unit, address_invoice_id, currency_id, context, company_id)
        result['values']['fiscal_operation_id'] = fiscal_operation_id
        result['values']['fiscal_operation_category_id'] = fiscal_operation_category_id
        if fiscal_operation_id:
            cfop_id = self.pool.get('l10n_br_account.fiscal.operation').browse(cr,uid,fiscal_operation_id).cfop_id.id
        result['values']['cfop_id'] = cfop_id
        
        return result
account_invoice_line()


class fiscal_operation(osv.osv):
    _inherit = "l10n_br_account.fiscal.operation"
    _columns = {
                'account_id': fields.many2one(
                                'account.account',
                                'Conta',)

                }
fiscal_operation()

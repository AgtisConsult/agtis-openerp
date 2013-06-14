# -*- encoding: utf-8 -*-
#################################################################################
#                                                                               #
# Copyright (C) 2013 Agtis Consultoria                                          #
#                                                                               #
#This program is free software: you can redistribute it and/or modify           #
#it under the terms of the GNU Affero General Public License as published by    #
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

from osv import fields, osv


class nfe_batch(osv.osv):
    _name="account.invoice.nfe.batch"
    _columns={
             'batch_number': fields.integer('Numero do Lote',required=True),
             'invoice_id': fields.many2one('account.invoice',
                                            'Fatura'),
              'return_edoc':fields.char('Retorno Edoc',size=255)
              }
     
    def get_next_batch_number(self, cr, uid, ids, context=None):
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, uid)
        batch_number = user.company_id.edoc_nfe_prox_lote
        
        
        return batch_number
    
    
    def create_record_batch(self, cr, uid, ids, context=None,invoice_id=None):
        batch_obj = self.pool.get('account.invoice.nfe.batch')
        newid= batch_obj.create(cr, uid, {'batch_number':batch_obj.get_next_batch_number(cr, uid, ids),
                                   'invoice_id':invoice_id},
                          context=context)
        
        batch_obj.increment_batch_number(cr, uid, ids)
        
        return newid
    
    def increment_batch_number(self, cr, uid, ids, context=None):
        batch_obj = self.pool.get('account.invoice.nfe.batch')
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, uid)
        company = user.company_id
        company.write({'edoc_nfe_prox_lote':batch_obj.get_next_batch_number(cr, uid, ids)+1})


nfe_batch()
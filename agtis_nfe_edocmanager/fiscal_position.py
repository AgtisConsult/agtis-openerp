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
import httplib, urllib ,base64,requests
import netsvc
from pprint import  pprint
from requests.exceptions import ConnectionError
import libxml2
from tools import config
from tools.translate import _
import decimal_precision as dp
import random
import sys, os
from datetime import datetime

import re, string
from unicodedata import normalize
from pprint import pprint

LOGGER = netsvc.Logger()

class fiscal_position(osv.osv):
    _inherit="account.fiscal.position"
    
    _columns = {
        'mirror_mappings_on':fields.many2one('account.fiscal.position', 'Espelhar Impostos em')
    }

    def update_mirrored(self, cr, uid, ids):
        #print "------------------------- fiscal_position -- update_mirrored "
        # nesta funcao são atualizado são atualizadas posições fiscais espelhadas em outras
        #
        if not isinstance(ids, list):
            ids = [ids]
        fp_obj = self.pool.get("account.fiscal.position")
        fp_tax_obj = self.pool.get("account.fiscal.position.tax")
        fp_brw = fp_obj.browse(cr, uid, ids)
        for fp in fp_brw:
            mirrored_ids = fp_obj.search(cr, uid, args=[('mirror_mappings_on','=',fp.id)])
            #print "------------------------- fiscal_position -- mirrored_ids =  ", pprint(mirrored_ids)
            if mirrored_ids:
                if not isinstance(mirrored_ids, list):
                    mirrored_ids = [mirrored_ids]
                mirrored_brw = fp_obj.browse(cr, uid, mirrored_ids)
                for mirrored in mirrored_brw:
                    for mirrored_tax in mirrored.tax_ids:
                            mirrored_tax.unlink(context={'updating_mirrored': True})
                    for base_tax in fp.tax_ids: 
                        fp_tax_obj.create(cr, uid, {
                            'tax_src_id': base_tax.tax_src_id.id,
                            'tax_dest_id': base_tax.tax_dest_id.id,
                            'position_id': mirrored.id
                        }, context={'updating_mirrored': True})
        return True
    
    def write(self, cr, uid, ids, vals, context=None):
        #print "------------------------- fiscal_position -- write "
        fp_obj = self.pool.get("account.fiscal.position")
        res = super(fiscal_position, self).write(cr, uid, ids, vals, context=context)        
        #print "hask=", context.has_key('updating_mirrored')
        self.update_mirrored(cr, uid, ids)
        for fp in fp_obj.browse(cr, uid, ids):
            if fp.mirror_mappings_on:
                self.update_mirrored(cr, uid, fp.mirror_mappings_on.id)
        return res

fiscal_position()


#class fiscal_position_tax(osv.osv):
#    _inherit="account.fiscal.position.tax"
#
#    def write(self, cr, uid, ids, vals, context=None):
#        print "------------------------- fiscal_position_tax -- write "
#        if context is None:
#            context = {}
#        fp_tax_obj = self.pool.get("account.fiscal.position.tax")
#        if not isinstance(ids, list):
#            ids = [ids]
#        res = super(fiscal_position_tax, self).write(cr, uid, ids, vals, context=context)
#        if not context.has_key('updating_mirrored'):
#            tax_brw = fp_tax_obj.browse(cr, uid, ids)
#            for tax in tax_brw:
#                tax.position_id.update_mirrored(tax.position_id.id)
#        return res
#
#    def create(self, cr, uid, vals, context=None):
#        print "------------------------- fiscal_position_tax -- create "
#        if context is None:
#            context = {}
#        fp_tax_obj = self.pool.get("account.fiscal.position.tax")
#        res = super(fiscal_position_tax, self).create(cr, uid, vals, context=context)        
#        if not context.has_key('updating_mirrored'):
#            tax = fp_tax_obj.browse(cr, uid, res)
#            tax.position_id.update_mirrored(tax.position_id.id)
#        return res
#
#    def unlink(self, cr, uid, ids, context=None):
#        print "------------------------- fiscal_position_tax -- unlink "
#        if context is None:
#            context = {}
#        fp_tax_obj = self.pool.get("account.fiscal.position.tax")
#        if not isinstance(ids, list):
#            ids = [ids]
#        #tax_brw = fp_tax_obj.browse(cr, uid, ids)
#        upd_pos_map = {}
#        #for tax in tax_brw:
#        #    upd_pos_map[tax.position_id.id] = tax.position_id.id
#        res = super(fiscal_position_tax, self).unlink(cr, uid, ids, context=context)        
#        #if not context.has_key('updating_mirrored'):
#        #    tax.position_id.update_mirrored(upd_pos_map.keys())
#        return res
#
#fiscal_position_tax()




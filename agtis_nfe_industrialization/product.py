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


from osv import fields, osv


class product(osv.osv):
    _inherit = "product.product"
    
    
    def copy(self, cr, uid, id, default=None, context={}):
        if not default:
            default={}
        product_brw = self.pool.get('product.product').browse(cr,uid,id)
        if product_brw.property_fiscal_classification:
            default.update({'property_fiscal_classification':product_brw.property_fiscal_classification.id})
        
        
        return super(product, self).copy(cr, uid, id, default=default,context=context)
    
    
product()

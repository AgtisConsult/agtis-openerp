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

from lxml import etree
from lxml.etree import ElementTree
from lxml.etree import Element, SubElement
import time
from datetime import datetime
import netsvc
import re
import string
from unicodedata import normalize

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'

    _columns = {
                    'price_unit': fields.float('Unit Price', required=True,
                    digits_compute= dp.get_precision('Account unit price')),
               }


account_invoice_line()

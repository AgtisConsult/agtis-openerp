# -*- encoding: utf-8 -*-

from osv import fields,osv


class nfe_cancel (osv.osv_memory):
    _name="account.invoice.nfe.sefaz.cancel"
    _columns={
              'justificativa': fields.char('Justificativa',size=255,required=True),
              }
    
    def do_nfe_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = []
        
        justificativa = self.browse(cr, uid, ids,context=context)[0].justificativa
        
        invoice_obj = self.pool.get('account.invoice')
        invoice_id = context.get('active_id')
        invoice = invoice_obj.browse(cr,uid,[invoice_id])[0]
        invoice.nfe_edoc_cancel(justificativa=justificativa)

        
        return True

nfe_cancel()    


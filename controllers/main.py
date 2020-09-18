from odoo import http
from odoo.http import request


class Api(http.Controller):
    @http.route('/api/product/', type="json", website=True, auth='public', methods=['POST'])
    def api_get_id(self, **rec):
        try:
            barcode = request.params.get('barcode')
            ids = request.env['product.template'].search(
                [['barcode', '=', barcode]])
            body = {'status': 'OK', 'id': ids.id}

        except:
            body = {'status': 'ERROR'}

        return body

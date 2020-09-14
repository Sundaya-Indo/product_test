import json
from odoo.http import Response
from odoo import http
from odoo.http import request


class Api(http.Controller):
    @http.route('/api/product/<string:barcode>/', website=True, auth='public')
    def api_get_id(self, barcode, **rec):
        try:
            headers = {'Content-Type': 'application/json'}
            ids = request.env['product.template'].search(
                [['barcode', '=', barcode]])
            body = {'status': 'OK', 'id': ids.id}

        except:
            headers = {'Content-Type': 'application/json'}
            body = {'status': 'ERROR'}

        return Response(json.dumps(body), headers=headers)

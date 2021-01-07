from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, pycompat

from itertools import groupby

class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    image_small_id = fields.Binary(related='product_tmpl_id.image_small', string='Image Small', compute='_compute_images', inverse='_set_image_small')

    item_code = fields.Char(related='product_tmpl_id.barcode', string='Item Code')


class MrpBomLine(models.Model):

    _inherit = 'mrp.bom.line'

    image_small_id = fields.Binary(related='product_id.image_small', string='Image Small', compute='_compute_images', inverse='_set_image_small')


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    product_id = fields.Many2one('product.product', 'Product D')

    @api.model
    def get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        lines = self._get_bom(bom_id=bom_id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
        return self.env.ref('mrp.report_mrp_bom_line').render({'data': lines})

    @api.model
    def _get_report_data(self, bom_id, searchQty=0, searchVariant=False):
        lines = {}
        bom = self.env['mrp.bom'].browse(bom_id)
        bom_quantity = searchQty or bom.product_qty
        bom_product_variants = {}
        bom_uom_name = ''

        if bom:
            bom_uom_name = bom.product_uom_id.name

            # Get variants used for search
            if not bom.product_id:
                for variant in bom.product_tmpl_id.product_variant_ids:
                    bom_product_variants[variant.id] = variant.display_name

        lines = self._get_bom(bom_id, product_id=searchVariant, line_qty=bom_quantity, level=1)
        # lines.update({'sorting_data': self._sorting_data(lines.get('components'))})
        return {
            'lines': lines,
            'variants': bom_product_variants,
            'bom_uom_name': bom_uom_name,
            'bom_qty': bom_quantity,
            'is_variant_applied': self.env.user.user_has_groups('product.group_product_variant') and len(bom_product_variants) > 1,
            'is_uom_applied': self.env.user.user_has_groups('uom.group_uom')
        }

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        data_test = [
            {
                "name": None,
                "level": None,
                "child": [
                {
                    "level": 1,
                    "name": "DC Energy Meter IC",
                    "child_bom": False,
                    "parent_id": 1
                },
                {
                    "level": 1,
                    "name": "Chip Resistor (10R, +/- 1%)",
                    "child_bom": False,
                    "parent_id": 1
                },
                {
                    "level": 1,
                    "name": "Chip Capasitor (100uF)",
                    "child_bom": False,
                    "parent_id": 1
                },
                {
                    "level": 1,
                    "name": "Test Energy",
                    "child_bom": 4,
                    "parent_id": 1
                },
                {
                    "level": 1,
                    "name": "Test Voltage",
                    "child_bom": 7,
                    "parent_id": 1
                }
                ]
            },
            {
                "child": [
                {
                    "level": 2,
                    "name": "AI",
                    "child_bom": False,
                    "parent_id": 4
                },
                {
                    "level": 2,
                    "name": "3pole Latch Relay",
                    "child_bom": False,
                    "parent_id": 4
                },
                {
                    "level": 2,
                    "name": "Test Meter",
                    "child_bom": 5,
                    "parent_id": 4
                }
                ],
                "name": "Test Energy",
                "level": 2
            },
            {
                "child": [
                {
                    "level": 2,
                    "name": "ACP Mounting Beam",
                    "child_bom": False,
                    "parent_id": 7
                },
                {
                    "level": 2,
                    "name": "15x2mm Strip Profile",
                    "child_bom": False,
                    "parent_id": 7
                }
                ],
                "name": "Test Voltage",
                "level": 2
            },
            {
                "child": [
                {
                    "level": 3,
                    "name": "BMS",
                    "child_bom": False,
                    "parent_id": 5
                },
                {
                    "level": 3,
                    "name": "Battery Casing",
                    "child_bom": False,
                    "parent_id": 5
                },
                {
                    "level": 3,
                    "name": "Test Power",
                    "child_bom": 6,
                    "parent_id": 5
                }
                ],
                "name": "Test Meter",
                "level": 3
            },
            {
                "child": [
                {
                    "level": 4,
                    "name": "15x2mm Strip Profile",
                    "child_bom": False,
                    "parent_id": 6
                },
                {
                    "level": 4,
                    "name": "AI",
                    "child_bom": False,
                    "parent_id": 6
                },
                {
                    "level": 4,
                    "name": "Test Voltage",
                    "child_bom": 7,
                    "parent_id": 6
                }
                ],
                "name": "Test Power",
                "level": 4
            },
            {
                "child": [
                {
                    "level": 5,
                    "name": "ACP Mounting Beam",
                    "child_bom": False,
                    "parent_id": 7
                },
                {
                    "level": 5,
                    "name": "15x2mm Strip Profile",
                    "child_bom": False,
                    "parent_id": 7
                }
                ],
                "name": "Test Voltage",
                "level": 5
            }
            ]
        bom = self.env['mrp.bom'].browse(bom_id)
        bom_quantity = line_qty
        if line_id:
            current_line = self.env['mrp.bom.line'].browse(int(line_id))
            bom_quantity = current_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id)
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        if product:
            attachments = self.env['mrp.document'].search(['|', '&', ('res_model', '=', 'product.product'),
            ('res_id', '=', product.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', product.product_tmpl_id.id)])
        else:
            product = bom.product_tmpl_id
            attachments = self.env['mrp.document'].search([('res_model', '=', 'product.template'), ('res_id', '=', product.id)])
        if bom.product_qty != 0.0:
            operations = self._get_operation_line(bom.routing_id, float_round(bom_quantity / bom.product_qty, precision_rounding=1, rounding_method='UP'), 0)
            lines = {
                'bom': bom,
                'bom_qty': bom_quantity,
                'bom_prod_name': product.display_name,
                'currency': self.env.user.company_id.currency_id,
                'product': product,
                'code': bom and self._get_bom_reference(bom) or '',
                'price': product.uom_id._compute_price(product.standard_price, bom.product_uom_id) * bom_quantity,
                'total': sum([op['total'] for op in operations]),
                'level': level or 0,
                'operations': operations,
                'operations_cost': sum([op['total'] for op in operations]),
                'attachments': attachments,
                'operations_time': sum([op['duration_expected'] for op in operations]),
                'image': product.image_small,
                'qty_available': product.qty_available,
                'product_qty': bom.product_qty,
                'stock_value': round(product.qty_available) * round(product.standard_price),
                'item_code': product.barcode,
                'link': product.id,
            }
            # components, total, total_svalue, components_list, build_data, sorting_data = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
            components, total, total_svalue, = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
            lines['components'] = components
            lines['total'] += total
            lines['total_svalue'] = total_svalue
            # lines['components_list'] = components_list
            # lines['build_data'] = self._build_data(components)
            lines['test_data'] = data_test
            lines['sorting_data'] = self._sorting_data(components)
            # build_data = self._build_data(components)
            # lines['transform'] = self._transform_data(components)
            return lines
        return None

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components = []
        total = 0
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            if line._skip_bom_line(product):
                continue
            price = line.product_id.uom_id._compute_price(line.product_id.standard_price, line.product_uom_id) * line_quantity
            if line.child_bom_id:
                factor = line.product_uom_id._compute_quantity(line_quantity, line.child_bom_id.product_uom_id) / line.child_bom_id.product_qty
                sub_total = self._get_price(line.child_bom_id, factor, line.product_id)
            else:
                sub_total = price
            sub_total = self.env.user.company_id.currency_id.round(sub_total)
            components.append({
                'prod_id': line.product_id.id,
                'prod_name': line.product_id.display_name,
                'code': line.child_bom_id and self._get_bom_reference(line.child_bom_id) or '',
                'prod_qty': line_quantity,
                'prod_uom': line.product_uom_id.name,
                'prod_cost': self.env.user.company_id.currency_id.round(price),
                'parent_id': bom.id,
                'line_id': line.id,
                'level': level or 0,
                'total': sub_total,
                'child_bom': line.child_bom_id.id,
                'child_bom_data': self._get_bom(bom_id=line.child_bom_id.id, product_id=line.child_bom_id.product_id.id),
                'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
                'attachments': self.env['mrp.document'].search(['|', '&',
                    ('res_model', '=', 'product.product'), ('res_id', '=', line.product_id.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', line.product_id.product_tmpl_id.id)]),
                'image': line.product_id.image_small,
                'qty_available': line.product_id.qty_available,
                'prod_price': line.product_id.standard_price,
                'product_qty': line.product_qty,
                'stock_value': line.product_id.qty_available * line.product_id.standard_price,
                'item_code': line.product_id.barcode,

            })
            total += sub_total
        components_stock_value = sum([component.get('stock_value') for component in components])
        # components_list = self._transform_data(components)
        # build_data = self._build_data(components)
        # sorting_data = self._sorting_data(components)
        # transform_data = self._transform_data(components)
    
        return components, total, components_stock_value,
        # return components, total, components_stock_value, components_list, build_data, sorting_data,

    # def _transform_data(self, components):
    #     list_data = []
    #     for component in components:
    #         child_bom_data = component.get('child_bom_data')
    #         if child_bom_data is not None:
    #             component_data = self._transform_data(child_bom_data.get('components'))
    #         else:
    #             component_data = False
    #         list_data.append([child_bom_data, component_data])
    #     return list_data

    def _build_data(self, components, arr = [], level = 0):
        level += 1
        list_bom = arr
        if isinstance(components, dict):
            components = components.get('components')
        for item in components:
            list_bom.append({'level': level, 'name': item["prod_name"], 'child_bom':item["child_bom"], 'parent_id': item['parent_id']})
            if item["child_bom_data"]:
                self._build_data(item["child_bom_data"], list_bom, level)
        return list_bom

    def _get_parent(self, data, parent_id):
        for d in range(len(data)):
            if data[d]["child_bom"] == parent_id:
                return data[d]

    def _sorting_data(self, components):
        data = self._build_data(components, arr = [])
        data.sort(key=lambda key: key.get('level'))
    #     max_level = max([d.get('level') for d in data])
    #     result_list = []
    #     level_list = [[d for d in data if d.get('level') == lvl] for lvl in range(1, max_level+1)]
    #     new_list = level_list.copy()
    #     level_list.insert(0, [{'name': 0, 'level': 0, 'child_bom': level_list[0][0]['parent_id']}])
    #     for level in level_list:
    #         data_list= []
    #         for lvl in level:
    #             data_child_list = []
    #             for new in new_list:
    #                 for n in new:
    #                     if lvl['child_bom']:
    #                         cond1 = lvl['child_bom'] == n['parent_id']
    #                         cond2 = (lvl['level'] + 1) == n['level']
    #                         if cond1 and cond2:
    #                             data_child_list.append(n)
    #             if lvl['child_bom']:
    #                 lvl.update({'level': lvl.get('level') + 1})
    #                 result_list.append({**lvl, "child": data_child_list})
    #     return result_list
        tmpParentId = data[0]["parent_id"]
        arr = []
        obj = {'name': None, 'level': None, 'child': []}
        arrParent = []
        for d in range(len(data)):
            if data[d]["child_bom"]:
                arrParent.append(data[d])
            if tmpParentId == data[d]["parent_id"]:
                obj["child"].append(data[d])
            else:
                if data[d-1]["level"] != 1:
                    parentData = self._get_parent(arrParent, tmpParentId)
                    if parentData is not None:
                        obj["name"] = parentData["name"]
                        obj["level"] = data[d-1]["level"]
                arr.append(obj)
                obj = {'child': []}
                obj["child"].append(data[d])
                tmpParentId = data[d]["parent_id"]
            if d + 1 == len(data):
                parentData = self._get_parent(arrParent, tmpParentId)
                if parentData is not None:
                    obj["name"] = parentData["name"]
                    obj["level"] = data[d-1]["level"]
                arr.append(obj)
        return arr
        
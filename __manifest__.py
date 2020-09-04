
{
  'name': 'Jarvis',
  'author': 'Sundaya IT Team',
  'version': '1.1.4',
  'depends': [
    # 'nama_modul',
    'stock',
    'purchase',
    'contacts',
    'crm',
  ],
  'data': [
    'views/product_template.xml',
    'views/template.xml',
    'views/attachments_tree.xml',
    'views/login.xml',
    'views/edit_inventory.xml',
    'views/contact_template.xml',
    'views/employee_template.xml',
    'views/company_template.xml',
    'views/crm_lead_template.xml',
    'views/mrp_production_views.xml',
    'views/stock_production_lot_views.xml',
  ],
  'qweb': [
    'static/src/xml/marker_color.xml',
  ],
  'sequence': 3,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': 'Enterprise Resource Planning',
  'summary': 'Jarvis System for Sundaya',
  'license': 'OPL-1',
  'website': 'https://github.com/Sundaya-Indo/product_test',
  'description': '-'
}

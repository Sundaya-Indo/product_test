
{
  'name': 'Jarvis',
  'author': 'Sundaya IT Team',
  'version': '0.1',
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
  ],
  'qweb': [
    # 'static/src/xml/nama_widget.xml',
  ],
  'sequence': 3,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': 'Enterprise Resource Planning',
  'summary': 'Jarvis System for Sundaya',
  'license': 'OPL-1',
  'website': 'www.sundaya.com',
  'description': '-'
}

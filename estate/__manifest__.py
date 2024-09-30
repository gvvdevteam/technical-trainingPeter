{
    "name": "Estate",  # The name that will appear in the App list
    "version": "17.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        'data/ir.model.access.csv',
        'actions/estate_property_action.xml',
        'menu/estate_property_menu.xml',
        'views/estate_property_view.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
}

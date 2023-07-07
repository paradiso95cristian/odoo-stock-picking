# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Preprinted Report",
    "summary": """
        This module adds functionality and a new design for pre-printed delivery notes.
    """,
    "author": "Paradiso Cristian",
    "maintainers": ["ParadisoCristian"],
    "license": "AGPL-3",
    "category": "Stock",
    "version": "15.0.1.1.1",
    "installable": True,
    "application": False,
    "depends": ['stock'],
    "data": [
        "view/template.xml",
        "view/stock_picking_view.xml",
    ],
}

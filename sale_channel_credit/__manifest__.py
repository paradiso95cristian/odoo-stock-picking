# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Channel Credit",
    "summary": """
        this module manage different sales channels to be able to
        control the sales made, as well as the delivery of the products and the invoices
        associated with those sales. In addition to controlling a credit limit per channel for your
        customers
    """,
    "author": "Paradiso Cristian",
    "maintainers": ["Paradiso Cristian"],
    "license": "AGPL-3",
    "category": "Sale",
    "version": "15.0.1.0.0",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "sale_management",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_channel_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/stock_picking_views.xml",
        "views/res_partner_views.xml",
        "views/credit_groups_views.xml",
        "views/template.xml",
    ],
}

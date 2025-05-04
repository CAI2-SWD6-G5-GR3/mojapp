import frappe

def before_uninstall():
    if frappe.db.exists("Print Format", "Iraqi Payroll Slip"):
        frappe.delete_doc("Print Format", "Iraqi Payroll Slip", ignore_permissions=True)

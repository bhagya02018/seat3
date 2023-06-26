import frappe


@frappe.whitelist()
def get_payment_terms(doctype, txt, searchfield, page_len, start, filters):
    item_code = filters.get("item_code")
    print item_code
    item = frappe.get_doc("Item",item_code)
    pt = frappe.get_doc("Payment Terms Template",item.payment_terms_template)
    return frappe.db.sql("""SELECT name FROM `tabPayment Terms Template` WHERE `tabPayment Terms Template`.order <= {0}""".format(pt.order))



def validate_customer(doc, method):
    if doc.customer_id:
        if len(doc.customer_id) <= 9:
            doc.customer_id += "V"
        elif len(doc.customer_id) > 9:
            if len(doc.customer_id) == 10:
                if doc.customer_id[len(doc.customer_id)-1] != "V":
                    doc.customer_id += "X"
            elif len(doc.customer_id) > 10:
                if doc.customer_id[len(doc.customer_id)-1] != "X":
                    doc.customer_id += "X"


    if doc.sales_team_1:
        nl = doc.append('sales_team', {})
        nl.sales_person = doc.sales_team_1
        nl.allocated_percentage = 100

def filter_payment_terms(doctype, txt, searchfield, start, page_len, filters):
    item_code = filters.get('item_code')
    payment_term_template_name = frappe.get_value("Item", item_code, "payment_terms_template")
    pttn = frappe.get_doc("Payment Terms Template",payment_term_template_name)
    print("Filter Payment Terms",pttn.order)
    return frappe.db.sql("""select name from `tabPayment Terms Template`
              where `tabPayment Terms Template`.order <= {0}""".format(pttn.order))


@frappe.whitelist()
def get_guarantors(item_code):
    return frappe.db.sql("""select guarantor from `tabSales Invoice Guarantor` where parent="{}" """.format(item_code),
                         as_list=1)


# payment template name
@frappe.whitelist()
def get_template_name(doctype, txt, searchfield, page_len, start, filters):
    return frappe.db.sql(
        """select payment_term_name from `tabItem Payment Terms` where parent="{}" """.format(filters.get("item_code")))


# function for payment term method
@frappe.whitelist()
def payment_term_template_list():
    payment_name_list = []
    payment_name = frappe.db.sql("""select name from `tabPayment Terms Template` """, as_dict=1)
    for names in payment_name:
        payment_name_list.append(names['name'])
    return payment_name_list

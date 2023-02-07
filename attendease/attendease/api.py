import frappe

@frappe.whitelist()
def get_companies():
    return frappe.db.get_all("Company", fields=["*"])

@frappe.whitelist()
def new_company():
    payload = frappe.request.json
    try:
        doc = frappe.get_doc(
                {
                    "doctype": "Company",
                    "company_name": payload["company_name"],
                    "address_line_1":payload["address_line_1"],
                    "address_line_1":payload["address_line_1"],
                    "state":payload["state"],
                    "country":payload["country"],
                    "gstin":payload["gstin"],
                    "pan":payload["pan"],
                    "contact":payload["contact"],
                }
            )
        doc.insert()
        return doc.name
    except Exception as e:
        return e
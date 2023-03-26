# Copyright (c) 2023, erevive and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AttendanceLog(Document):
    def validate(self):
        if self.clock_in and self.clock_out:
            self.working_hours = round(frappe.utils.time_diff_in_hours(self.clock_out, self.clock_in))

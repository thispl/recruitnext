# -*- coding: utf-8 -*-
# Copyright (c) 2019, suganya and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
from frappe.utils import flt, getdate, get_url
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.model.document import Document
from six import BytesIO
# from docxtpl import DocxTemplate


class Candidate(Document):
    def validate(self):
        self.total_exp()
        self.check_closure_exists()
        self.validate_passport()
        self.create_closure()

    def validate_passport(self):
        if(self.passport_no):
            pp = self.passport_no
            match = re.match("[A-Z0-9]{8}$", pp)
            if not match:
                frappe.msgprint(_("{0} is not a valid Passport No").format(pp))
                self.passport_no = ''

    def check_project_details(self):
        if self.pending_for != 'IDB' or self.pending_for != 'Do Not Disturb':
            if self.project:
                frappe.msgprint(_('Supplier is mandatory'))
            elif not self.project:
                frappe.msgprint(_('Project is mandatory'))
            elif not self.task:
                frappe.msgprint(_('Task is mandatory'))

    def total_exp(self):
        if self.local_experience or self.international_experience:
            self.total_experience = self.local_experience + self.international_experience
        elif not self.local_experience and not self.international_experience:
            self.total_experience = 0

        # Check if any previous closure exists
    def check_closure_exists(self):
        closure = frappe.db.get_value("Closure", {"candidate": self.name})
        if closure:
            self.candidate_status = 'Proposed PSL'

    def check_mandatory(self):
        if self.candidate_status == 'Proposed PSL':
            self.given_name__surname

    def create_closure(self):
        if self.candidate_status == 'Proposed PSL':
            if self.original_documents:
                for docs in self.original_documents:
                    docslist = frappe.db.get_value("Original Documents",{"name": docs.name})
            closure_id = frappe.db.get_value("Closure", {"candidate": self.name})
            # interview = frappe.db.get("Candidate", docs.candidate)
            # if interview:
            #     interview_date = interview.interview_date
            project = frappe.get_doc("Project", self.project)
            task = frappe.db.get_value("Task", self.task, "subject")
            # ca_executive = frappe.db.get_value(
            #     "Customer", self.customer, "customer_owner")
            territory = frappe.db.get_value("Customer", self.customer, "territory")
            payment_terms = project.payment_terms
            # dle = ca_executive = source_executive = ''
            tl = ''
            bu = ''
            department = ''
            if self.user:
                executive = frappe.db.get("Employee", {"user_id": self.user})
                if executive:
                    source_executive = executive.user_id
                    department = executive.department
                    # bu = frappe.get_value("Employee", executive, 'business_unit')
                    # tl = frappe.db.get_value("Employee", executive.reports_to, "user_id")
                    if closure_id:
                        closure = frappe.get_doc("Closure", closure_id)
                    else:
                        closure = frappe.new_doc("Closure")
                        closure.update({
                            "supplier": self.supplier,
                            "territory": territory,
                            "project": self.project,
                            "payment_terms": payment_terms,
                            "task": self.task,
                            "candidate": self.name,
                            "name1": self.given_name__surname,
                            "designation": task,
                            "contact_no": self.mobile,
                            "current_location": self.current_location,
                            "passport_no": self.passport_no,
                            "ecr_status": self.ecr_status,
                            "expiry_date": self.expiry_date,
                            "date_of_issue": self.issued_date,
                            "place_of_issue": self.place_of_issue,
                            # "cr_executive": project.cpc,
                            # "ca_executive": ca_executive,
                            # "business_unit": bu,
                            "department": department,
                            # "division": self.division,
                            "source_executive": source_executive,
                            "selection_date": self.interview_date,
                            # "tl": tl,
                            "degree": self.degree,
                            "specialization": self.specialization,
                            "yop": self.yop,
                            "basic": self.basic,
                            "food": self.food,
                            "other_allowances": self.other_allowances,
                            "date_of_birth": self.date_of_birth
                        })
                        if self.irf:
                            closure.update({"irf": self.irf})
                        if self.candidate_image:
                            closure.update({"photo": self.candidate_image})
                        if self.passport:
                            closure.update({"passport": self.passport})
                        if self.candidate_payment_applicable and flt(self.service_charge_candidate) > 0:
                            closure.update({
                                "candidate_payment_applicable": 1,
                                "service_charge_candidate": self.service_charge_candidate
                            })
                    closure.save(ignore_permissions=True)

#     def _fill_template(template, data):
#     """
#     Fill a word template with data.

#     Makes use of BytesIO to write the resulting file to memory instead of disk.

#     :param template:    path to docx file or file-like object
#     :param data:    dict with keys and values
#     """
#     doc = DocxTemplate(template)
#     doc.render(data)
#     _file = BytesIO()
#     doc.docx.save(_file)
#     return _file

# @frappe.whitelist()
# def fill_and_attach_template(doctype, name, template):
#     frappe.errprint("hi")
#     """
#     Use a documents data to fill a docx template and attach the result.

#     Reads a document and a template file, fills the template with data from the
#     document and attaches the resulting file to the document.

#     :param doctype"     data doctype
#     :param name"        data name
#     :param template"    name of the template file
#     """
#     data = frappe.get_doc(doctype, name)
#     data_dict = data.as_dict()

#     template_doc = frappe.get_doc("File", template)
#     template_path = template_doc.get_full_path()

#     output_file = _fill_template(template_path, data_dict)
#     output_doc = frappe.get_doc({
#         "doctype": "File",
#         "file_name": "-".join([name, template_doc.file_name]),
#         "attached_to_doctype": doctype,
#         "attached_to_name": name,
#         "content": output_file.getvalue(),
#     })
#     output_doc.save()

@frappe.whitelist()
def get_parent_territory(customer):
    territory = frappe.db.get_value("Customer", customer, "territory")
    return territory


def get_projects(doctype, txt, searchfield, start, page_len, filters):
    if not filters.get("customer"):
        frappe.throw(_("Please select Customer first."))

    project_list = frappe.db.sql(
        """select project.name from tabProject project where project.customer = %s order by creation desc""", (filters.get("customer")))
    return project_list


def get_tasks(doctype, txt, searchfield, start, page_len, filters):
    if not filters.get("project"):
        frappe.throw(_("Please select Project first."))

    task_list = frappe.db.sql(
        """select task.name,task.subject from tabTask task where task.project = %s order by creation desc""", (filters.get("project")))
    return task_list


def get_associates(doctype, txt, searchfield, start, page_len, filters):
    associate_list = frappe.db.sql(
        """select associate_name,name from tabAssociate order by associate_name asc""")
    return associate_list


def get_candidates(doctype, txt, searchfield, start, page_len, filters):
    if not filters.get("task"):
        frappe.throw(_("Please select Position first."))

    candidate_list = frappe.db.sql(
        """select candidate.name,candidate.given_name from tabCandidate candidate where candidate.task = %s order by creation desc""", (filters.get("task")))
    return candidate_list


@frappe.whitelist()
def make_candidate(source_name, target_doc=None, ignore_permissions=False):
    doclist = get_mapped_doc("Task", source_name, {
        "Task": {
            "doctype": "Candidate",
        },
        "Task Candidate": {
            "doctype": "Sales Invoice Candidate",
            "field_map": {
                "parent": "task"
            },
            "add_if_empty": True
        }

    }, target_doc, ignore_permissions=ignore_permissions)

    return doclist

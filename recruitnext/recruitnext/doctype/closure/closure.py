# -*- coding: utf-8 -*-
# Copyright (c) 2019, suganya and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.data import today
from frappe.model.document import Document


class Closure(Document):
    def validate(self):
        # self.tcrdetails()
        self.validate_psl()
        self.calculate_service_charge()

    def calculate_service_charge(self):
        if self.candidate_status == 'Dropped':
            self.dropped_date = today()
        # self.pending_payment = self.as_on_date_collection - self.collected

    def validate_psl(self):
        if self.candidate_status == 'Dropped':
            frappe.db.set_value("Candidate", self.candidate,
                                "pending_for", "IDB")
            self.status = 'Dropped'

        elif self.candidate_status == 'Waitlisted':
            self.status = 'Waitlisted'

        elif self.candidate_status == 'Selected':
            if self.territory == 'Sri Lanka':
                if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                    self.status = 'Onboarded'
                    self.status_updated_on = today()
                else:
                    self.status = 'Sales Order'
                    self.status_updated_on = today()

            elif self.territory == 'Abudhabi' or self.territory == 'UAE' or self.territory == 'Dubai' or self.territory == 'Nigeria':
                if self.irf and self.passport and self.photo:
                    if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                        if self.offer_letter:
                            if self.mol:
                                if self.visa:
                                    if self.final_medical:
                                        if self.stamped_visa:
                                            if self.slbfe:
                                                if self.payment_reciept:
                                                    if self.ticket:
                                                        if self.status == 'Onboarded':
                                                            self.status = 'Onboarded'
                                                            self.boarded_date = today()
                                                        else:
                                                            self.status = 'Onboarding'
                                                            self.status_updated_on = today()
                                                    else:
                                                        self.status = 'Ticket Details'
                                                        self.ticket_date = today()
                                                else:
                                                    self.status = 'Payment Receipt'
                                                    self.payment_receipt_date = today()
                                            else:
                                                self.status = 'slbfe'
                                                self.poe_date = today()
                                        else:
                                            self.status = 'Visa Stamping'
                                            self.stamped_visa_date = today()
                                    else:
                                        self.status = 'Final Medical'
                                        self.visa_date = today()
                                else:
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'MOL'
                                self.mol_date = today()
                        else:
                            self.status = 'Offer Letter'
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Sales Order'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.csl_status = 'Sales Order'
                    self.status_updated_on = today()

            elif self.territory == 'Malaysia':
                if self.irf and self.passport and self.photo:
                    if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                        if self.offer_letter:
                            if self.premedical:
                                # if self.mol:
                                    if self.visa:
                                        if self.slbfe:
                                            if self.payment_reciept:
                                                if self.ticket:
                                                    if self.status == 'Onboarded':
                                                        self.status = 'Onboarded'
                                                        self.boarded_date = today()
                                                    else:
                                                        self.status = 'Onboarding'
                                                        self.status_updated_on = today()
                                                else:
                                                    self.status = 'Ticket Details'
                                                    self.ticket_date = today()
                                            else:
                                                self.status = 'Payment Receipt'
                                                self.payment_receipt_date = today()
                                        else:
                                            self.status = 'slbfe'
                                            self.poe_date = today()
                                    else:
                                        self.status = 'Visa'
                                        self.visa_date = today()
                                # else:
                                #     self.status = 'MOL'
                                #     self.mol_date = today()
                            else:
                                self.status = 'Premedical'
                                self.premedical_date = today()
                        else:
                            self.status = 'Offer Letter'
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Sales Order'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.csl_status = 'Sales Order'
                    self.status_updated_on = today()

            elif self.territory == 'Dammam' or self.territory == 'Jeddah' or self.territory == 'Riyadh' or self.territory == 'Romania' or self.territory == 'Poland' or self.territory == 'Timor-Leste':
                if self.irf and self.passport and self.photo:
                    if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                        if self.offer_letter:
                            if self.visa:
                                if self.final_medical:
                                    if self.pcc:
                                        if self.stamped_visa:
                                            if self.slbfe:
                                                if self.payment_reciept:
                                                    if self.ticket:
                                                        if self.status == 'Onboarded':
                                                            self.status = 'Onboarded'
                                                            self.boarded_date = today()
                                                        else:
                                                            self.status = 'Onboarding'
                                                            self.status_updated_on = today()
                                                    else:
                                                        self.status = 'Ticket Details'
                                                        self.ticket_date = today()
                                                else:
                                                    self.status = 'Payment Receipt'
                                                    self.payment_receipt_date = today()
                                            else:
                                                self.status = 'slbfe'
                                                self.poe_date = today()
                                        else:
                                            self.status = 'Visa Stamping'
                                            self.stamped_visa_date = today()
                                    else:
                                    self.status = 'PCC'
                                    self.pcc_date = today()
                                else:
                                    self.status = 'Final Medical'
                                    self.final_medical_date = today()
                            else:
                                self.status = 'Visa'
                                self.visa_date = today()
                        else:
                            self.status = 'Offer Letter'
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Sales Order'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.csl_status = 'Sales Order'
                    self.status_updated_on = today()
            elif self.territory == 'Qatar':
                if self.irf and self.passport and self.photo:
                    if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                        if self.offer_letter:
                            if self.premedical:
                                if self.visa:
                                    if self.final_medical:
                                        if self.stamped_visa:
                                            if self.slbfe:
                                                if self.payment_reciept:
                                                    if self.ticket:
                                                        if self.status == 'Onboarded':
                                                            self.status = 'Onboarded'
                                                            self.boarded_date = today()
                                                        else:
                                                            self.status = 'Onboarding'
                                                            self.status_updated_on = today()
                                                    else:
                                                        self.status = 'Ticket Details'
                                                        self.ticket_date = today()
                                                else:
                                                    self.status = 'Payment Receipt'
                                                    self.payment_receipt_date = today()
                                            else:
                                                self.status = 'slbfe'
                                                self.poe_date = today()
                                        else:
                                            self.status = 'Visa Stamping'
                                            self.stamped_visa_date = today()
                                    else:
                                        self.status = 'Final Medical'
                                        self.final_medical_date = today()
                                else:
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Premedical'
                                self.premedical_date = today()
                        else:
                            self.status = 'Offer Letter'
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Sales Order'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.csl_status = 'Sales Order'
                    self.status_updated_on = today()

            elif self.territory == 'Oman' or self.territory == 'Maldives' or self.territory == 'Bahrain':
                if self.irf and self.passport and self.photo:
                    if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                        if self.offer_letter:
                            if self.premedical:
                                if self.stamped_visa:
                                    if self.slbfe:
                                        if self.payment_reciept:
                                            if self.ticket:
                                                if self.status == 'Onboarded':
                                                    self.status = 'Onboarded'
                                                    self.boarded_date = today()
                                                else:
                                                    self.status = 'Onboarding'
                                                    self.status_updated_on = today()
                                            else:
                                                self.status = 'Ticket Details'
                                                self.ticket_date = today()
                                        else:
                                            self.status = 'Payment Receipt'
                                            self.payment_receipt_date = today()
                                    else:
                                        self.status = 'slbfe'
                                        self.poe_date = today()
                                else:
                                    self.status = 'Visa'
                                    self.visa_date = today()
                            else:
                                self.status = 'Premedical'
                                self.premedical_date = today()
                        else:
                            self.status = 'Offer Letter'
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Sales Order'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.csl_status = 'Sales Order'
                    self.status_updated_on = today()

            elif self.territory == 'Kuwait' or self.territory == 'Singapore':
                if self.irf and self.passport and self.photo:
                    if self.csl_status == 'Sales Order Confirmed' or self.sales_order_confirmed_date:
                        if self.offer_letter:
                            if self.premedical:
                                if self.pcc:
                                    if self.visa:
                                        if self.final_medical:
                                            if self.stamped_visa:
                                                if self.slbfe:
                                                    if self.payment_reciept:
                                                        if self.ticket:
                                                            if self.status == 'Onboarded':
                                                                self.status = 'Onboarded'
                                                                self.boarded_date = today()
                                                            else:
                                                                self.status = 'Onboarding'
                                                                self.status_updated_on = today()
                                                        else:
                                                            self.status = 'Ticket Details'
                                                            self.ticket_date = today()
                                                    else:
                                                        self.status = 'Payment Receipt'
                                                        self.payment_receipt_date = today()
                                                else:
                                                    self.status = 'slbfe'
                                                    self.poe_date = today()
                                            else:
                                                self.status = 'Visa Stamping'
                                                self.stamped_visa_date = today()
                                        else:
                                            self.status = 'Final Medical'
                                            self.final_medical_date = today()
                                    else:
                                        self.status = 'Visa'
                                        self.visa_date = today()
                                else:
                                    self.status = 'PCC'
                                    self.pcc_date = today()
                            else:
                                self.status = 'Premedical'
                                self.premedical_date = today()
                        else:
                            self.status = 'Offer Letter'
                            self.offer_letter_date = today()
                    else:
                        self.status = 'Sales Order'
                        self.status_updated_on = today()
                else:
                    self.status = 'PSL'
                    self.csl_status = 'Sales Order'
                    self.status_updated_on = today()


@frappe.whitelist()
def get_dle(doctype, txt, searchfield, start, page_len, filters):
    if not filters.get("candidate"):
        frappe.throw(_("Please select candidate first."))

    dle = frappe.db.sql(
        """select candidate.user from tabCandidate candidate where candidate.name = %s""", (filters.get("candidate")))
#    dle_user = frappe.db.sql("""select employee.user_id from tabEmployee employee where employee.name=%s""",dle)
    return dle_user


def get_tl(doctype, txt, searchfield, start, page_len, filters):
    if not filters.get("dle"):
        frappe.throw(_("Please select Delivery Executive first."))

    tl = frappe.db.sql(
        """select employee.reports_to from tabEmployee employee where employee.user_id=%s""", (filters.get("dle")))
    tl_user = frappe.db.sql(
        """select employee.user_id from tabEmployee employee where employee.name=%s""", tl)
    return tl_user


@frappe.whitelist()
def update_dnd_incharge(project, dnd):
    if dnd:
        p = frappe.get_doc("Project", project)
        if not p.dnd_incharge:
            p.update({
                "dnd_incharge": dnd
            })
            p.save(ignore_permissions=True)
            frappe.db.commit()
            return True


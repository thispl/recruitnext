from __future__ import unicode_literals
import json
import calendar
import frappe
import socket
import os
import math
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils.data import today
from frappe.utils import time_diff_in_seconds, time_diff_in_hours, formatdate, add_months, cint, fmt_money, add_days
import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
import time
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee

@frappe.whitelist()
def task_alert(name):
    task=frappe.get_doc("Task",name)
    # frappe.errprint(can.name1)
    content="""<h4>Dear Sir,</h4><br>
    <p>Client Service Changed for %s<p><br>
    <p>You can see it by clicking <a href= "%s">Open Task</a></p>""" %(task.subject,frappe.utils.get_url_to_form("Task",name))
    frappe.sendmail(
        recipients=[
            'barathprathosh.m@voltechgroup.com',
            ],
        subject='Task Overdue Alert - ' +
        formatdate(today()),
        message=""" %s""" % (content))
    frappe.msgprint(content)

@frappe.whitelist()
def Candidate_overdue_alert(name):
    closure=frappe.get_doc("Closure",name)
    # frappe.errprint(can.name1)
    content="""<h4>Dear Sir,</h4><br>
    <p>Client Service Changed for %s<p><br>
    <p>You can see it by clicking <a href= "%s">Open Closure</a></p>""" %(closure.given_name__surname,frappe.utils.get_url_to_form("Closure",name))
    frappe.sendmail(
        recipients=[
            'barathprathosh.m@voltechgroup.com',
            ],
        subject='Candidate Overdue Alert - ' +
        formatdate(today()),
        message=""" %s""" % (content))
    frappe.msgprint(content)
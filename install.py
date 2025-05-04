import frappe

def before_install():
    if not frappe.db.exists("Print Format", "Iraqi Payroll Slip"):
        frappe.get_doc({
            "doctype": "Print Format",
            "name": "Iraqi Payroll Slip",
            "doc_type": "Salary Slip",
            "print_format_type": "Jinja",
            "custom_format": 1,
            "html": """
<div style="text-align: center;">
    <h2>دائرة الإصلاح العراقية</h2>
    <h3>قسم الشؤون الإدارية والمالية</h3>
    <h4>كشف الرواتب لشهر {{ doc.month }} {{ doc.fiscal_year }}</h4>
</div>
<table style="width: 100%; border-collapse: collapse;" border="1">
    <thead>
        <tr>
            <th>ت</th>
            <th>اسم الموظف</th>
            {% if doc.show_employee_details %}
            <th>العنوان الوظيفي</th>
            <th>التحصيل الدراسي</th>
            {% endif %}
            <th>الراتب الاسمي</th>
            {% if doc.show_allowances %}
            <th>المخصصات</th>
            {% endif %}
            {% if doc.show_deductions %}
            <th>الاستقطاعات</th>
            {% endif %}
            <th>الصافي</th>
            {% if doc.show_signature %}
            <th>التوقيع</th>
            {% endif %}
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>{{ doc.employee_name }}</td>
            {% if doc.show_employee_details %}
            <td>{{ doc.designation }}</td>
            <td>{{ doc.educational_qualification or "" }}</td>
            {% endif %}
            <td>{{ frappe.utils.fmt_money(doc.base, currency=doc.currency) }}</td>
            {% if doc.show_allowances %}
            <td>
                {% for e in doc.earnings %}
                    {{ e.salary_component }}: {{ frappe.utils.fmt_money(e.amount, currency=doc.currency) }}<br>
                {% endfor %}
            </td>
            {% endif %}
            {% if doc.show_deductions %}
            <td>
                {% for d in doc.deductions %}
                    {{ d.deduction_type }}: {{ frappe.utils.fmt_money(d.amount, currency=doc.currency) }}<br>
                {% endfor %}
            </td>
            {% endif %}
            <td>{{ frappe.utils.fmt_money(doc.net_pay, currency=doc.currency) }}</td>
            {% if doc.show_signature %}
            <td>_____________</td>
            {% endif %}
        </tr>
    </tbody>
</table>
{% if doc.show_remarks %}
<div style="margin-top: 30px;">
    <strong>ملاحظات:</strong> {{ doc.remarks or "" }}
</div>
{% endif %}
<div style="margin-top: 50px; text-align: right;">
    <p>مدير الشؤون الإدارية والمالية</p>
</div>
"""
        }).insert(ignore_permissions=True)

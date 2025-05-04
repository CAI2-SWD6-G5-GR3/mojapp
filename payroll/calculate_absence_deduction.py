import frappe

def calculate_absence_deduction(doc, method):
    # Extract basic salary (الراتب الاسمي) from earnings
    basic = 0
    for row in doc.earnings:
        if row.salary_component == "الراتب الاسمي":
            basic = row.amount
            break

    if not basic:
        frappe.msgprint("⚠️ Could not find 'الراتب الاسمي' in earnings.")
        return

    # Count absent days from Attendance records
    total_absent_days = frappe.db.count('Attendance', {
        'employee': doc.employee,
        'status': 'Absent',
        'attendance_date': ['between', [doc.start_date, doc.end_date]]
    })

    if total_absent_days == 0:
        return  # No absences to deduct

    # Calculate absence deduction
    daily_rate = basic / 30
    absence_deduction = daily_rate * total_absent_days

    # Append deduction to Salary Slip
    doc.append("deductions", {
        "deduction_type": "استقطاع غيابات",
        "amount": absence_deduction
    })
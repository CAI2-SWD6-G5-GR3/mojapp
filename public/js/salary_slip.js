frappe.ui.form.on('Salary Slip', {
    validate: function(frm) {
        console.log("🟢 Salary Slip validation triggered!");

        // 1. Get "الراتب الاسمي"
        let basic = 0;
        frm.doc.earnings.forEach(row => {
            if (row.salary_component === "الراتب الاسمي") {
                basic = row.amount;
            }
        });

        if (!basic) {
            frappe.msgprint("⚠️ الراتب الاسمي غير موجود!");
            return;
        }

        // 2. Calculate values
        let pension_deduction = basic * 0.15;
        let income_tax = 0;

        if (basic <= 500000) {
            income_tax = 0;
        } else if (basic <= 1000000) {
            income_tax = (basic - 500000) * 0.03;
        } else if (basic <= 2000000) {
            income_tax = 15000 + (basic - 1000000) * 0.05;
        } else {
            income_tax = 65000 + (basic - 2000000) * 0.10;
        }

        // 3. Clear & add to deductions properly
        frm.clear_table("deductions");

        let row1 = frm.add_child("deductions");
        row1.salary_component = "استقطاع التقاعد";
        row1.amount = pension_deduction;

        let row2 = frm.add_child("deductions");
        row2.salary_component = "ضريبة الدخل";
        row2.amount = income_tax;

        // 4. Refresh field
        frm.refresh_field("deductions");
    }
});

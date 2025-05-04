frappe.ui.form.on('Salary Structure Assignment', {
  employee: function(frm) {
    set_base_from_grade_level(frm);
  },
  grade: function(frm) {
    set_base_from_grade_level(frm);
  },
  custom_grade_level: function(frm) {
    set_base_from_grade_level(frm);
  }
});

function set_base_from_grade_level(frm) {
  if (frm.doc.grade && frm.doc.custom_grade_level) {
    frappe.call({
      method: 'frappe.client.get',
      args: {
        doctype: 'Employee Grade',
        name: frm.doc.grade
      },
      callback: function(r) {
        if (r.message && r.message.custom_grade_levels) {
          let matched_level = r.message.custom_grade_levels.find(row => row.level_name === frm.doc.custom_grade_level);
          
          if (matched_level && matched_level.base_pay) {
            frm.set_value('base', matched_level.base_pay);
          } else {
            frm.set_value('base', 0); // لو مفيش level أو مفيش base_pay
          }
        } else {
          frm.set_value('base', 0); // لو مفيش بيانات أساسًا
        }
      },
      error: function() {
        frm.set_value('base', 0); // لو حصل Error في الاتصال
      }
    });
  } else {
    frm.set_value('base', 0); // لو مش موجودين grade أو level
  }
}


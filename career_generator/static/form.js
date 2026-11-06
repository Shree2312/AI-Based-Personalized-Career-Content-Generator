// form.js – Fill Sample Data button logic (plain JavaScript only)

// Fill all profile form fields with a realistic student example
function fillSampleData() {
  // Fill the text input fields by their element id
  document.getElementById('name-input').value      = "Riya Mehta";
  document.getElementById('education-input').value = "B.Tech Computer Science, 3rd Year";
  document.getElementById('skills-input').value    = "python, sql, git, html, css";

  // Untick ALL interest checkboxes first to start clean
  document.querySelectorAll('.interest-cb').forEach(function(cb) {
    cb.checked = false;
  });

  // Tick exactly 3 sample interests by matching their value attribute
  var sampleInterests = ["web development", "backend systems", "databases"];
  sampleInterests.forEach(function(val) {
    var cb = document.querySelector('.interest-cb[value="' + val + '"]');
    if (cb) cb.checked = true;  // Only tick if the checkbox actually exists on the page
  });

  // Set the career goal dropdown to "Crack campus placements"
  var goalSelect = document.getElementById('career-goal-select');
  for (var i = 0; i < goalSelect.options.length; i++) {
    if (goalSelect.options[i].value === "Crack campus placements") {
      goalSelect.selectedIndex = i;
      break;
    }
  }

  // Set the role dropdown to "Python Developer"
  var roleSelect = document.getElementById('role-select');
  for (var i = 0; i < roleSelect.options.length; i++) {
    if (roleSelect.options[i].value === "Python Developer") {
      roleSelect.selectedIndex = i;
      break;
    }
  }
}

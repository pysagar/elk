var file = document.getElementById('file');
var projects = document.getElementById('projects');
var log_type = document.getElementById('log_type');
var submit = document.getElementById('submit');

var validateFile = function() {
  var ext = file.files[0].name.match('log');
  if (!ext) {
    alert('Please select log file.')
    file.value = '';
  }
}

$('#myModal').on('hide.bs.modal', function (e) {
  file.value = '';
  projects.value = '';
  log_type.value = '';
})

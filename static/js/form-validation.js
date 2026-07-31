// Kipsolu Central FC - vanilla JS Bootstrap-style validation feedback for the contact form
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('kc-contact-form');
  if (!form) return;

  form.addEventListener('submit', function (event) {
    var isValid = true;

    var name = form.querySelector('#id_name');
    var email = form.querySelector('#id_email');
    var subject = form.querySelector('#id_subject');
    var message = form.querySelector('#id_message');

    [name, email, subject, message].forEach(function (field) {
      if (field && field.value.trim() === '') {
        field.classList.add('is-invalid');
        isValid = false;
      } else if (field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
      }
    });

    if (email && email.value.trim() !== '') {
      var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(email.value.trim())) {
        email.classList.add('is-invalid');
        email.classList.remove('is-valid');
        isValid = false;
      }
    }

    if (message && message.value.trim().length > 0 && message.value.trim().length < 10) {
      message.classList.add('is-invalid');
      message.classList.remove('is-valid');
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault();
      event.stopPropagation();
    }

    form.classList.add('was-validated');
  }, false);

  form.querySelectorAll('input, textarea').forEach(function (field) {
    field.addEventListener('input', function () {
      if (field.value.trim() !== '') {
        field.classList.remove('is-invalid');
      }
    });
  });
});

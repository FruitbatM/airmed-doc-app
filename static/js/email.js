// Send email function
function sendMail(contactForm) {
    emailjs.send('airmed', 'template_g28czrg', {
      'from_name': contactForm.fullname.value,
      'from_email': contactForm.email.value,
      'subject': contactForm.subject.value,
      'message': contactForm.message.value
    })
    
      .then(
        // Sweet Alert custom pop-up alert if success; credit: https://sweetalert2.github.io/
        function() {
          Swal.fire ({
            title: 'Thank you for getting in touch!',
            text: 'We will get back to you shortly.',
            icon: 'success',
            confirmButtonColor: '#F68C48'
          });
        },
        // Sweet Alert custom pop-up alert if fail
        function() {
          Swal.fire ({
            title: 'Ooops...',
            text: 'Something went wrong.',
            icon: 'error',
            confirmButtonColor: '#F68C48'
          });
        });
  
      // Clear the form
      document.getElementById('contactForm').reset();
      return false;
  }
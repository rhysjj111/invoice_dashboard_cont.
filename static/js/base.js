const currentUrl = window.location.href;
//initialize toasts

document.addEventListener('DOMContentLoaded', function() {

  // Initialize toasts
  const toastElList = document.querySelectorAll('.toast-message');
  const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, { autohide: true, delay: 10000 })); // Set delay to 5000 milliseconds (5 seconds)

  // Display toasts
  toastList.forEach(toast => toast.show());
  

});

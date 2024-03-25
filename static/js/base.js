// function to debounce search filter 
function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        let context = this, args = arguments;
        let later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        let callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
        };
};

// search filter function 
$(document).ready(function () {
    $("#search-bar").keyup(debounce(function() {
        let value = $(this).val().toLowerCase();
        $("#table-body tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    }, 300)); 
});


const originalVehicleOptions = document.getElementById('id_vehicle').innerHTML;

/**
* Update the vehicle select options when a user is creating an invoice
* so that only options are shown corresponding to a valid customer.
*/
function updateVehicles() {
    let selectedCustomer = document.getElementById('id_customer').value;
    let vehicleOptions = document.querySelectorAll('#id_vehicle option');

    document.getElementById('id_vehicle').innerHTML = originalVehicleOptions
    vehicleOptions = document.querySelectorAll('#id_vehicle option');
    vehicleOptions.forEach(function(option) {
      if (option.className === selectedCustomer || option.className === 'no_customer') {
        option.style.display = 'block';
        found = true;
      } else {
        option.style.display = 'none';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    updateVehicles();
  });
  document.getElementById('id_customer').addEventListener('change', updateVehicles);


const originalVehicleOptions = document.getElementById('id_vehicle').innerHTML;

/**
* Update the vehicle select options when a user is creating an invoice
* so that only options are shown corresponding to a valid customer.
*/
function updateVehicles() {
    let selectedCustomer = document.getElementById('id_customer').value;
    let vehicleOptions = document.querySelectorAll('#id_vehicle option');

    // reset vehicle options 
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

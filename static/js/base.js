const currentUrl = window.location.href;

document.addEventListener('DOMContentLoaded', function() {
  
  if (currentUrl.includes("invoice_select")){
    hideLastDeleteInput('parts')
    hideLastDeleteInput('labour')
  }
  
  if (currentUrl.includes('invoice')) {
    updateVehicles();
    document.getElementById('id_customer').addEventListener('change', updateVehicles);
  }
  
});


/*
* Function to hide the delete input of one 'extra' form of a
* formset. The function gets value of the total number of
* forms from the formset manager information and then constructs
* the id of the 'extra' form (it will have the highest 'number').
* Finally the display of the delete unput is set to none.
* The parameter target should be the form name.
*/
function hideLastDeleteInput(target) {
  let totalFormsInput = document.getElementById('id_' + target + '-TOTAL_FORMS');
  let totalForms = parseInt(totalFormsInput.value);
  let lastDeleteInputId = '#div_id_' + target + '-' + (totalForms - 1) + '-DELETE';
  let lastDeleteInput = document.querySelector(lastDeleteInputId);
  if (lastDeleteInput) {
    lastDeleteInput.style.display = 'none';
  }
}


let originalVehicleSelectInput = document.getElementById('id_vehicle');
/*
* Update the vehicle select options when a user is creating an invoice
* so that only options are shown corresponding to a valid customer.
* The selected customer id value is fetched. A list of the vehicles
* is also fetched. The options are reset incase more than one customer
* is selected in the same session. The vehicle options are looped through
* and removed if their class does not match with the value of the selected
* customer.
*/
function updateVehicles() {
  let selectedCustomer = document.getElementById('id_customer').value;
  let vehicleOptions = document.querySelectorAll('#id_vehicle option'); 
  // resets vehicle options
  document.getElementById('id_vehicle').innerHTML = originalVehicleSelectInput.innerHTML;
  vehicleOptions = document.querySelectorAll('#id_vehicle option');
  // loop through vehicle options and hide/show depending on customer selected
  vehicleOptions.forEach(function(option) {
      if (option.className === selectedCustomer || option.className === 'no_customer') {
        option.style.display = 'block';
      } else {
        option.style.display = 'none';
      }
    });
  }


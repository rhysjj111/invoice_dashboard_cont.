document.addEventListener('DOMContentLoaded', function() { 

    // copy invoice descriptions to clipboard 
    document.querySelectorAll('.content-to-copy').forEach(function(div) {
      div.addEventListener('click', function() {
        // Get the content of the clicked div
        let contentToCopy = this.innerText;
  
        // Use the Clipboard API to copy the content
        navigator.clipboard.writeText(contentToCopy)
          .then(function() {
            // Show the toast
            let copiedToast = new bootstrap.Toast(document.getElementById('copied-toast'));
            copiedToast.show();
          })
          .catch(function(err) {
            console.error('Failed to copy: ', err);
          });
      });
    });

    // triggers if user on invoice summary page
    let saveButton = document.getElementById('save-button')
    if (saveButton){
        hideLastDeleteInput('parts');
        hideLastDeleteInput('labour');
        formSaveReminder();    
    }

    // triggers if user on invoice list page 
    let vehicleSelect = document.getElementById('id_vehicle')
    if(vehicleSelect){
        updateVehicles();
        document.getElementById('id_customer').addEventListener('change', function(){
        updateVehicles();
        resetVehicleSelect()
    }); 
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
let vehicleSelect = document.getElementById('id_vehicle');
let selectedCustomer = document.getElementById('id_customer').value;
let vehicleOptions = document.querySelectorAll('#id_vehicle option'); 
// resets vehicle options
vehicleSelect.innerHTML = originalVehicleSelectInput.innerHTML;
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

function formSaveReminder(){
let elements = document.querySelectorAll('input, select');
let invoiceForm = document.getElementById('invoice-form');
// loop over all input and select inputs  and add change event listener
elements.forEach(element => {
    element.addEventListener("change", () => {
    // Add warning border around invoice form if change detected 
    setTimeout(() => {
        invoiceForm.classList.add("highlight");
    }, 8000);
    });
});
}

function resetVehicleSelect(){
// resets vehicle selected option
let vehicleSelect = document.getElementById('id_vehicle');
vehicleSelect.selectedIndex = 0;
}
initialize();

async function initialize() {
  console.log('TEST')
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const sessionId = urlParams.get('session_id');
  let session_status_url = document.getElementById('session_status_url').innerText.replace(/["']/g, '');
  const response = await fetch(`${session_status_url}?session_id=${sessionId}`);
  console.log(response)
  const session = await response.json();
  console.log(session)

  if (session.status == 'open') {
    let checkout_url = document.getElementById('checkout_url').innerText.replace(/["']/g, '')
    window.location.replace(checkout_url)
  } else if (session.status == 'complete') {
    document.getElementById('success').classList.remove('hidden');
    document.getElementById('customer-email').textContent = session.customer_email
  }
}
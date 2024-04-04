// This is your test publishable API key.
const stripe = Stripe("pk_test_51P1ZRPRs8wZfo3OzGYtCkQSPVyRRCXfrj22W5iQYc5sZpUS9ibvG40zaDCq9NoXKIrMdiYTihUb9FkHZIQ9jPKBw00hPKe1VAx");

initialize();

// Create a Checkout Session
async function initialize() {
  const fetchClientSecret = async () => {
    let checkout_url = document.getElementById('checkout_url').innerText.replace(/["']/g, '');
    const response = await fetch(checkout_url, {
      method: "POST",
    });
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
  console.log('fin')
}
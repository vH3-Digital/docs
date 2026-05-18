(function () {
  if (document.querySelector('script[src*="stripe.com/v3/pricing-table"]')) return;
  var s = document.createElement('script');
  s.src = 'https://js.stripe.com/v3/pricing-table.js';
  s.async = true;
  document.head.appendChild(s);
})();

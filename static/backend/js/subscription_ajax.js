// Get Stripe publishable key
fetch("/config/")
  .then((result) => result.json())
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    var yearly_plan = 'no';

//    const basic_monthly = document.querySelector('.basic_monthly');
//    const premium_monthly = document.querySelector('.premium_monthly');
    const unlimited_monthly = document.querySelector('.unlimited_monthly');
    const pricing_duration = document.querySelectorAll('.pricing-duration');

    // check for yearly checkbox
//    var checkbox = document.getElementById('yearly_subscription');
//        checkbox.addEventListener('change', function () {
//            if (checkbox.checked) {
//                yearly_plan = 'yes';
////                basic_monthly.textContent = '490'
////                premium_monthly.textContent = '990'
//                unlimited_monthly.textContent = '2490'
//                pricing_duration.forEach(function(duration) {
//                        duration.textContent = '/Year'; // Change to your desired text
//                    });
//            } else {
//                yearly_plan = 'no';
////                basic_monthly.textContent = '49'
////                premium_monthly.textContent = '99'
//                unlimited_monthly.textContent = '249'
//                pricing_duration.forEach(function(duration) {
//                        duration.textContent = '/Month'; // Change to your desired text
//                    });
//
//            }
//        });

document.addEventListener('DOMContentLoaded', function() {
    var checkbox = document.getElementById('yearly_subscription');
    if (checkbox) {
        checkbox.addEventListener('change', function () {
            if (checkbox.checked) {
                yearly_plan = 'yes';
                unlimited_monthly.textContent = '2490';
                pricing_duration.forEach(function(duration) {
                    duration.textContent = '/Year'; // Change to your desired text
                });
            } else {
                yearly_plan = 'no';
                unlimited_monthly.textContent = '20';
                pricing_duration.forEach(function(duration) {
                    duration.textContent = '/Month'; // Change to your desired text
                });
            }
        });
    }
});

    let Submit_Btn1 = document.querySelector("#SubscriptionBtn1");
    let Submit_Btn2 = document.querySelector("#SubscriptionBtn2");
    let Submit_Btn3 = document.querySelector("#SubscriptionBtn3");

    // Event Handler basic_monthly_subscription
    if (Submit_Btn1 != null) {
      Submit_Btn1.addEventListener("click", () => {
        $("#SubscriptionBtn1").attr('disabled', true);
        $("#SubscriptionBtn2").attr('disabled', true);
        $("#SubscriptionBtn3").attr('disabled', true);
        // Get Checkout Session ID
        fetch("/create-checkout-session/basic_monthly_subscription/"+yearly_plan)
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            console.log(data);

            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .catch((res) => {
            console.log(res);
          });
      });
    }

    // Event Handler premium_monthly_subscription
    if (Submit_Btn2 != null) {
      Submit_Btn2.addEventListener("click", () => {
        $("#SubscriptionBtn1").attr('disabled', true);
        $("#SubscriptionBtn2").attr('disabled', true);
        $("#SubscriptionBtn3").attr('disabled', true);
        // Get Checkout Session ID
        fetch("/create-checkout-session/premium_monthly_subscription/"+yearly_plan)
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            console.log(data);

            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .catch((res) => {
            console.log(res);
          });
      });
    }

    // Event Handler unlimited_monthly_subscription
    if (Submit_Btn3 != null) {
      Submit_Btn3.addEventListener("click", () => {
        $("#SubscriptionBtn1").attr('disabled', true);
        $("#SubscriptionBtn2").attr('disabled', true);
        $("#SubscriptionBtn3").attr('disabled', true);
        // Get Checkout Session ID
        fetch("/create-checkout-session/unlimited_monthly_subscription/"+yearly_plan)
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            console.log(data);

            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .catch((res) => {

            console.log(res);
          });
      });
    }

  });
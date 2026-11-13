(function () {
  // ===== Edit questions and answers here (updates on all pages) =====
  var heading = "Fees & EMI: Your Questions Answered";
  var subheading = "Everything you need to know about paying your course fee in installments.";

  var faqs = [
    {
      q: "Is EMI available for Rohil NextGen courses?",
      a: "Yes, you can pay your course fee in monthly installments. Our admission team will help you choose a plan that fits your budget."
    },
    {
      q: "Which courses can I join with EMI?",
      a: "EMI is available for our course programs. Please confirm the course you want with our admission team, as plans may differ by course."
    },
    {
      q: "How many months can I pay in?",
      a: "Flexible repayment periods are available. Contact us to know the options for your course."
    },
    {
      q: "Do I need to pay anything at the time of joining?",
      a: "An initial payment confirms your seat in the batch. The exact amount is shared by our admission team when you enquire."
    },
    {
      q: "What documents are required?",
      a: "Our team will tell you the exact documents when you enquire. Please keep a valid ID proof and your contact details ready."
    },
    {
      q: "How do I apply for EMI?",
      a: 'Call us at <a href="tel:+919751867879">+91 97518 67879</a> or <a href="contact.html">send an enquiry</a>. We will guide you through the process.'
    }
  ];
  // ==================================================================

  function addEmiFaq() {
    if (document.querySelector(".emi-faq")) return;

    var target =
      document.querySelector(".newsletter-section") ||
      document.querySelector(".tech-footer");
    if (!target) {
      console.warn("EMI FAQ: footer/newsletter not found on this page");
      return;
    }

    var css =
      ".emi-faq{background:#f5f5f5;padding:65px 20px}" +
      ".emi-faq-inner{max-width:820px;margin:0 auto}" +
      ".emi-faq-head{text-align:center;margin-bottom:32px}" +
      ".emi-faq-head h2{margin:0 0 10px;font-size:2rem;color:#333;font-family:Georgia}" +
      ".emi-faq-head p{margin:0;color:#666;font-size:1.05rem;font-family:Georgia}" +
      ".emi-faq details{background:#fff;border-radius:10px;box-shadow:0 3px 12px rgba(0,0,0,.08);margin-bottom:12px;padding:0 22px;border-left:4px solid transparent;transition:border-color .3s}" +
      ".emi-faq details[open]{border-left-color:#d40404}" +
      ".emi-faq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:14px;padding:18px 0;font-size:1.05rem;font-weight:600;color:#333;font-family:Georgia}" +
      ".emi-faq summary::-webkit-details-marker{display:none}" +
      ".emi-faq summary::after{content:'+';font-size:1.6rem;line-height:1;color:#d40404;flex:0 0 auto}" +
      ".emi-faq details[open] summary::after{content:'\\2212'}" +
      ".emi-faq summary:hover{color:#d40404}" +
      ".emi-faq details p{margin:0;padding:0 0 18px;color:#666;line-height:1.7;font-family:Georgia}" +
      ".emi-faq details p a{color:#d40404;font-weight:600}" +
      ".emi-faq + .newsletter-section{margin-top:0}" +
      "@media(max-width:768px){.emi-faq{padding:45px 15px}.emi-faq-head h2{font-size:1.5rem}.emi-faq summary{font-size:1rem}}";

    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var items = faqs
      .map(function (f) {
        return "<details><summary>" + f.q + "</summary><p>" + f.a + "</p></details>";
      })
      .join("");

    var section = document.createElement("section");
    section.className = "emi-faq";
    section.innerHTML =
      '<div class="emi-faq-inner">' +
        '<div class="emi-faq-head"><h2>' + heading + "</h2><p>" + subheading + "</p></div>" +
        items +
      "</div>";

    target.parentNode.insertBefore(section, target);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addEmiFaq);
  } else {
    addEmiFaq();
  }
})();
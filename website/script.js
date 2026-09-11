(function () {
  const toggle = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');

  function closeMenu() {
    if (!toggle || !links) return;
    links.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
  }

  if (toggle && links) {
    toggle.addEventListener('click', function () {
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });
    links.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMenu();
    });
  }

  const form = document.querySelector('#inquiry-form');
  if (!form) return;

  const params = new URLSearchParams(window.location.search);
  const typeField = form.elements.inquiryType;
  const sourceField = form.elements.source;
  const pocFields = document.querySelector('#poc-fields');
  const pocType = 'Apply for LATCHES POC Site Partnership';
  const allowedTypes = Array.from(typeField.options).map(function (option) {
    return option.value;
  });
  const requestedType = params.get('type');

  typeField.value = requestedType && allowedTypes.includes(requestedType)
    ? requestedType
    : 'General Inquiry';
  sourceField.value = params.get('source') || 'Contact Us';

  function updatePocFields() {
    pocFields.hidden = typeField.value !== pocType;
  }

  typeField.addEventListener('change', updatePocFields);
  updatePocFields();

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const status = document.querySelector('#form-error');
    if (!form.checkValidity()) {
      status.textContent = 'Please complete the required fields before submitting.';
      form.reportValidity();
      return;
    }
    status.textContent = 'Preview only: no information was sent or stored. Your entries remain on this page for review.';
    status.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}());

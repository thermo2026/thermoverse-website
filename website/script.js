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
    document.addEventListener('click', function (event) {
      if (links.classList.contains('open') && !links.contains(event.target) && !toggle.contains(event.target)) {
        closeMenu();
      }
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
    const isZh = form.elements.language?.value === 'zh' || document.documentElement.lang.startsWith('zh');
    if (!form.checkValidity()) {
      status.textContent = isZh
        ? '請填妥所有必填欄位後再送出。'
        : 'Please complete the required fields before submitting.';
      form.reportValidity();
      return;
    }
    status.textContent = isZh
      ? '展示預覽模式：目前表單處於展示階段，尚未實際送出或儲存資料。您的輸入內容已保留於本頁以供檢視。'
      : 'Preview only: no information was sent or stored. Your entries remain on this page for review.';
    status.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}());

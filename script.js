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

  function ensureContactModal() {
    if (document.querySelector('#inquiry-form')) return;
    const zh = document.documentElement.lang.startsWith('zh');
    const modal = document.createElement('div');
    modal.id = 'contact-modal';
    modal.className = 'contact-modal';
    modal.hidden = true;
    modal.innerHTML = `<div class="contact-backdrop" data-contact-close></div><section class="contact-dialog" role="dialog" aria-modal="true" aria-labelledby="contact-title"><button class="contact-close" type="button" aria-label="${zh ? '關閉聯絡表單' : 'Close contact form'}" data-contact-close>&times;</button><div class="eyebrow">${zh ? '與我們聯絡' : 'Connect with us'}</div><h2 id="contact-title">${zh ? '告訴我們您的專案需求' : 'Tell us about your project'}</h2><p class="contact-lead">${zh ? '請留下基本資料與需求，我們會盡快回覆您。' : 'Share a little context and our team will get back to you shortly.'}</p><form class="contact-modal-form" id="inquiry-form" novalidate><div class="contact-fields-two"><div class="field"><label for="modal-first-name">${zh ? '名字' : 'First name'} <span class="required">*</span></label><input id="modal-first-name" name="firstName" autocomplete="given-name" required placeholder="${zh ? '您的名字' : 'Your first name'}"></div><div class="field"><label for="modal-last-name">${zh ? '姓氏' : 'Last name'} <span class="required">*</span></label><input id="modal-last-name" name="lastName" autocomplete="family-name" required placeholder="${zh ? '您的姓氏' : 'Your last name'}"></div></div><div class="contact-fields-two"><div class="field"><label for="modal-email">${zh ? '企業郵箱' : 'Work email'} <span class="required">*</span></label><input id="modal-email" name="email" type="email" autocomplete="email" required placeholder="${zh ? '您的郵箱地址' : 'you@company.com'}"></div><div class="field"><label for="modal-organization">${zh ? '公司名稱' : 'Company' } <span class="required">*</span></label><input id="modal-organization" name="organization" autocomplete="organization" required placeholder="${zh ? '您的公司' : 'Your company'}"></div></div><div class="contact-fields-two"><div class="field"><label for="modal-role">${zh ? '職稱' : 'Role / title'}</label><input id="modal-role" name="role" autocomplete="organization-title" placeholder="${zh ? '您的職稱' : 'Your role'}"></div><div class="field"><label for="modal-location">${zh ? '國家／地區' : 'Country / region'}</label><input id="modal-location" name="location" autocomplete="country-name" placeholder="${zh ? '國家／地區' : 'Country / region'}"></div></div><div class="field"><label for="modal-inquiry-type">${zh ? '諮詢主題' : 'What can we help with?'} <span class="required">*</span></label><select id="modal-inquiry-type" name="inquiryType" required><option value="">${zh ? '請選擇' : 'Select one'}</option><option value="Schedule an Energy Assessment (Services) (New)">${zh ? '建築能源服務' : 'Energy Services'}</option><option value="Apply for LATCHES POC Site Partnership">${zh ? 'LATCHES™ POC 場域合作' : 'LATCHES™ POC partnership'}</option><option value="Technology / Engineering Inquiry">${zh ? '技術／工程諮詢' : 'Technology / engineering'}</option><option value="FACES Workforce Program Interest">${zh ? 'FACES 人才培訓計畫' : 'FACES workforce program'}</option><option value="General Inquiry">${zh ? '一般諮詢' : 'General inquiry'}</option></select></div><div class="field"><label for="modal-message">${zh ? '需求說明' : 'Project details'} <span class="required">*</span></label><textarea id="modal-message" name="message" required placeholder="${zh ? '請描述您的需求…' : 'Tell us what you need…'}"></textarea></div><fieldset id="poc-fields" class="poc-fields" hidden><legend>${zh ? 'LATCHES™ POC 場域資訊' : 'LATCHES™ POC site context'}</legend><div class="field"><label for="modal-site-type">${zh ? '場域類型' : 'Site type'}</label><input id="modal-site-type" name="siteType"></div><div class="field"><label for="modal-site-description">${zh ? '建築或設施描述' : 'Building or facility description'}</label><textarea id="modal-site-description" name="siteDescription"></textarea></div><div class="field"><label for="modal-data">${zh ? '可提供的能源資料' : 'Available energy data'}</label><textarea id="modal-data" name="dataAvailable"></textarea></div><div class="field"><label for="modal-contact-time">${zh ? '方便聯絡時段' : 'Preferred contact time'}</label><input id="modal-contact-time" name="contactTime"></div></fieldset><input type="hidden" name="source" value="Contact module"><input type="hidden" name="language" value="${zh ? 'zh' : 'en'}"><input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="field checkbox-field"><label><input type="checkbox" name="marketing"> <span>${zh ? '我想不定期接收 ThermoVerse 最新消息。' : 'I would like to receive occasional ThermoVerse updates.'}</span></label></div><p class="contact-privacy">${zh ? '送出即表示您同意我們的 <a href="privacy.html" target="_blank" rel="noopener noreferrer">隱私權政策</a>。我們會使用您提供的資料回覆這次諮詢。' : 'By submitting, you agree to our <a href="privacy.html" target="_blank" rel="noopener noreferrer">Privacy Policy</a>. We use the information you provide to respond to this inquiry.'}</p><button class="contact-submit" type="submit">${zh ? '送出' : 'Submit'}</button><p class="form-status" id="form-error" role="status" aria-live="polite"></p></form></section>`;
    document.body.appendChild(modal);
  }

  ensureContactModal();
  const form = document.querySelector('#inquiry-form');
  const modal = document.querySelector('#contact-modal');
  const openTriggers = document.querySelectorAll('a[href*="contact.html"], [data-contact-open]');
  let lastTrigger = null;
  function closeContact() {
    if (!modal) return;
    modal.hidden = true;
    document.body.classList.remove('contact-modal-open');
    if (lastTrigger) lastTrigger.focus();
  }
  function openContact(trigger) {
    if (!modal) return;
    lastTrigger = trigger;
    const href = trigger && trigger.getAttribute('href');
    if (href) {
      const query = href.includes('?') ? new URL(href, window.location.href).searchParams : null;
      const requested = query && query.get('type');
      if (requested && form.elements.inquiryType) form.elements.inquiryType.value = requested;
      if (query && query.get('source')) form.elements.source.value = query.get('source');
    }
    modal.hidden = false;
    document.body.classList.add('contact-modal-open');
    const first = modal.querySelector('input');
    if (first) first.focus();
    updatePocFields();
  }
  openTriggers.forEach(function (trigger) {
    trigger.addEventListener('click', function (event) {
      event.preventDefault();
      openContact(trigger);
    });
  });
  if (modal) {
    modal.querySelectorAll('[data-contact-close]').forEach(function (button) { button.addEventListener('click', closeContact); });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape' && !modal.hidden) closeContact(); });
  }
  if (modal && new URLSearchParams(window.location.search).get('openContact') === '1') {
    openContact({ getAttribute: function () { return window.location.href; } });
  }
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
    function setStatus(message, type) {
      if (!status) return;
      status.textContent = message;
      status.className = 'form-status' + (type ? ' status-' + type : '');
    }
    if (!form.checkValidity()) {
      setStatus(
        isZh ? '請填妥所有必填欄位後再送出。' : 'Please complete the required fields before submitting.',
        'error'
      );
      form.reportValidity();
      return;
    }
    const submit = form.querySelector('[type="submit"]');
    const payload = Object.fromEntries(new FormData(form).entries());
    if (payload.firstName || payload.lastName) {
      payload.name = [payload.firstName, payload.lastName].filter(Boolean).join(' ');
    }
    payload.marketing = form.elements.marketing.checked;
    const configuredBase = window.THERMO_API_BASE_URL || 'https://yyuah016q3.execute-api.ap-southeast-2.amazonaws.com';
    submit.disabled = true;
    setStatus(isZh ? '正在送出諮詢內容…' : 'Sending your inquiry…', 'pending');
    fetch(configuredBase + '/api/inquiries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(async function (response) {
      const result = await response.json().catch(function () { return {}; });
      if (!response.ok) throw new Error(result.error || 'Unable to send the inquiry.');
      form.reset();
      typeField.value = 'General Inquiry';
      updatePocFields();
      setStatus(
        isZh ? '謝謝，已收到您的諮詢內容。' : 'Thank you. Your inquiry has been received.',
        'success'
      );
    }).catch(function (error) {
      setStatus(
        isZh ? '目前無法送出，請稍後再試。' : 'We could not send your inquiry. Please try again shortly.',
        'error'
      );
      console.error('Inquiry submission failed:', error);
    }).finally(function () {
      submit.disabled = false;
      if (status) status.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
}());

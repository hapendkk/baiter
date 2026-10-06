//метод для копирования заголовка
document.addEventListener('click', function (e) {
  var btn = e.target.closest('.copy');
  if (!btn) return;
  var done = function () {
    btn.textContent = 'Copied';
    setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
  };
  if (navigator.clipboard) {
    navigator.clipboard.writeText(btn.dataset.copy).then(done, function () {});
  }
});

//показать имя выбранного файла
document.querySelectorAll('.dropzone input[type="file"]').forEach(function (input) {
  input.addEventListener('change', function () {
    var label = input.closest('.dropzone').querySelector('[data-file-name]');
    label.textContent = input.files.length ? input.files[0].name : '';
  });
});

//слово дженерейтинг пока человек ждет обработки
document.querySelectorAll('form').forEach(function (form) {
  form.addEventListener('submit', function () {
    var btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Generating\u2026';
    }
  });
});

//восстановление кнопки при возврате в раузере
window.addEventListener('pageshow', function (e) {
  if (!e.persisted) return;
  document.querySelectorAll('button[type="submit"]').forEach(function (btn) {
    btn.disabled = false;
    btn.textContent = 'Generate headlines';
  });
});

(function() {
  var overlay, img, caption, closeBtn;

  function createOverlay() {
    overlay = document.createElement('div');
    overlay.id = 'shadowbox-overlay';
    overlay.innerHTML =
      '<div id="shadowbox-close">&times;</div>' +
      '<div id="shadowbox-content">' +
        '<img id="shadowbox-img" src="" alt="">' +
        '<div id="shadowbox-caption"></div>' +
      '</div>';
    document.body.appendChild(overlay);

    img = document.getElementById('shadowbox-img');
    caption = document.getElementById('shadowbox-caption');
    closeBtn = document.getElementById('shadowbox-close');

    overlay.addEventListener('click', function(e) {
      if (e.target === overlay || e.target === closeBtn) {
        close();
      }
    });
    closeBtn.addEventListener('click', close);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') close();
    });
  }

  function open(src, title) {
    if (!overlay) createOverlay();
    img.src = src;
    img.alt = title;
    caption.textContent = title;
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function close() {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
    img.src = '';
  }

  document.addEventListener('DOMContentLoaded', function() {
    var links = document.querySelectorAll('#elenco_opere a');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function(e) {
        e.preventDefault();
        var href = this.getAttribute('href');
        var title = this.getAttribute('title') || '';
        open(href, title);
      });
    }
  });
})();

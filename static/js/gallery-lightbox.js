// Kipsolu Central FC - vanilla JS lightbox for the gallery page
document.addEventListener('DOMContentLoaded', function () {
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('.gallery-thumb'));
  if (thumbs.length === 0) return;

  var overlay = document.getElementById('lightbox-overlay');
  var overlayImg = document.getElementById('lightbox-image');
  var caption = document.getElementById('lightbox-caption');
  var takenAt = document.getElementById('lightbox-taken-at');
  var takenAtSep = document.getElementById('lightbox-taken-at-sep');
  var closeBtn = document.getElementById('lightbox-close');
  var prevBtn = document.getElementById('lightbox-prev');
  var nextBtn = document.getElementById('lightbox-next');

  var currentIndex = 0;

  function openLightbox(index) {
    currentIndex = index;
    var thumb = thumbs[currentIndex];
    var fullSrc = thumb.getAttribute('data-full') || thumb.querySelector('img').src;
    overlayImg.src = fullSrc;
    caption.textContent = thumb.getAttribute('data-caption') || '';

    var dateValue = thumb.getAttribute('data-taken-at') || '';
    takenAt.textContent = dateValue;
    takenAtSep.style.display = dateValue ? 'inline' : 'none';

    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  function showRelative(offset) {
    currentIndex = (currentIndex + offset + thumbs.length) % thumbs.length;
    openLightbox(currentIndex);
  }

  thumbs.forEach(function (thumb, index) {
    thumb.addEventListener('click', function () {
      openLightbox(index);
    });
  });

  closeBtn.addEventListener('click', closeLightbox);
  prevBtn.addEventListener('click', function () { showRelative(-1); });
  nextBtn.addEventListener('click', function () { showRelative(1); });

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeLightbox();
  });

  document.addEventListener('keydown', function (e) {
    if (!overlay.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') showRelative(-1);
    if (e.key === 'ArrowRight') showRelative(1);
  });
});
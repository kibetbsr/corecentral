// Kipsolu Central FC - navbar active link highlighter (vanilla JS, no frameworks)
document.addEventListener('DOMContentLoaded', function () {
  var currentPath = window.location.pathname;
  var navLinks = document.querySelectorAll('.navbar-kc .nav-link');

  navLinks.forEach(function (link) {
    var linkPath = link.getAttribute('href');
    if (!linkPath) return;

    if (linkPath === '/' && currentPath === '/') {
      link.classList.add('active');
    } else if (linkPath !== '/' && currentPath.indexOf(linkPath) === 0) {
      link.classList.add('active');
    }
  });
});

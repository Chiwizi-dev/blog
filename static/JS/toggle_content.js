document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.getElementById('toggleSectionButton');
  const collapsibleSection = document.getElementById('collapsibleSection');
  const dashboardLinks = document.getElementById('dashboardLinks');

  if (window.location.search === '?section=open') {
    collapsibleSection.style.display = 'block';
  }

  if (toggleButton && collapsibleSection) {
    toggleButton.addEventListener('click', function(event) {
      event.preventDefault();
      if (collapsibleSection.style.display === 'none' || collapsibleSection.style.display === '') {
        collapsibleSection.style.display = 'block';
        window.history.pushState({}, '', '?section=open');
      } else {
        collapsibleSection.style.display = 'none';
        window.history.pushState({}, '', window.location.pathname);
      }
    });
  }

  dashboardLinks.addEventListener('click', function(event) {
    if (event.target.tagName === 'A') {
      event.preventDefault();
      window.location.href = event.target.href + '?section=open';
    }
  });
});


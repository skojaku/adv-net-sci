<script>
document.addEventListener('keydown', function(e) {
  if (e.key === 's' && !e.ctrlKey && !e.metaKey && 
      e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
    e.preventDefault();
    e.stopPropagation();
  }
}, true);
</script>

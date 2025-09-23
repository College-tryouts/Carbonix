// Optional: Animate particles randomly
const particles = document.querySelectorAll('.particle');
particles.forEach(p => {
  const randomX = Math.random() * window.innerWidth;
  const randomY = Math.random() * window.innerHeight;
  p.style.left = randomX + 'px';
  p.style.top = randomY + 'px';
});

// carousel.js

let currentIndex = 0;

function moveSlide(direction) {
  const track = document.querySelector('.carousel-track');
  const totalSlides = track.children.length;
  currentIndex = (currentIndex + direction + totalSlides) % totalSlides;
  track.style.transform = `translateX(-${currentIndex * 100}%)`;
}

document.querySelector('.carousel-btn.prev').addEventListener('click', () => moveSlide(-1));
document.querySelector('.carousel-btn.next').addEventListener('click', () => moveSlide(1));

// Autoplay a cada 5 segundos
setInterval(() => {
  moveSlide(1);
}, 5000);

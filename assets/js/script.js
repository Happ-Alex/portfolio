let sidebarButton = document.querySelector('.sidebar-button');
let sidebar = document.querySelector('.sidebar');
let mainBody = document.querySelector('.main');
let screenHide = document.querySelector('.screen-hider');

sidebarButton.addEventListener('click', function(e) {
  sidebarButton.classList.toggle('active');
  sidebar.classList.toggle('active');
  mainBody.classList.toggle('active');
  screenHide.classList.toggle('active');
});

const navigationLink = document.querySelectorAll(".sidebar-nav__item")
const navigationPage = document.querySelectorAll(".section")

navigationLink.forEach((link,index) => {
  link.addEventListener("click", (nav) => {
    navigationLink.forEach((f) => f.classList.remove("active"));
    navigationPage.forEach((page) => {
      page.classList.add("hidden");
  });
    nav.target.classList.add("active")
    navigationPage[index].classList.remove("hidden")
    sidebarButton.classList.remove('active');
    sidebar.classList.remove('active');
    mainBody.classList.remove('active');
    screenHide.classList.remove('active');
  });
})



let count = 0;
let width;

const sliderLine = document.querySelector('.portfolio-slider');
const slides = document.querySelectorAll('.portfolio-box');

function init() {
  width = document.querySelector('.slider').offsetWidth;
  rollSlider();
}

init();
window.addEventListener('resize', init);

let touchstartX = 0;
let touchendX = 0;

sliderLine.addEventListener('touchstart', function (event) {
  touchstartX = event.changedTouches[0].clientX;
});

sliderLine.addEventListener('touchend', function (event) {
  touchendX = event.changedTouches[0].clientX;
  handleSwipe();
});

function handleSwipe() {
  const minSwipeDistance = 50; 
  const swipeDistance = touchstartX - touchendX;

  if (swipeDistance > minSwipeDistance) {
    count++;
    if (count >= slides.length) {
      count = 0;
    }
  } else if (swipeDistance < -minSwipeDistance) {
    count--;
    if (count < 0) {
      count = slides.length - 1;
    }
  }

  rollSlider();
}

function rollSlider() {
  if (window.innerWidth <= 950) {
    width = document.querySelector('.slider').offsetWidth;
    sliderLine.style.transform = 'translateX(-' + count * width + 'px)';
  }
}

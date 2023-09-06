// Sidebar navigation panel 
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
// portfolio accordion

const portfolioCollection = document.querySelectorAll(".portfolio-collection");
const portfolioLink = document.querySelectorAll('.portfolio-link');

portfolioLink.forEach((portEl, portIndex) => {
  portEl.addEventListener('click', () => {
    const currentCollection = portfolioCollection[portIndex];

    if (currentCollection.style.display) {
      currentCollection.style.display = null;
    } else {
      portfolioCollection.forEach((el) => el.style.display = null);
      currentCollection.style.display = "flex";

    }
  });
});




// toggles

let settingBlock = document.querySelector(".gear-block")
let settingButton = document.querySelector('.gear-button')
let settingPannel = document.querySelector('.gear')

settingButton.addEventListener('click', () => {
  settingPannel.classList.toggle('active');
  settingBlock.classList.toggle('active');
})

// day switcher
let toggleDay = document.querySelector('.ball');
let changeBody = document.querySelector('.body');

toggleDay.addEventListener("click", () => {
  toggleDay.classList.toggle('day');
  if (!toggleDay.classList.contains('day')) {
    changeBody.classList.add("dark")
  } else {
    changeBody.classList.remove("dark")
  }
});

// theme color

const colorChange = document.querySelectorAll('.alternate-style');

function setActiveStyle(color) {
  colorChange.forEach((style) => {
    if (color === style.getAttribute('title')) {
      style.removeAttribute("disabled");
    } else {
      style.setAttribute("disabled", "true")
    }
  });
};

// Swiper

const swiper = new Swiper('.swiper', {
    breakpoints: {
      1000: {
        slidesPerView: 'auto',
      },
    740: {
      slidesPerView: 2,
    },
    // when window width is >= 320px
    320: {
      slidesPerView: 1,
    }
  }
});

// 3D

document.addEventListener('mousemove', e => {
	Object.assign(document.documentElement, {
		style: `
		--move-x: ${(e.clientX - window.innerWidth / 2) * -.005}deg;
		--move-y: ${(e.clientY - window.innerHeight / 2) * .01}deg;
		`
	})
})

// 
alert("This site hasn`t been done properly yet (Цей сайт ще не завершено повністю)")

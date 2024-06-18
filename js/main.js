const swiper = new Swiper(".swiper", {
  effect: "fade",
  pagination: {
    el: ".swiper-pagination",
  },
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
});

const tabItem = document.querySelectorAll('.tabsbtn-item');
const tabContent = document.querySelectorAll('.tabscontent-item');

tabItem.forEach(function (element) {
  element.addEventListener('click', open);
});

  // Function to open modal
function openModal(modalId) {
var modal = document.getElementById(modalId);
modal.style.display = "block";
}

// Function to close modal
function closeModal(modalId) {
var modal = document.getElementById(modalId);
modal.style.display = "none";
}

// Close modal if user clicks outside of it
window.onclick = function(event) {
var modals = document.getElementsByClassName('modal');
for (var i = 0; i < modals.length; i++) {
  if (event.target == modals[i]) {
    modals[i].style.display = "none";
  }
}
}

function open(evt) {
  const tabTarget = evt.currentTarget;
  const tabTargetIndex = Array.from(tabItem).indexOf(tabTarget);

  tabItem.forEach(function(item) {
    item.classList.remove('tabsbtn-item--active');
  });
  tabContent.forEach(function(content) {
    content.classList.remove('tabscontent-item--active');
  });

  tabTarget.classList.add('tabsbtn-item--active');
  tabContent[tabTargetIndex].classList.add('tabscontent-item--active');



}
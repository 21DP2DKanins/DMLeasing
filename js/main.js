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

  const tabItem = document.querySelectorAll('.tabs__btn-item');
  const tabContent = document.querySelectorAll('.tabs__content-item');

  tabItem.forEach(function (element) {
    element.addEventListener('click', open);
  });

  function open(evt) {
    const tabTarget = evt.currentTarget;
    const tabTargetIndex = Array.from(tabItem).indexOf(tabTarget);

    tabItem.forEach(function(item) {
      item.classList.remove('tabs__btn-item--active');
    });
    tabContent.forEach(function(content) {
      content.classList.remove('tabs__content-item--active');
    });

    tabTarget.classList.add('tabs__btn-item--active');
    tabContent[tabTargetIndex].classList.add('tabs__content-item--active');

}


const acc = document.getElementsByClassName(".content-accordion__header");
var i;
var button = document.getElementsByClassName('.content-accordion__button');

for (i=0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("_active");
  })
};


let header__burger = document.querySelectorAll('.header__burger,.header-body-menu__link');
let header_menu = document.querySelector('.header-body-menu');
let back = document.querySelector('body');

header__burger.forEach(function (item) {
   item.onclick = function () {
      item.classList.toggle('active');
      header_menu.classList.toggle('active');
      back.classList.toggle('lock');
   }
});
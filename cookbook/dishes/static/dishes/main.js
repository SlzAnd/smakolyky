new Swiper('.image-slider', {
    // Навігація стрілками
    navigation: {
         //Вказуємо елементи з відповідними класами
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    },

    // Пагінація, крапки під слайдом
    //pagination: {
        // вказуємо елемент
        //el: '.swiper-pagination',
        // можливість перелістувати слайди при кліку на булети
        //clickable: true,
        // Булети змінюють розмір
        //dynamicBullets:true,
    //},

    // Курсор перетаскування
    grabCursor: true,

    // Перелистування при кліку
    slideToClickedSlide: true,

    // Керування клавіатурою
    keyboard: {
        enabled: true,
        onlyInViewport: true,
        pageUpDown: true,
    },

    // Керування колесом миші
    //mousewheel: {
        //sensitivity: 1,
        //eventsTarget: '.image-slider'
    //},

    // Автовисота
    autoHeight: true,

    // Кількість слайдів для показу
    slidesPerView: 1.1, 

    // Відключення функціоналу, якщо слайдів меньше ніж потрібно
    //watchOverflow: true,

    // Активний слайд по центру
    centeredSlide: false,

    // Стартовий слайд(починається з 0)
    initialSlide: 0,

    // Нескінченність прокручування
    loop: true,

    // Вільний режим
    freeMode: false,

    // Автопрокрутка
    autoplay: {
        delay: 3000,
        // Зупинитися на останньому слайді
        stopOnLastSlide: false,
        // Відключити після ручного перемикання
        disableOnInteraction: false,
    },
});

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
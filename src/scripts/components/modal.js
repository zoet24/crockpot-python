// Open/close modal
document.addEventListener('click', (e) => {
    if (!e.target.closest('.modal__buttons')) return;

    const modal = document.querySelector('.modal');
    const isOpen = document.querySelector('.modal__button--open');
    const isClose = e.target.closest('.modal__button--close');

    console.log(modal, isOpen, isClose)

    if (isOpen !== null) {
        modal.classList.remove("hide");
    }

    if (isClose !== null) {
        modal.classList.add("hide");
    }
});
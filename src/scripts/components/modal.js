// Open/close modal
document.addEventListener('click', (e) => {
    if (!e.target.closest('.modal__buttons')) return;

    // console.log(e.target)
    
    const modalIdentifier = e.target.closest('.modal__buttons').classList[1].split("--")[1];
    const modal = document.querySelector(`.modal--${modalIdentifier}`);
    const isOpen = document.querySelector(`.modal__button--open--${modalIdentifier}`);
    const isClose = e.target.closest(`.modal__button--close--${modalIdentifier}`);

    // console.log(modalIdentifier, modal, isOpen, isClose)

    if (isOpen !== null) {
        modal.classList.remove("hide");
    }

    if (isClose !== null) {
        modal.classList.add("hide");
    }
});
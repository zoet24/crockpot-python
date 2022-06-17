// Toggle switch
document.addEventListener('click', (e) => {
    if (!e.target.closest('.toggle__input')) return;

    const slider = e.target.closest('.toggle').querySelector('.toggle__slider');
    const isToggleBox = e.target.closest('.toggle-box__container');

    if (e.target.classList.contains('toggle__input--1')) {
        slider.style.transform = "translate(0%,0)";

        // If component is toggleBox show/hide content
        if (isToggleBox !== null) {
            isToggleBox.querySelector('.toggle-box__box-left').classList.remove("hide");
            isToggleBox.querySelector('.toggle-box__box-right').classList.add("hide");
        }
    }

    if (e.target.classList.contains('toggle__input--2')) {
        slider.style.transform = "translate(100%,0)";

        // If component is toggleBox show/hide content
        if (isToggleBox !== null) {
            isToggleBox.querySelector('.toggle-box__box-left').classList.add("hide");
            isToggleBox.querySelector('.toggle-box__box-right').classList.remove("hide");
        }
    }
});
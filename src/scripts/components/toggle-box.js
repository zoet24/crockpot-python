document.addEventListener('click', (e) => {
    if (!e.target.closest('.toggle-box__toggle-input')) return;
    
    const slider = e.target.closest('.toggle-box__toggle').querySelector('.toggle-box__toggle-slider');

    if (e.target.classList.contains('toggle-box__toggle-input--1')) {
        slider.style.transform = "translate(0%,0)";
    } else {
        slider.style.transform = "translate(100%,0)";
    }
});
// Add remove rows on recipe forms
document.addEventListener('click', (e) => {
    if (!e.target.closest('.btn-add-remove')) return;

    const isAdd = e.target.closest('.btn-add-remove__input--add');
    const isRemove = e.target.closest('.btn-add-remove__input--remove');

    const targetBtns = e.target.closest('.btn-add-remove');
    const targetRow = e.target.closest('.form__row');
    const targetInputs = targetRow.querySelectorAll('.form__inputs');
    const targetInputsNum = targetInputs.length;

    if (isAdd !== null) {
        var cloneInput = targetInputs[0].cloneNode(true);
        cloneInput.classList.remove("hide");
        targetRow.insertBefore(cloneInput, targetBtns);
    }

    if (isRemove !== null) {
        if (targetRow.querySelectorAll('.form__inputs').length > 2) {
            const cloneInputRemove = targetInputs[(targetInputsNum - 1)]
            cloneInputRemove.parentNode.removeChild(cloneInputRemove)
        }
    }
});
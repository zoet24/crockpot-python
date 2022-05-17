// Plus minus button
document.addEventListener('click', (e) => {
    if (!e.target.closest('.btn-plus-minus__input')) return;

    const num = e.target.closest('.btn-plus-minus__btn').querySelector('.btn-plus-minus__num');
    var numVal = parseInt(num.value);

    const minVal = num.getAttribute("min");
    const maxVal = num.getAttribute("max");
    const step = parseInt(num.getAttribute("step"));
    var stepUp = true;

    const isPlus = e.target.closest('.btn-plus-minus__input--plus');
    const isMinus = e.target.closest('.btn-plus-minus__input--minus');
    const isViewRecipe = e.target.closest('.view-recipe');
    const isEditRecipe = e.target.closest('.edit-recipe');

    if ((isPlus !== null) && (numVal < maxVal)) {
        numVal += step;
        stepUp = true;
    }

    if ((isMinus !== null) && (numVal > minVal)) {
        numVal -= step;
        stepUp = false;
    }

    num.value = numVal;

    if (isEditRecipe !== null) {
        multiplyInputs(numVal, stepUp);
    }

    if (isViewRecipe !== null) {
        multiplyIngs(numVal);
    }
});

// If on the same page as edit recipe, change quantity of ingredient inputs
function multiplyInputs(numVal, stepUp) {
    const targetInputs = document.querySelectorAll('.btn-plus-minus__targetInput');

    for (var i = 0; i < targetInputs.length; i++) {
        var targetInput = parseFloat(targetInputs[i].value);
        console.log(stepUp)
        if ((numVal > 1) && (stepUp == true)) {
            var targetInputSingle = targetInput / (numVal - 1);
        } else if ((numVal >= 1) && (stepUp == false)) {
            var targetInputSingle = targetInput / (numVal + 1);
        } else {
            var targetInputSingle = targetInput / (numVal);
        }
        targetInputs[i].value = targetInputSingle * numVal;
    }
}

// If on the same page as view recipe, change quantity of ingredients
function multiplyIngs(numVal) {
    const targetNums = document.querySelectorAll('.btn-plus-minus__targetNum');
    const targetNumsHidden = document.querySelectorAll('.btn-plus-minus__targetNum--hidden');
    const ingNums = document.querySelectorAll('.btn-plus-minus__ingNum');

    for (var i = 0; i < targetNums.length; i++) {
        var targetNum = targetNums[i];
        var targetNumHidden = targetNumsHidden[i];
        var ingNum = parseFloat(ingNums[i].innerHTML);
        var ingNumHidden = parseFloat(targetNumHidden.innerHTML);
        var targetNumNew = ingNum * numVal;

        if (String(ingNumHidden).includes('.')) {
            targetNum.innerHTML = targetNumNew.toFixed(2);
            if (targetNum.innerHTML.includes('.')) {
                if (targetNum.innerHTML.includes('.00')) {
                    targetNum.innerHTML -= ".00"
                }
                if (targetNum.innerHTML.slice(-1) == "0") {
                    targetNum.innerHTML -= "0"
                }
            }
        } else {
            targetNum.innerHTML = targetNumNew;
        }
    }
}
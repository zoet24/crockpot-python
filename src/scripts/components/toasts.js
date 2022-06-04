// Find toasts and fade them out one by one
window.addEventListener('load', (event) => {
    var i = 0;
    const toasts = document.querySelectorAll(".toast");
    const time = 1000;

    for (j = 1; j <= toasts.length; j++) {
        setTimeout(function() {
            hideToast();
        }, time * j);
    }

    function hideToast() {
        toasts[i].classList.add("fade-out");

        if (i == (toasts.length - 1)) {
            setTimeout(function() {
                for (k = 0; k < toasts.length; k++) {
                    toasts[k].classList.add("hide");
                }
            }, time);
        }

        i += 1;
    }
})

// Include proof details in print, then restore the reader's open/closed state.
(() => {
    let closedDetails = [];
    window.addEventListener("beforeprint", () => {
        closedDetails = [...document.querySelectorAll("details:not([open])")];
        closedDetails.forEach((detail) => { detail.open = true; });
    });
    window.addEventListener("afterprint", () => {
        closedDetails.forEach((detail) => { detail.open = false; });
        closedDetails = [];
    });
})();

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("adoptionModal");
    const openBtn = document.getElementById("adoptBtn");
    const closeBtn = document.querySelector(".modal-close");

    if(openBtn){
        openBtn.addEventListener("click", function () {
            modal.style.display = "flex";
        });
    }

    if(closeBtn){
        closeBtn.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    window.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

});

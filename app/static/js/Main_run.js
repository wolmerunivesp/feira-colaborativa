window.load = begin_();
function begin_(){
    setTimeout(function () {
        document.querySelector(".loading").style.display = "none"
        document.querySelector("#main_content").style.display = "block"
    }, 750)
}
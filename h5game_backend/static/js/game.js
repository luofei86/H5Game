var spirit, startX, startY;
$(document).ready(function(){
    var subXX = document.getElementById("answer_sub_1");
    var subXY = document.getElementById("answer_sub_2");
    var subYX = document.getElementById("answer_sub_3");
    var subYY = document.getElementById("answer_sub_4");    
    // add touch start listener
    subXX.addEventListener("touchStart", touchStart, false);
    subXX.addEventListener("click", touchStart, false);
});
 
function touchStart(event) {
    event.preventDefault();
    if (spirit ||! event.touches.length) return;
    var touch = event.touches[0];
    startX = touch.pageX;
    startY = touch.pageY;
    alert(startX)
    alert(startY)
// spirit = document.createElement(“div”);
// spirit.className = “spirit”;
// spirit.style.left = startX;
// spirit.style.top = startY;
// canvas.appendChild(spirit);
}
 

/*$(document).ready(function() {
  alert('pronto!');
  document.getElementById("Titulo").innerHTML = "Doc pronto";
});*/

var my_time;

function pageLoad() {
    let doc = document.getElementById("Titulo")
    if (doc){
          pageScroll();
          $(".tableContainer").mouseover(function() {
              this.mouseIsOver = true;
          }).mouseout(function() {
              this.mouseIsOver = false;
          });
    }
    else {
        setTimeout('pageLoad()', 500);
    }
}

var count=1;

function pageScroll() {
    count+=1;
    let objList = document.getElementsByClassName("tableContainer");

    for (var i = 0; i<objList.length; i++) {
        let objDiv = objList[i];

        if ((objDiv.parado) || (objDiv.mouseIsOver)) { continue; }

        objDiv.scrollTop = objDiv.scrollTop + 1;

        let scrollMax = objDiv.scrollHeight - objDiv.offsetHeight;

        if ((objDiv.scrollTop >= scrollMax) && (scrollMax > 0)) {
            objDiv.parado=true;

            setTimeout(function () {
                objDiv.scrollTop = 0;
                setTimeout(function () {
                    objDiv.parado=false;
                }, 500);
            }, 2000);
        }
    }
    clearTimeout(my_time);
    my_time = setTimeout('pageScroll()', 100);
}

setTimeout('pageLoad()', 500);







function disableEn() {
    var rd1 = document.getElementById("hospital2");
    var rd2 = document.getElementById("hospital4");
    var rd3 = document.getElementById("clinc");
    var rd4 = document.getElementById("lab");
    var rd5 = document.getElementById("center");
    var rd6 = document.getElementById("pharmacy");
    var sel1 = document.getElementById("hospital1");
    var sel2 = document.getElementById("hospital3");
    var sel3 = document.getElementById("clinc1");
    var sel4 = document.getElementById("lab1");
    var sel5 = document.getElementById("center1");
    var sel6 = document.getElementById("pharmacy1");
    if(rd1.checked)
    {
        sel1.disabled = false;
        sel2.disabled = true;
        sel4.disabled = true;
        sel5.disabled = true;
        sel3.disabled = true;
        sel6.disabled = true;
        sel4.value = 0;
        sel3.value = 0;
        sel2.value = 0;
        sel5.value = 0;
        sel6.value = 0;
    }
    else if(rd2.checked)
    {
        sel1.disabled = true;
        sel2.disabled = false;
        sel4.disabled = true;
        sel5.disabled = true;
        sel3.disabled = true;
        sel6.disabled = true;
        sel1.value = 0;
        sel3.value = 0;
        sel4.value = 0;
        sel5.value = 0;
        sel6.value = 0;
    }
    else if(rd3.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = true;
        sel5.disabled = true;
        sel3.disabled = false;
        sel6.disabled = true;
        sel1.value = 0;
        sel4.value = 0;
        sel2.value = 0;
        sel5.value = 0;
        sel6.value = 0;
    }
    else if(rd4.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = false;
        sel5.disabled = true;
        sel3.disabled = true;
        sel6.disabled = true;
        sel1.value = 0;
        sel3.value = 0;
        sel2.value = 0;
        sel5.value = 0;
        sel6.value = 0;
    }
    else if(rd5.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = true;
        sel5.disabled = false;
        sel3.disabled = true;
        sel6.disabled = true;
        sel7.disabled = true;
        sel1.value = 0;
        sel3.value = 0;
        sel2.value = 0;
        sel4.value = 0;
        sel6.value = 0;
        sel7.value = 0;
    }
    else if(rd6.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = true;
        sel5.disabled = true;
        sel3.disabled = true;
        sel6.disabled = false;
        sel7.disabled = true;
        sel1.value = 0;
        sel3.value = 0;
        sel2.value = 0;
        sel5.value = 0;
        sel4.value = 0;
        sel7.value = 0;
    }
}
function redir(){
    var hosSel = document.getElementById("hospital1");
    var hosSel2 = document.getElementById("hospital3");
    var nBtn = document.getElementById("nBtn1Link");
    if(hosSel.value == "مستشفى الأمومة"){
        nBtn.setAttribute("href", "main-hospital1");
    }
    if(hosSel2.value == "مستشفى عين شمس"){
        nBtn.setAttribute("href", "main-hospital2");
    }
}
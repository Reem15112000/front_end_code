function disableEn() {
    var rd1 = document.getElementById("hospital");
    var rd2 = document.getElementById("med");
    var rd3 = document.getElementById("clinc");
    var rd4 = document.getElementById("lab");
    var rd5 = document.getElementById("center");
    var sel1 = document.getElementById("hospital1");
    var sel2 = document.getElementById("med1");
    var sel3 = document.getElementById("clinc1");
    var sel4 = document.getElementById("lab1");
    var sel5 = document.getElementById("center1");
    if(rd1.checked)
    {
        sel2.disabled = true;
        sel3.disabled = true;
        sel4.disabled = true;
        sel5.disabled = true;
        sel1.disabled = false;
        sel2.value = 0;
        sel3.value = 0;
        sel4.value = 0;
        sel5.value = 0;
    }
    else if(rd2.checked)
    {
        sel1.disabled = true;
        sel3.disabled = true;
        sel4.disabled = true;
        sel5.disabled = true;
        sel2.disabled = false;
        sel1.value = 0;
        sel3.value = 0;
        sel4.value = 0;
        sel5.value = 0;
    }
    else if(rd3.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = true;
        sel5.disabled = true;
        sel3.disabled = false;
        sel1.value = 0;
        sel2.value = 0;
        sel4.value = 0;
        sel5.value = 0;
    }
    else if(rd4.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = false;
        sel5.disabled = true;
        sel3.disabled = true;
        sel1.value = 0;
        sel3.value = 0;
        sel2.value = 0;
        sel5.value = 0;
    }
    else if(rd5.checked)
    {
        sel1.disabled = true;
        sel2.disabled = true;
        sel4.disabled = true;
        sel5.disabled = false;
        sel3.disabled = true;
        sel1.value = 0;
        sel3.value = 0;
        sel2.value = 0;
        sel4.value = 0;
    }
}
function redir(){
    var hosSel = document.getElementById("hospital1");
    var nBtn = document.getElementById("nBtn1Link");
    if(hosSel.value == "النفسية"){
        nBtn.setAttribute("href", "hospital2-department1");
    }
    if(hosSel.value == "امراض الدم"){
        nBtn.setAttribute("href", "hospital2-department2");
    }
    if(hosSel.value == "الجراحة العامة"){
        nBtn.setAttribute("href", "hospital2-department3");
    }
    if(hosSel.value == "العظام"){
        nBtn.setAttribute("href", "hospital2-department4");
    }
}
let btn = document.getElementById('run');
btn.addEventListener('click', event=> { code(); });
function code() {

document.getElementById('output').innerHTML="";
var x = 5;
if ((x == 5)) {
document.getElementById("output").innerHTML +=(parseInt(5) + parseInt(3))+"<br>";
}
else {
document.getElementById("output").innerHTML +=10+"<br>";

}

}
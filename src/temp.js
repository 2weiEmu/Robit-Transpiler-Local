let btn = document.getElementById('run');
btn.addEventListener('click', event=> { code(); });
function code() {

document.getElementById('output').innerHTML="";
var x = 1;
switch (x) {

case (5):
{
document.getElementById("output").innerHTML +="five"+"<br>";

}
break;
case (6):
{
document.getElementById("output").innerHTML +="six"+"<br>";

}
break;
case (7):
{
document.getElementById("output").innerHTML +="house"+"<br>";

}
break;
default:
{
document.getElementById("output").innerHTML +="nothing"+"<br>";

}
break;
}

}
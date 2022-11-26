let btn = document.getElementById('run');
btn.addEventListener('click', event=> { code(); });
function code() {

document.getElementById('output').innerHTML="";
var n = prompt('Input', 'Your input...');
while ((n < 5)) {
document.getElementById("output").innerHTML +="Iteration"+"<br>";

document.getElementById("output").innerHTML +=n+"<br>";

var n = (parseInt(n + 2));

}
document.getElementById("output").innerHTML +=n+"<br>";

}
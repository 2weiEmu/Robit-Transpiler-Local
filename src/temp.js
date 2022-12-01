let btn = document.getElementById('run');
btn.addEventListener('click', event=> { code(); });
function code() {

document.getElementById('output').innerHTML="";
var k = prompt('Input', 'Your input...');
for (var x = parseInt(0); x < parseInt(k) + 1;x += 1){
if (((parseInt(x) % parseInt(3)) == 0)) {
document.getElementById("output").innerHTML +="x is a multiple of 3"+"<br>";

document.getElementById("output").innerHTML +=x+"<br>";
}
}

}
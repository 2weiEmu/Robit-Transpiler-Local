let btn = document.getElementById('run');
btn.addEventListener('click', event=> { code(); });
function code() {

document.getElementById('output').innerHTML="";
var k = prompt('Input', 'Your input...');
for (var x = parseInt(0); x < parseInt(k) + 1;x += 1){
if (((parseInt(x) % parseInt(2)) == 0)) {
document.getElementById("output").innerHTML +="x is even"+"<br>";

document.getElementById("output").innerHTML +=x+"<br>";
}
}

}
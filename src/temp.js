let btn = document.getElementById('run');
btn.addEventListener('click', event=> { code(); });
function code() {

document.getElementById('output').innerHTML="";
for (var X = 0; X < 6 + 1;X += 2){
document.getElementById("output").innerHTML +="Xs current value is:"+"<br>";

document.getElementById("output").innerHTML +=X+"<br>";
}

}
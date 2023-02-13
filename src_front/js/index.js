
// Enabling easier tabbing
document.getElementById('code').addEventListener('keydown', function(e) {
    if (e.key == 'Tab') {
      e.preventDefault();
      var start = this.selectionStart;
      var end = this.selectionEnd;
  
      // set textarea value to: text before caret + tab + text after caret
      this.value = this.value.substring(0, start) +
        "\t" + this.value.substring(end);
  
      // put caret at right position again
      this.selectionStart = this.selectionEnd = start + 1;
    }
  });

var run_button = document.getElementById("run_button");

var code_editor = document.getElementById("code");
var code_data;

var result_area = document.getElementById("result");

run_button.addEventListener("click", collectCode);

function update_run_button(run_button, text, colour) {
  run_button.style.backgroundColor = colour;
  run_button.innerHTML = text;
}

function collectCode() {
  update_run_button(run_button, "TRANSPILING", "FFE76A")

  code_data = code_editor.value;
  console.log(code_data)
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/entered_code",
    data: code_data,
    success: function (result) {
      result = result.slice(2);
      result = result.slice(0, -2);
      result = result.split('","');
      console.log(result);
      if (result[0] === 'robit_trp_failure') {
        document.getElementById("result").innerHTML = result[0] + '\n' + result[1];
        
        update_run_button(run_button, "RUN", "#91FF6A");
      }
      else {
        var script_area = document.createElement("script");
        script_area.type = "text/javascript";
        script_area.id = "transpiled";
        script_area.innerHTML = "function execute_transpiled() {\n";
        for (var i = 0; i < result.length; i++) {
          script_area.innerHTML += String(result[i]) + "\n";
        }
        script_area.innerHTML += "console.log('completed');}";
        
        document.getElementById("temp").innerHTML = "";
        result_area.innerHTML = "";
        document.getElementById("temp").appendChild(script_area);
  
        update_run_button(run_button, "RUNNING", "#FF6A6A");
        execute_transpiled();
        update_run_button(run_button, "RUN", "#91FF6A");
      }
      
    },
    timeout: 3000,
    error: function(request, status, error) {
      result_area.innerHTML = "The Transpile has failed. (The Server is probably unavailable)."
      update_run_button(run_button, "RUN", "#91FF6A");
    },
    dataType: 'text'
  }
  );
  

}
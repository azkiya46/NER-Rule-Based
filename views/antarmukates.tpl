%rebase base apptitle=apptitle
<div style="float:left">
    <form method="POST" id="newcat" action="#" onsubmit="return getresult();">
        <div class="formsection">
        <select name="task" id="task">
            <option value='ner'>Entitas Bernama</option>
            <option value='postag'>POS Tag</option>
        </select>
        </div>
    	<textarea cols="80" rows="25" name="teks" id="teks"></textarea><br/>
        <div class="formsection">
    	<input type="submit" name="save" value="Tag"/>
        </div>
    </form>

    <form action="/upload" method="POST" enctype="multipart/form-data">
      masukkan file .txt: <br>
      <input type="file" name="upload" id="input" />
      <HR>
      <button type="button" onclick="myFunction()">split</button>
    </form>
</div>

<div id="result" style="width:500px;background-color:#ccc;float:left;margin: 3.5em 2em;padding:8px;">&nbsp;</div>
<div id="demo" style="width:100%;float:none"></div>
<script type="text/javascript">

    function getresult(){
        var param = {}
        param["teks"] = $("#teks").val()
        param["task"] = $("#task").val()
        $.post('{{root}}/handler', param, function(data) {
          $("#result").html(data)
        }
        );
        return false;
    }
    function readSingleFile(e) { 
        console.log("check");
        var file = e.target.files[0];
        if (!file) {
        return;
      }
      var reader = new FileReader();
      reader.onload = function(e) {
        var contents = e.target.result;
        displayContents(contents);
      };
      reader.readAsText(file);
    }

    function displayContents(contents) {
      var element = document.getElementById('teks');
      element.innerHTML = contents;
    }

    document.getElementById('input')
      .addEventListener('change', readSingleFile, false);

    function myFunction() {
    var str = document.getElementById("result").innerHTML;
    console.log(str);
    var res = str.split(" ");
    var result = "<HR>";
    for (var i=0; i<res.length; i++) {
      result=result+res[i]+"<br>";
    } 
    document.getElementById("demo").innerHTML=result;
    }
</script>

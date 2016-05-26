%rebase base apptitle=apptitle
<hr>
<center>Pengenalan Entitas Bernama </center><hr>
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
    </form>
</div>

<div id="result" style="width:500px;background-color:#ccc;float:left;margin: 3.5em 2em;padding:8px;">&nbsp;</div>
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

</script>

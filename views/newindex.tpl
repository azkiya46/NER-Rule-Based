%rebase base apptitle=apptitle
<form method="POST" id="newcat" action="#" onsubmit="return getresult();">
    <div class="formsection">
    <select name="task" id="task">
        <option value='postag'>POS Tag</option>
        <option value='ner'>Entitas Bernama</option>
    </select>
    </div>
	<textarea cols="80" rows="25" name="teks" id="teks"></textarea><br/>
    <div class="formsection">
	<input type="submit" name="save" value="Tag"/>
    Masukkan file .txt: <input type="file" name="browse" value="Pilih file"/>
    </div>
</form>
<div id="result" style="width:500px;background-color:#ccc;float:left;margin: 0em 1em;padding:8px;">&nbsp;</div>
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
</script>

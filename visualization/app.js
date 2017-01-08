var express = require("express");
var app     = express();
var path    = require("path");
app.use(express.static(__dirname));

app.get('/pepe',function(req,res){
  res.sendFile(path.join(__dirname+'/index.html'));
  //__dirname : It will resolve to your project folder.
});

app.get('/p', function(req, res) {
  var spawn = require("child_process").spawn;
  //var process = spawn('python',[path.join(__dirname,'../visualizer.py'), req.query.timelineElementID]);
  var pythonPath = path.join(__dirname,'../visualizer.py')
  var process = spawn('python',[pythonPath, req.query.timelineElementID]);

  //res.send(pythonPath);
  //res.send("timelineElementID is set to " + req.query.timelineElementID);
  process.on('exit', function() {
      res.sendFile(path.join(__dirname+'/index.html'));
  //process.exit()
})

});

// GET /p?timelineElementID=5
// timelineElementID is set to 5

app.get('/about',function(req,res){
  res.sendFile(path.join(__dirname+'/about.html'));
});

app.get('/sitemap',function(req,res){
  res.sendFile(path.join(__dirname+'/sitemap.html'));
});

app.listen(8030);

console.log("Running at Port 8030");

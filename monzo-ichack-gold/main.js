

//var express = require('express');
//var app = express();

// set the port of our application
// process.env.PORT lets the port be set by Heroku
//var port = process.env.PORT || 8080;

//// set the view engine to ejs
//app.set('view engine', 'ejs');
//
//// make express look in the public directory for assets (css/js/img)
//app.use(express.static(__dirname + '/public'));
//
//// set the home page route
//app.get('/', function(req, res) {
//
//    // ejs render automatically looks in the views folder
//    res.render('index');
//});
//
//app.listen(port, function() {
//    console.log('Our app is running on http://localhost:' + port);
//});
var http = require('http')


var express = require("express");
var app = express();
app.get("/", function(req, res) {
  
  var body = JSON.stringify({
      type: "transaction.created"
  })
  
  var request = new http.ClientRequest({
      hostname: "129.31.186.106",
      port: 8080,
      path: "/monzo",
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body)
      }
  });
  
  request.end(body)
  res.send("Heroku Demo!");
});

// bind the app to listen for connections on a specified port
 var port = process.env.PORT || 5000;
 app.listen(port);

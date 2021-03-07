var express = require('express')
var app = express()
const exec = require('child_process').exec
var bodyParser = require('body-parser')
var partials = require('express-partials');

var urlEncodedParser = bodyParser.urlencoded({extended: false});
app.set('view engine','ejs')
app.use(partials())
app.use(express.static("public"))

app.post('/contact',urlEncodedParser,function(req,resp){
    var data = req.body
    var fname = data['fname']
    var lname = data['lname']
    var email = data['email']
    var msg = data['msg']
    exec(`python database.py -m insert-contact --fname ${fname} --lname ${lname} --email ${email} --msg ${msg}`)
    resp.render("index")
})

app.post('/track',urlEncodedParser,function(req,resp){
    var data = req.body
    console.log('Tracking number : ' + data['num'])
    resp.render('track',{num:data['num']})
})

app.get('/',function(req,resp){
    resp.render("index")
})

app.listen(80)

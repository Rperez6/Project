// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const session = require('express-session');
const axios = require('axios');

app.use(session({ secret: '123', resave: false, saveUninitialized: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));

// set the view engine to ejs
app.set('view engine', 'ejs');

//default page
app.get('/', (req, res) => {
  res.render('login',{showAverages: false});
});
//default page
app.get('/login', (req, res) => {
  res.render('login',{showAverages: false});

});
//Login function
app.post('/login', (req, res) => {
  const username = req.body.username;
  const password = req.body.password;

  const validUsername = 'admin'; // Replace with your desired username
  const validPassword = 'admin'; // Replace with your desired password

  if (username === validUsername && password === validPassword) {
      req.session.loggedIn = true;
      res.redirect('index');
  } else {
      res.send('Invalid credentials');
  }
});
//default page
app.get('/index', (req, res) => {
  res.render('index',{showAverages: false});
});

//average results
app.get('/fetch-averages', (req, res) => {
  axios.get('https://dummyjson.com/carts')
    .then((response) => {
      const carts = response.data.carts;

      const averages = carts.map((cart) => {
        const totalAmount = cart.total;
        const totalQuantity = cart.totalQuantity;
        return totalAmount / totalQuantity;
      });

      res.render('index', { averages, showAverages: true });
    })
});

//Captains Page
app.get('/captains', (req, res) => {
  res.render('captains',{showAverages: false});
});
//GET
app.get('/api/captains/all', async (req, res) => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/captains/all');
    const captains = response.data.captains;
    res.json(captains);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error fetching captains');
  }
});
//Post
app.post('/api/captains', async (req, res) => {
  try {
    const captainData = req.body;
    const response = await axios.post('http://127.0.0.1:5000/api/captains', captainData);
    res.send(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error adding captain');
  }
});
//Delete
app.delete('/api/captains/delete/:capt_badge', function(req, res) {
  const capt_badge = req.params.capt_badge;
  res.setHeader('Content-Type', 'text/plain');
  res.write(`Are you sure you want to delete captain badge ${capt_badge}?`);
  res.end();
});




//cargo Page
app.get('/cargo', (req, res) => {
  res.render('cargo',{showAverages: false});
});

//ship Page
app.get('/ships', (req, res) => {
  res.render('ships',{showAverages: false});
});

app.listen(8080, () => {
  console.log('8080 = webpage');
});

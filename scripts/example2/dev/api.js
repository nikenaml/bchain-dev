const express = require('express')
const app = express()

// We can handle different end points or different routes.
// For example, we have a get endpoint, which is just slash. And with this endpoint, we are sending back the response of Hello World and then this whole server is listening on Port 3000

app.get('/', function (req, res) {
  res.send('Hello World')
})

app.listen(3000)
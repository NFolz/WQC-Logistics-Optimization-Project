const fs = require('fs').promises;
const express = require('express');
const cors = require('cors');


const app = express();
const port = 3000;

// Serve static files from the 'client' directory
//app.use(express.static(path.join(__dirname, '../client')));

jsonData=null

app.use(cors());
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  })


fs.readFile('testing/routes.json', 'utf8')
    .then(data => {
        jsonData = JSON.parse(data);
        console.log(jsonData); })
        .catch(error => {
            console.error("Error loading JSON file:", error);
        });

app.get('/routes', function(req, res) {
    // console.log(jsonData)
            res.json(jsonData)
});
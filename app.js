const path = require('path')
const express = require('express')
const hbs = require('hbs')

const getCountriesLastReport = require('./data-scraping/worldometers-data.js')
const getCountriesTimeLine = require('./data-scraping/gitHubCoronaData.js')


const app = express()
const publicDirectoryPath = path.join(__dirname, './public')
const viewsPath = path.join(__dirname, './templates/views')
const partialsPath = path.join(__dirname, './templates/partials')

app.set('view engine', 'hbs')
app.set('views', viewsPath)
hbs.registerPartials(partialsPath)

app.use(express.static(publicDirectoryPath))


app.get('/countries-last-report', (req, res) => {
    getCountriesLastReport((data) => {
        res.send(data)
    })
})

app.get('/patients-timeline', (req, res) => {
    getCountriesTimeLine((data) => {
        res.send(data)
    })
})

app.get('/', (req, res) => {
    res.render('index', {
        name: 'Alon'
    })
})

app.listen(3000, () => {
console.log('Server is up on port 3000.')
})
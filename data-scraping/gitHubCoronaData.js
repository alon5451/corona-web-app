const request = require('request');
const cheerio = require('cheerio');


const getCountriesData = (callback) => {
    const url = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

    request(url, function (error, response, html) {
        if (!error) {
            // console.log(html)
            const $ = cheerio.load(html)
            // console.log(instElements.length)
            const tableElement = $("table")
            const tableHeaders = tableElement.find('thead').find('th').map(function() {
                return $(this).text().trim()
            }).get();
            const headersNum = tableHeaders.length
    
    
            const tableData = $(tableElement.find('tbody')[0]).find('tr').map(function() {
                const cells = $(this).find('td')
                let rowData = {}
                for (let i=0; i<headersNum; i++) {
                    rowData[tableHeaders[i]] = $(cells[i+1]).text().trim()
                }
                return rowData
            }).get()
            
    

            callback ({
                countriesTimeLine: tableData,
            })
    
        }
        
      })

      
}


module.exports = getCountriesData





// const potusParse = function(url) {
//   return rp(url)
//     .then(function(html) {
//         // console.log(html)
//       return {
//         table: $('#main_table_countries', html).text(),
//       };
//     })
//     .catch(function(err) {
//       //handle errors
//     });
// };

// console.log(potusParse(url))
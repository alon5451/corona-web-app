const request = require('request');
const cheerio = require('cheerio');


const getCountriesData = (callback) => {
    const url = 'https://www.worldometers.info/coronavirus/#countries'

    request(url, function (error, response, html) {
        if (!error) {
            const $ = cheerio.load(html)
            const tableElement = $("#main_table_countries")
            const tableHeaders = tableElement.find('thead').find('th').map(function() {
                return $(this).text().trim()
            }).get();
            const headersNum = tableHeaders.length
    
    
            const tableData = $(tableElement.find('tbody')[0]).find('tr').map(function() {
                const cells = $(this).find('td')
                let rowData = {}
                for (let i=0; i<headersNum; i++) {
                    rowData[tableHeaders[i]] = $(cells[i]).text().trim()
                }
                return rowData
            }).get()
    
    
            let total = {}
            Object.values(Object.assign({}, tableHeaders.slice(1,8))).map(function(key, index) {
                total[key] = 0;
              });
    
            let avgSum = 0
            for (let i=0; i<tableData.length; i++) {
                const row = tableData[i]
                for (let i=1; i<headersNum; i++) {
                    const column = tableHeaders[i]
                    const value = parseFloat(row[column].replace('+','').replace(',',''))
                    // console.log(column.slice(0,4) != 'Tot ')
                    // console.log(typeof 'Tot Cases/1M pop')
                    if (!isNaN(value) && i != 8) {
                        total[column] += value
                    } else if (!isNaN(value) && i == 8) {
                        avgSum += value
                    }
                    
                }
            }
            total['Tot Cases/1M pop'] = Math.round(avgSum/tableData.length * 1000) / 1000

            callback ({
                countriesReport: tableData,
                totalReport: total,
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
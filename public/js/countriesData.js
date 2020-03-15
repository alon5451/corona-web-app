const fetchData = (url, callback) => {
    fetch(url).then((res) => {
        res.json().then((data) => {
            callback(data)
        })
    })
}

function search(nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {
        if (myArray[i]['Country,Other'] === nameKey) {
            return myArray[i];
        }
    }
}

fetchData('./countries-last-report', (data) => {
    const israelData = search('Israel', data.countriesReport)
    const totCases = Object.keys(israelData).map((i) => {
        return i
    })[8]
    const totalData = data.totalReport
    console.log(totalData)
    const insertValues = [
        {id: 'perMillion', title: 'מספר חולים / מיליון אזרחים', propertyName: totCases, bgColor: '#65b1ef33'},
        {id: 'totalCases', title: 'מספר חולים', propertyName: 'TotalCases', bgColor: '#ef656e33'},
        {id: 'newCases', title: 'מקרים חדשים', propertyName: 'NewCases', bgColor: '#70ef6533'},
        {id: 'totalDeaths', title: 'מקרי מוות', propertyName: 'TotalDeaths', bgColor: '#efaf6533'},
        {id: 'newDeaths', title: 'מקרי מוות חדשים', propertyName: 'NewDeaths', bgColor: '#ef65c733'},
        {id: 'totalRecovered', title: 'מקרי החלמה', propertyName: 'TotalRecovered', bgColor: '#efaf6533'},
        {id: 'activeCases', title: 'מקרים פעילים', propertyName: 'ActiveCases', bgColor: '#ef656533'},
        {id: 'criticalCases', title: 'חולים במצב קשה', propertyName: 'Serious,Critical', bgColor: '#ef65b433'},
    ]
    $('.compareBox').css({'animation':'none'})
    for (let i=0; i<insertValues.length; i++) {
        const v = insertValues[i]
        const e = $('#'+v['id'])

        const israelValue = israelData[v['propertyName']]

        if (v['id']=='perMillion') {
            e.find('.worldText').find('p').text(totalData['Tot Cases/1M pop']) 
        }
    
        e.find('.titleDiv').css({'background-color': v['bgColor']})
        e.find('.title').text(v['title']) 
        e.find('.worldText').find('p').text(totalData[v['propertyName']]) 
        e.find('.israelText').find('p').text(israelValue!='' ? israelValue : 0) 
    }    
})
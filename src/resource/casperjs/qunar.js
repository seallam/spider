// 创建浏览器
var casper = require('casper').create({
    //verbose: true,
    //logLevel: "debug",
    clientScripts: [
        '../jQuery/jquery-1.7.2.js'
    ],
    pageSettings: {
        loadImages: false,
        loadPlugins: true,
        // 伪造 agent
        userAgent: 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    },

    viewportSize: {
        width: 1920,
        height: 1080
    }
});

var searchDate = casper.cli.get(0);
var limitPrice = casper.cli.get(1);

// casper.start('searchDepartureAirport=%E5%A4%A7%E8%BF%9E&searchArrivalAirport=%E9%87%8D%E5%BA%86&'
//     + 'searchDepartureTime=2017-10-25&searchArrivalTime=2017-10-26&nextNDays=0&'
//     + 'startSearch=true&fromCode=DLC&toCode=CKG&from=flight_dom_search&lowestPrice=null'
// );
casper.start(url='https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E5%B9%BF%E5%B7%9E&searchArrivalAirport=%E6%88%90%E9%83%BD&searchDepartureTime=2017-09-30&searchArrivalTime=2017-10-03&nextNDays=0&startSearch=true&fromCode=CAN&toCode=CTU&from=flight_dom_search&lowestPrice=null')

casper.waitFor(function check() {
    return this.evaluate(function () {
        return document.querySelectorAll('div.b-airfly').length > 1;
    });
}, function then() {

    var result = this.evaluate(function (airDate, airPrice) {
        var airList = document.querySelectorAll('div.b-airfly');

        var resultObj = {};
        var resultArray = [];

        for (var i = 0; i < airList.length; i++) {
            var air = airList[i];
            resultArray.push(air.textContent);
        }

        resultObj.date = airDate;
        resultObj.list = resultArray;
        return JSON.stringify(resultObj);

    }, searchDate, limitPrice);

    this.echo(result);

}, function timeout() {
    this.echo("Connection time out .").exit();
}, 60000);

casper.run();
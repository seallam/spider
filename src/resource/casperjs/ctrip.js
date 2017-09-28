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

casper.start(url='http://flights.ctrip.com/booking/can-ctu-day-1.html?ddate1=2017-10-09#DDate1=2017-10-10');

casper.wait_for(function check() {
    return this.evaluate(function () {
        return document.querySelectorAll('#J_flightlist2 .search_box').length > 1;
    });
}, function then() {
    this.evaluate()
});

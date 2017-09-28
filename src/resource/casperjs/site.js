//USAGE: E:\toolkit\n1k0-casperjs-e3a77d0\bin>python casperjs site.js --url=http://spys.ru/free-proxy-list/IE/ --outputfile='temp.html'

var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages: false,
        loadPlugins: false,
        userAgent: 'Mozilla/5.0 (windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
    },
    logLevel: "debug",//日志等级
    verbose: true // 记录日志到控制台
});
var url = casper.cli.raw.get('url');
var outputfile = casper.cli.raw.get('outputfile');
//请求页面
casper.start(url, function () {
    fs.write(outputfile, this.getHTML(), 'w');
});

casper.run();
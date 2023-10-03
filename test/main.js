const {JSDOM} = require("jsdom");
const {Readability} = require("@mozilla/readability");
const fs = require('fs');

(async () => {
    const {Readability} = require('@mozilla/readability');
    const {JSDOM} = require('jsdom');

    const url = "https://web.dev/howbrowserswork/"

    const response = await fetch(url)

    const htmlBody = await response.text()

    let doc = new JSDOM(htmlBody);
    let reader = new Readability(doc.window.document);
    let article = reader.parse();

    const htmlText = article.content;

    console.log(article)

    fs.writeFile('output.html', htmlText, (err) => {

        // In case of an error throw err.
        if (err) throw err;
    })
})();

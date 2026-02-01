const fs = require('fs');
const pdfLib = require('pdf-parse');

let dataBuffer = fs.readFileSync('kejian/Day 2.pdf');

// Check if pdfLib is a function or has default
const parse = (typeof pdfLib === 'function') ? pdfLib : pdfLib.default;

let options = {
    pagerender: function(pageData) {
        // This function returns the text content of the page
        return pageData.getTextContent()
        .then(function(textContent) {
            let lastY, text = '';
            for (let item of textContent.items) {
                if (lastY == item.transform[5] || !lastY){
                    text += item.str;
                }  
                else{
                    text += '\n' + item.str;
                }                                                    
                lastY = item.transform[5];
            }
            // Mark page end
            return `---PAGE ${pageData.pageIndex + 1} START---\n${text}\n---PAGE ${pageData.pageIndex + 1} END---`;
        });
    }
}

parse(dataBuffer, options).then(function(data) {
    const text = data.text;
    const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);
    
    const items = [];
    let currentPage = 1;
    
    const isThai = (str) => /[\u0E00-\u0E7F]/.test(str);
    const isChinese = (str) => /[\u4E00-\u9FFF]/.test(str);
    const isPageMarker = (str) => /^---PAGE \d+ (START|END)---$/.test(str);

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        if (line.startsWith('---PAGE ') && line.endsWith(' START---')) {
            currentPage = parseInt(line.match(/(\d+)/)[0]);
            continue;
        }
        
        if (isPageMarker(line)) continue;

        // Look ahead for pattern
        if (i + 2 < lines.length) {
            const l1 = lines[i];
            const l2 = lines[i+1];
            const l3 = lines[i+2];
            
            // Avoid processing markers as content
            if (isPageMarker(l1) || isPageMarker(l2) || isPageMarker(l3)) continue;

            if (isThai(l1) && !isChinese(l1) && 
                !isThai(l2) && !isChinese(l2) && 
                isChinese(l3) && !isThai(l3)) {
                
                items.push({
                    thai: l1,
                    phonetic: l2,
                    chinese: l3,
                    page: currentPage
                });
                i += 2; 
            }
        }
    }
    
    console.log(JSON.stringify(items, null, 2));
    fs.writeFileSync('data/day2.json', JSON.stringify(items, null, 2));
});

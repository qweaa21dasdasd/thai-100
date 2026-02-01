const { PDFDocument, PDFName } = require('pdf-lib');
const fs = require('fs');

(async () => {
    const pdfBytes = fs.readFileSync('kejian/Day 2.pdf');
    const pdfDoc = await PDFDocument.load(pdfBytes);
    
    const pages = pdfDoc.getPages();
    let imgCount = 0;
    const imagesMeta = [];

    // Ensure output directory exists
    if (!fs.existsSync('public/images/day2')) {
        fs.mkdirSync('public/images/day2', { recursive: true });
    }

    for (let i = 0; i < pages.length; i++) {
        const page = pages[i];
        const { width, height } = page.getSize();
        console.log(`Page ${i + 1}: ${width}x${height}`);
        
        // This is a bit lower-level, pdf-lib doesn't have a high-level "getImages"
        // We need to inspect the page's resources
        
        // Note: This approach is complex in pure pdf-lib without helper logic. 
        // pdf-lib is mostly for creation/modification.
        // However, we can try to access the XObject dictionary.
    }
    
    // Actually, extracting images with pdf-lib is non-trivial because encoding varies (Flate, DCT, etc.)
    // pdf-lib can COPY images to another PDF, but extracting raw bytes to PNG/JPG is hard if not just raw stream copy.
    
    console.log("pdf-lib might not be the best tool for extraction to files.");
})();

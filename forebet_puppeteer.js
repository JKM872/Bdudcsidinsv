/**
 * 🔥 FOREBET PUPPETEER SCRAPER - STEALTH MODE 🔥
 * ================================================
 * Używa Puppeteer Extra z pluginem Stealth do ominięcia Cloudflare.
 * Zapisuje HTML do pliku dla Python scrapera.
 * 
 * Uruchomienie:
 *   node forebet_puppeteer.js <sport> <output_file>
 * 
 * Przykład:
 *   node forebet_puppeteer.js football forebet_football.html
 */

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');

// Dodaj plugin stealth
puppeteer.use(StealthPlugin());

// Sport URLs
const SPORT_URLS = {
    'football': 'https://www.forebet.com/en/football-tips-and-predictions-for-today',
    'soccer': 'https://www.forebet.com/en/football-tips-and-predictions-for-today',
    'basketball': 'https://www.forebet.com/en/basketball/predictions-today',
    'tennis': 'https://www.forebet.com/en/tennis/predictions-today',
    'volleyball': 'https://www.forebet.com/en/volleyball/predictions-today',
    'handball': 'https://www.forebet.com/en/handball/predictions-today',
    'hockey': 'https://www.forebet.com/en/hockey/predictions-today',
    'ice-hockey': 'https://www.forebet.com/en/hockey/predictions-today'
};

// Consent button selectors
const CONSENT_SELECTORS = [
    'button.fc-cta-consent',
    '.fc-cta-consent',
    'button[data-cookiefirst-action="accept"]',
    '#onetrust-accept-btn-handler',
    'button:has-text("Accept")',
    'button:has-text("Agree")',
    'button:has-text("Zgadzam")'
];

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function randomDelay(min = 1000, max = 3000) {
    const ms = Math.floor(Math.random() * (max - min + 1)) + min;
    return delay(ms);
}

async function clickConsent(page) {
    console.log('🍪 Szukam przycisku consent...');
    
    for (const selector of CONSENT_SELECTORS) {
        try {
            const button = await page.$(selector);
            if (button) {
                const isVisible = await button.isIntersectingViewport();
                if (isVisible) {
                    console.log(`🍪 Klikam: ${selector}`);
                    await button.click();
                    await delay(2000);
                    return true;
                }
            }
        } catch (e) {
            // Kontynuuj do następnego selektora
        }
    }
    
    // Fallback - szukaj po tekście
    try {
        const buttons = await page.$$('button');
        for (const button of buttons) {
            const text = await page.evaluate(el => el.textContent, button);
            if (text && /accept|agree|zgadzam|consent/i.test(text)) {
                console.log(`🍪 Klikam button z tekstem: ${text.substring(0, 30)}`);
                await button.click();
                await delay(2000);
                return true;
            }
        }
    } catch (e) {
        // Ignore
    }
    
    console.log('🍪 Nie znaleziono przycisku consent');
    return false;
}

async function waitForContent(page) {
    console.log('⏳ Czekam na załadowanie treści...');
    
    // Czekaj na różne możliwe selektory meczów
    const selectors = [
        'div.rcnt',
        'tr.tr_0',
        'tr.tr_1',
        'div.schema',
        '.contentmiddle',
        'table.schema'
    ];
    
    for (const selector of selectors) {
        try {
            await page.waitForSelector(selector, { timeout: 10000 });
            console.log(`✅ Znaleziono: ${selector}`);
            return true;
        } catch (e) {
            // Kontynuuj do następnego
        }
    }
    
    return false;
}

async function simulateHumanBehavior(page) {
    console.log('🖱️ Symulacja zachowania człowieka...');
    
    // Scroll
    await page.evaluate(() => {
        window.scrollBy(0, 300);
    });
    await randomDelay(500, 1500);
    
    await page.evaluate(() => {
        window.scrollBy(0, 500);
    });
    await randomDelay(500, 1500);
    
    // Scroll back up
    await page.evaluate(() => {
        window.scrollTo(0, 0);
    });
    await randomDelay(1000, 2000);
}

async function scrapeForebet(sport, outputFile) {
    const url = SPORT_URLS[sport.toLowerCase()] || SPORT_URLS['football'];
    console.log(`🌐 Forebet ${sport}: ${url}`);
    
    let browser;
    
    try {
        // Opcje przeglądarki
        const launchOptions = {
            headless: 'new',  // Nowy headless mode
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--window-size=1920,1080',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            ]
        };
        
        console.log('🚀 Uruchamiam przeglądarkę...');
        browser = await puppeteer.launch(launchOptions);
        
        const page = await browser.newPage();
        
        // Ustaw viewport
        await page.setViewport({ width: 1920, height: 1080 });
        
        // Ustaw extra headers
        await page.setExtraHTTPHeaders({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        });
        
        console.log('🌐 Ładuję stronę...');
        await page.goto(url, { 
            waitUntil: 'networkidle2',
            timeout: 60000 
        });
        
        // Czekaj na potencjalny challenge
        console.log('⏳ Czekam na Cloudflare...');
        await delay(5000);
        
        // Symuluj człowieka
        await simulateHumanBehavior(page);
        
        // Kliknij consent
        await clickConsent(page);
        
        // Czekaj na content
        const hasContent = await waitForContent(page);
        
        if (!hasContent) {
            console.log('⚠️ Nie znaleziono treści, czekam jeszcze...');
            await delay(10000);
            await simulateHumanBehavior(page);
        }
        
        // Pobierz HTML
        const html = await page.content();
        
        // Sprawdź czy to prawdziwa strona
        const isChallenge = html.includes('loading-verifying') || 
                           html.includes('lds-ring') ||
                           html.includes('Checking your browser');
        
        const isForebet = html.includes('rcnt') || 
                         html.includes('forepr') ||
                         html.includes('tr_0');
        
        if (isChallenge && !isForebet) {
            console.log('❌ Cloudflare challenge nie został rozwiązany!');
            
            // Jeszcze jedna próba - czekaj dłużej
            console.log('⏳ Ostatnia próba - czekam 30 sekund...');
            await delay(30000);
            await simulateHumanBehavior(page);
            await clickConsent(page);
            
            const html2 = await page.content();
            
            if (html2.includes('rcnt') || html2.includes('tr_0')) {
                console.log('✅ Sukces po dodatkowym czekaniu!');
                fs.writeFileSync(outputFile, html2);
                console.log(`💾 Zapisano: ${outputFile} (${html2.length} znaków)`);
            } else {
                // Zapisz do debug
                fs.writeFileSync('forebet_challenge_debug.html', html2);
                console.log('❌ NIEPOWODZENIE - zapisano debug HTML');
                process.exit(1);
            }
        } else if (isForebet) {
            console.log(`✅ SUKCES! Strona Forebet załadowana (${html.length} znaków)`);
            fs.writeFileSync(outputFile, html);
            console.log(`💾 Zapisano: ${outputFile}`);
        } else {
            console.log('⚠️ Nieznana strona - zapisuję do analizy');
            fs.writeFileSync(outputFile, html);
        }
        
    } catch (error) {
        console.error(`❌ Błąd: ${error.message}`);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
            console.log('🔒 Przeglądarka zamknięta');
        }
    }
}

// Main
const sport = process.argv[2] || 'football';
const outputFile = process.argv[3] || 'forebet_output.html';

console.log('🔥 FOREBET PUPPETEER SCRAPER - STEALTH MODE 🔥');
console.log(`Sport: ${sport}`);
console.log(`Output: ${outputFile}`);
console.log('');

scrapeForebet(sport, outputFile)
    .then(() => {
        console.log('✅ Zakończono');
        process.exit(0);
    })
    .catch(err => {
        console.error(`❌ Fatal error: ${err.message}`);
        process.exit(1);
    });

# Fiskejournal (olundsfiske.se)
Denna webbapp förenar mina två passioner: programmering och fiske. Det här är ett rent hobbyprojekt för att lära mig mer om att skapa och lansera en full stack webbapp. Appen är designad för att logga mina fångster mer eller mindre automatiskt utifrån ett uppladdat foto från telefonen.

Utifrån datat i fotot hämtas fångstplats, aktuellt väder med mera från olika tjänster. OpenAI artbestämmer fisken automatiskt och allt sparas i databasen. Den kombinerar modern teknik med en kärlek för naturen och fisket.

Eftersom detta endast är i självlärande syfte för att skapa mig en bild över hur saker och ting hänger ihop så har jag inte lagt ner 100% i alla delar. När de varit "good enough" har jag stannat där. Därför går mycket att effektivisera eller förbättra, men för mig uppfyller den sitt syfte gott nog och jag lärde mig mycket på vägen. Med tiden kommer jag gå igenom koden lite mera. Det finns till exempel delar kvar som går att bryta ut i fler Vue-komponenter. Även websockets skulle gå att ge lite mer kärlek och mycket annat smått.  

Du kan se appen igång här: https://olundsfiske.se

## Flödet vid uppladdning av foto

När jag är inloggad visas en ikon för filuppladdning. Jag klickar på ikonen och väljer "Ta foto" (eller väljer ett befintligt från telefonen).

1. När fotot tas laddas det direkt upp till servern. Backend verifierar att det finns tidsstämpel och koordinater i fotot, samt att fotot inte redan finns.
2. Om servern accepterar fotot skickas det till Celery som påbörjar en task i bakgrunden.

### Bakgrundsuppgiften (Celery)

1. Bakgrundsuppgiften extraherar metadata (tidsstämpel och koordinater).
2. Koordinaterna skickas i ett anrop till Geonames API för att namnsätta platsen på vattnet där fotot är taget.
3. Koordinaterna används också i ett anrop till Weatherapi API för att hämta aktuell väderdata på platsen för fotot.
4. Orginalbilden konverteras till en liten bild (thumbnail) och en mediumbild som är 800px bred eller hög (beroende på orientering).
5. Mediumbilden konverteras till en Base64-sträng som skickas till OpenAI API som artbestämmer fisken på bilden.
6. Orginalbilden raderas från servern och de båda konverterade bilderna laddas upp och lagras på Amazon S3 och används för att visa bilderna på sidan.
7. När allt är klart sparas allting i databasen som en ny fisk.

### Administrationspanel

Sidan har en enklare administrationspanel där jag kan redigera objekten i databasen, om till exempel OpenAI inte lyckats artbestämma fisken. Jag kan även lägga in vikt, längd, vilket bete och så vidare om jag skulle vilja.

## Frontend

### Vue.js

För frontend har jag valt Vue.js. Det är ett välutvecklat JavaScript-ramverk, känt för sin flexibilitet och kraftfulla komponentbaserade arkitektur, vilket gör det idealiskt för att bygga dynamiska webbappar.

### TailwindCSS

Tailwind CSS är ett utility-first CSS-ramverk som används för att snabbt och enkelt skapa responsiva och anpassningsbara användargränssnitt. Tailwind är ett oerhört populärt ramverk med stort community.

### DaisyUI

DaisyUI är ett plugin för Tailwind CSS som tillhandahåller färdiga komponenter som är enkla att använda och anpassa. Det hjälper till att säkerställa en enhetlig design genom hela applikationen.

### Leaflet

Leaflet är ett JavaScript-bibliotek för att skapa interaktiva kartor. Det är snabbt och enkelt att använda, vilket gör det perfekt för att visa geospatial data i webbapplikationer.

## Backend

### Django Ninja

Django Ninja är ett ramverk för att bygga snabba REST-API:er med Django och Python. Det är enkelt att använda och kraftfullt. Med möjligheten att utnyttja Djangos lösning för autentisering "out of the box" gör detta till ett utmärkt val för min backend.

### PostgreSQL

PostgreSQL är en kraftfull objekt-relationsdatabas med öppen källkod. Jag valde PostgreSQL för dess robusthet, snabbhet och att det fungerar för himla fint tillsammans med Django och Pydantic.

### Celery

Celery är ett asynkront jobbkösystem som används för att hantera tidskrävande uppgifter i bakgrunden. Det hjälper till att hålla applikationen responsiv genom att flytta uppgifterna för bildhanteringen till bakgrundstasks.

### Redis

Redis är en snabb nyckel-värde-databashanterare som jag använder som en broker för Celery och för caching av data för att förbättra prestandan.

### NginX

NginX är en högpresterande webbserver och reverse proxy-server. Den används för att hantera inkommande webbtrafik och som en proxy mellan klienter och backend-servrar.

### Amazon S3

Amazon S3 är en skalbar lagringslösning från Amazon Web Services (AWS). Jag använder S3 för att lagra och leverera statiskt innehåll. Dels de uppladdade fotona, men även andra bilder som finns på sidan. S3 har hög tillgänglighet och prestanda.

### Docker

Allting körs i Docker för att ha isolerade containrar som enkelt kan flyttas mellan olika miljöer.


## Externa tjänster

### Weatherapi API

Weatherapi används för att hämta väderdata. Det används för att logga aktuella vädret vid fångsttillfället.

### Geonames API

Geonames API används för att utifrån koodinaterna i fotot hämta platsnamnet för vattnet där fisken fångasts.

### OpenAI API

OpenAI API används för att artbestämma fisken på fotot som jag laddar upp.

### OpenStreetMap

Kartan som används är OpenStreetMap, en öppen och lättarbetad karta.

## Licens

Denna app är licensierad under MIT License - se filen [LICENSE](LICENSE) för detaljer.

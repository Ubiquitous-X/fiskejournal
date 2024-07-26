<template>
  <div class="flex justify-center mt-2">
    <div class="w-full lg:w-3/4 p-8 rounded-lg">
      <router-link to="/" exact-active-class="active" class="btn btn-ghost mb-4">
        <i class="fas fa-arrow-left mr-2"></i>
        Tillbaka
      </router-link>

      <!-- Om denna webbapp -->
      <section class="mb-8 bg-neutral text-neutral-content p-4 rounded-2xl">
        <div class="container px-6 py-10 mx-auto">
          <div class="lg:flex lg:items-center">
            <div class="w-full space-y-6">
              <h1 class="text-3xl font-semibold lg:text-4xl">Om denna webbapp</h1>
              <p class="text-base mb-4">
                Det här är ett rent hobbyprojekt för att utforska skapandet av en full stack webbapp för personligt bruk med ett javascript framework för frontend och ett api som backend. Tidigare har jag bara skapat saker med rena Python-ramverk som Django eller Flask och deras respektive templatingsystem. Sidan är helt responsiv och gör sig bra även på små skärmar, mycket tack vare att TailwindCSS är "mobility first" och innehåller bra stöd för detta.
              </p>
              <p class="text-base mb-4">
                Eftersom detta endast är i självlärande syfte för att skapa mig en bild över hur många och komplexa komponenter en full stack webbapp egentligen består av så har jag inte lagt ner 100% i alla delar. När de varit "good enough" har jag stannat där. Därför går mycket att effektivisera eller förbättra, men för mig uppfyller den sitt syfte gott nog och jag lärde mig mycket på vägen.
              </p>
              <p class="text-base mb-4">
                Vem som helst är fri att använda koden och sätta upp sin egen installation av denna webbapp. Med tiden kommer jag förmodligen gå igenom koden lite nogrannare och se vad som går att göra. Det finns till exempel delar kvar som går att bryta ut i fler Vue-komponenter. Även websockets skulle gå att ge lite mer kärlek och inte minst bättre kommentering av koden.
              </p>
            </div>
          </div>
          <!-- DaisyUI Collapse Component -->
          <div tabindex="0" class="collapse collapse-plus border-neutral-content bg-neutral text-neutral-content border mt-6 rounded-lg">
            <div class="collapse-title text-xl font-bold">Flödet vid uppladdning av foto</div>
            <div class="collapse-content text-base">
              <ul class="list-disc list-inside space-y-2">
                <li>När jag är inloggad visas en ikon för filuppladdning. Jag klickar på ikonen och väljer "Ta foto" (eller väljer ett befintligt från telefonen).</li>
                <li>När fotot tas laddas det direkt upp till servern. Backend verifierar att det finns tidsstämpel och koordinater i fotot, samt att fotot inte redan finns.</li>
                <li>Om servern accepterar fotot skickas det till Celery som påbörjar en task i bakgrunden.</li>
              </ul>
              <h3 class="text-lg font-bold mt-4 mb-4">Bakgrundsuppgiften (Celery)</h3>
              <ul class="list-disc list-inside space-y-2">
                <li>Bakgrundsuppgiften extraherar metadata (tidsstämpel och koordinater).</li>
                <li>Koordinaterna skickas i ett anrop till Geonames API för att namnsätta platsen på vattnet där fotot är taget.</li>
                <li>Koordinaterna används också i ett anrop till Weatherapi API för att hämta aktuell väderdata på platsen för fotot.</li>
                <li>Orginalbilden konverteras till en liten bild (thumbnail) och en mediumbild som är 800px bred eller hög (beroende på orientering).</li>                
                <li>Mediumbilden konverteras till en Base64-sträng som skickas till OpenAI API som artbestämmer fisken på bilden.</li>
                <li>Orginalbilden raderas från servern och de båda konverterade bilderna laddas upp och lagras på Amazon S3 och används för att visa bilderna på sidan.</li>
                <li>När allt är klart sparas allting i databasen som en ny fisk.</li>
              </ul>
              <h3 class="text-lg font-bold mt-4 mb-4">Administrationspanel</h3>
              <p>Sidan har en enklare administrationspanel där jag kan redigera objekten i databasen, om till exempel OpenAI inte lyckats artbestämma fisken. Jag kan även lägga in vikt, längd, vilket bete och så vidare om jag skulle vilja.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Frontend -->
      <section class="bg-base-100 shadow-xl mb-8">
        <div class="container px-6 py-10 mx-auto">
          <div class="lg:flex lg:items-center">
            <div class="w-full lg:w-1/2 space-y-12">
              <div>
                <h2 class="text-3xl font-semibold text-gray-800 lg:text-4xl dark:text-white">Frontend</h2>
                <div class="mt-2">
                  <span class="inline-block w-40 h-1 rounded-full bg-blue-500"></span>
                  <span class="inline-block w-3 h-1 ml-1 rounded-full bg-blue-500"></span>
                  <span class="inline-block w-1 h-1 ml-1 rounded-full bg-blue-500"></span>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/vue-logo.png" alt="Vue Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Vue.js</h1>
                  <p class="mt-3 text-base-content">
                    För frontend har jag valt Vue.js. Det är ett välutvecklat JavaScript-ramverk, känt för sin flexibilitet och kraftfulla komponentbaserade arkitektur, vilket gör det idealiskt för att bygga dynamiska webbappar.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/tailwind-logo.png" alt="TailwindCSS Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">TailwindCSS</h1>
                  <p class="mt-3 text-base-content">
                    Tailwind CSS är ett utility-first CSS-ramverk som används för att snabbt och enkelt skapa responsiva och anpassningsbara användargränssnitt. Tailwind är ett oerhört populärt ramverk med stort community.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/daisyui-logo.png" alt="DaisyUI Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">DaisyUI</h1>
                  <p class="mt-3 text-base-content">
                    DaisyUI är ett plugin för Tailwind CSS som tillhandahåller färdiga komponenter som är enkla att använda och anpassa. Det hjälper till att säkerställa en enhetlig design genom hela applikationen.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/leaflet-logo.png" alt="Leaflet Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Leaflet</h1>
                  <p class="mt-3 text-base-content">
                    Leaflet är ett JavaScript-bibliotek för att skapa interaktiva kartor. Det är snabbt och enkelt att använda, vilket gör det perfekt för att visa geospatial data i webbapplikationer.
                  </p>
                </div>
              </div>
            </div>
            <div class="hidden lg:flex lg:items-center lg:w-1/2 lg:justify-center">
              <img class="w-[28rem] h-[28rem] object-cover xl:w-[32rem] xl:h-[32rem] rounded-full" src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/developmentdesk.webp" alt="Frontend Workspace Image">
            </div>
          </div>
        </div>
      </section>

      <!-- Backend -->
      <section class="bg-base-100 shadow-xl mb-8">
        <div class="container px-6 py-10 mx-auto">
          <div>
            <div>
              <h2 class="text-3xl font-semibold text-gray-800 lg:text-4xl dark:text-white">Backend</h2>
              <div class="mt-2">
                <span class="inline-block w-40 h-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-3 h-1 ml-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-1 h-1 ml-1 rounded-full bg-red-500"></span>
              </div>
            </div>
            <div class="space-y-12 mt-6">
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/django-logo.svg" alt="Django Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Django Ninja</h1>
                  <p class="mt-3 text-base-content">
                    Django Ninja är ett ramverk för att bygga snabba REST-API:er med Django och Python. Det är enkelt att använda och kraftfullt. Med möjligheten att utnyttja Djangos lösning för autentisering "out of the box" gör detta till ett utmärkt val för min backend.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/postgresql-logo.svg" alt="PostgreSQL Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">PostgreSQL</h1>
                  <p class="mt-3 text-base-content">
                    PostgreSQL är en kraftfull objekt-relationsdatabas med öppen källkod. Jag valde PostgreSQL för dess robusthet, snabbhet och att det fungerar för himla fint tillsammans med Django och Pydantic.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/celery-logo.svg" alt="Celery Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Celery</h1>
                  <p class="mt-3 text-base-content">
                    Celery är ett asynkront jobbkösystem som används för att hantera tidskrävande uppgifter i bakgrunden. Det hjälper till att hålla applikationen responsiv genom att flytta uppgifterna för bildhanteringen till bakgrundstasks.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/redis-logo.svg" alt="Redis Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Redis</h1>
                  <p class="mt-3 text-base-content">
                    Redis är en snabb nyckel-värde-databashanterare som jag använder som en broker för Celery och för caching av data för att förbättra prestandan.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/nginx-logo.svg" alt="NginX Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">NginX</h1>
                  <p class="mt-3 text-base-content">
                    NginX är en högpresterande webbserver och reverse proxy-server. Den används för att hantera inkommande webbtrafik och som en proxy mellan klienter och backend-servrar.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/docker-logo.svg" alt="Docker Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Docker</h1>
                  <p class="mt-3 text-base-content">
                    Docker är en plattform för att utveckla, leverera och köra applikationer i isolerade containrar. Det gör det enkelt att hantera beroenden och säkerställa att applikationen fungerar konsekvent oavsett var den körs.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/aws-logo.svg" alt="Amazon S3 Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <h1 class="text-2xl font-semibold">Amazon S3</h1>
                  <p class="mt-3 text-base-content">
                    Amazon S3 är en skalbar lagringslösning från Amazon Web Services (AWS). Jag använder S3 för att lagra och leverera statiskt innehåll. Dels de uppladdade fotona, men även andra bilder som finns på sidan. S3 har hög tillgänglighet och prestanda.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Infrastruktur och Övrigt -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <section class="bg-base-100 p-4 rounded-lg">
          <div class="container px-6 py-10 mx-auto">
            <div>
              <h2 class="text-3xl font-semibold text-gray-800 lg:text-4xl dark:text-white">Infrastruktur</h2>
              <div class="mt-2">
                <span class="inline-block w-40 h-1 rounded-full bg-blue-500"></span>
                <span class="inline-block w-3 h-1 ml-1 rounded-full bg-blue-500"></span>
                <span class="inline-block w-1 h-1 ml-1 rounded-full bg-blue-500"></span>
              </div>
            </div>
            <div class="space-y-6 mt-6">
              <div>
                <h3 class="text-xl font-bold mb-2">Manjaro Linux</h3>
                <p class="text-base mb-4">
                  För utveckling kör jag Manjaro Linux. Det är en Linuxdistribution baserad på Arch Linux, känd för sin renhet, snabbhet och kraftfulla pakethantering.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">Git</h3>
                <p class="text-base mb-4">
                  Jag använder Git för versionshantering, vilket gör det möjligt att enkelt spåra ändringar i koden.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">Stagingserver i VirtualBox</h3>
                <p class="text-base mb-4">
                  Som testserver kör jag en Ubuntu 24.04 i VirtualBox på min utvecklingsdator.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">Produktionsserver DigitalOcean</h3>
                <p class="text-base mb-4">
                  Produktionsservern ligger på en VPS på DigitalOcean som kör Ubuntu 24.04.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section class="bg-base-100 p-4 rounded-lg">
          <div class="container px-6 py-10 mx-auto">
            <div>
              <h2 class="text-3xl font-semibold text-gray-800 lg:text-4xl dark:text-white">Externa tjänster</h2>
              <div class="mt-2">
                <span class="inline-block w-40 h-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-3 h-1 ml-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-1 h-1 ml-1 rounded-full bg-red-500"></span>
              </div>
            </div>
            <div class="space-y-6 mt-6">
              <div>
                <h3 class="text-xl font-bold mb-2">Weatherapi API</h3>
                <p class="text-base mb-4">
                  Weatherapi används för att hämta väderdata. Det används för att logga aktuella vädret vid fångsttillfället.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">Geonames API</h3>
                <p class="text-base mb-4">
                  Geonames API används för att utifrån koodinaterna i fotot hämta platsnamnet för vattnet där fisken fångasts.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">OpenAI API</h3>
                <p class="text-base mb-4">
                  OpenAI API används för att artbestämma fisken på fotot som jag laddar upp.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2">OpenStreetMap</h3>
                <p class="text-base mb-4">
                  Kartan som används är OpenStreetMap, en öppen och lättarbetad karta.
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Github -->
      <section class="flex justify-center items-center mt-8">
        <a href="https://github.com/Ubiquitous-X/fiskejournal" target="_blank" class="text-gray-800 dark:text-white text-xl font-semibold">
          <i class="fab fa-github mr-2"></i>Github
        </a>
      </section>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
  name: "AboutView",
  setup() {
    const setCanonicalUrl = () => {
      const existingCanonicalLink = document.querySelector("link[rel='canonical']");
      if (existingCanonicalLink) {
        existingCanonicalLink.remove();
      }
      const link = document.createElement('link');
      link.setAttribute('rel', 'canonical');
      link.setAttribute('href', 'https://olundsfiske.se/om');
      document.head.appendChild(link);
    };

    onMounted(() => {
      setCanonicalUrl();
    });
  }
});
</script>

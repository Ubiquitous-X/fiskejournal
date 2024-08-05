<template>
  <div class="flex justify-center">
    <div class="w-full lg:w-3/4 p-6 md:p-8 rounded-lg">
      <router-link to="/" exact-active-class="active" class="btn btn-ghost mb-2">
        <i class="fas fa-arrow-left mr-2"></i>
        Tillbaka
      </router-link>

      <!-- Om denna webbapp -->
      <section class="mb-8 bg-neutral text-neutral-content p-4 rounded-2xl">
        <div class="container lg:px-6 md:py-6 mx-auto">
          <div class="lg:flex lg:items-center">
            <div class="w-full space-y-6">
              <h1 class="text-2xl lg:text-3xl font-semibold">Om denna webbapp</h1>
              <p class="text-base mb-4">
                Det här är ett rent hobbyprojekt för att utforska skapandet av en full stack webbapp för personligt bruk med ett JavaScript-ramverk för frontend och ett API som backend. Tidigare har jag bara skapat saker med rena Python-ramverk som Django eller Flask och deras respektive templatingsystem. Sidan är helt responsiv och fungerar bra även på små skärmar, mycket tack vare att TailwindCSS är "mobility first" och innehåller bra stöd för detta.
              </p>
              <p class="text-base mb-4">
                Eftersom detta endast är i självlärande syfte för att skapa mig en bild av hur många och komplexa komponenter en full stack webbapp egentligen består av, har jag inte lagt ner 100% på alla delar. När de varit "good enough" har jag stannat där. Därför går mycket att effektivisera eller förbättra, men för mig uppfyller den sitt syfte gott nog och jag har lärt mig mycket på vägen.
              </p>
              <p class="text-base mb-4">
                Vem som helst är fri att använda koden och sätta upp sin egen installation av denna webbapp. Med tiden kommer jag förmodligen gå igenom koden lite noggrannare och se vad som går att göra. Det finns till exempel delar kvar som går att bryta ut i fler Vue-komponenter. Även websockets skulle gå att ge lite mer kärlek och inte minst bättre kommentering av koden. Högt på listan står dock att lägga till enhetstester för både frontend och backend i byggflödet.
              </p>
            </div>
          </div>
          <!-- DaisyUI Collapse Component -->
          <div tabindex="0" class="collapse collapse-plus border-neutral-content bg-neutral text-neutral-content border mt-6 rounded-lg">
            <div class="collapse-title text-lg md:text-xl font-bold">Flödet vid uppladdning av foto</div>
            <div class="collapse-content text-base">
              <ul class="list-disc list-inside space-y-2">
                <li>När jag är inloggad visas en ikon för filuppladdning. Jag klickar på ikonen och väljer "Ta foto" (eller väljer ett befintligt från telefonen).</li>
                <li>När fotot tas laddas det direkt upp till servern. Backend verifierar att det finns tidsstämpel och koordinater i fotot, samt att fotot inte redan finns.</li>
                <li>Om servern accepterar fotot skickas det till Celery som påbörjar en task i bakgrunden.</li>
              </ul>
              <h3 class="text-lg font-bold mt-4 mb-4">Bakgrundsuppgiften (Celery)</h3>
              <ul class="list-disc list-inside space-y-2">
                <li>Bakgrundsuppgiften extraherar metadata (tidsstämpel och koordinater).</li>
                <li>Koordinaterna skickas i ett anrop till Geonames API för att namnge platsen på vattnet där fotot är taget.</li>
                <li>Koordinaterna används också i ett anrop till Weatherapi API för att hämta aktuell väderdata på platsen för fotot.</li>
                <li>Originalbilden konverteras till en liten bild (thumbnail) och en mediumbild som är 800px bred eller hög (beroende på orientering).</li>                
                <li>Mediumbilden konverteras till en Base64-sträng som skickas till OpenAI API för att artbestämma fisken på bilden.</li>
                <li>Originalbilden raderas från servern och de båda konverterade bilderna laddas upp och lagras på Amazon S3 för att visas på sidan.</li>
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
        <div class="container px-4 md:px-6 py-6 md:py-10 mx-auto">
          <div class="lg:flex lg:items-center">
            <div class="w-full lg:w-1/2 space-y-12">
              <div>
                <h2 class="text-3xl font-semibold lg:text-4xl">Frontend</h2>
                <div class="mt-2">
                  <span class="inline-block w-40 h-1 rounded-full bg-blue-500"></span>
                  <span class="inline-block w-3 h-1 ml-1 rounded-full bg-blue-500"></span>
                  <span class="inline-block w-1 h-1 ml-1 rounded-full bg-blue-500"></span>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/vue-logo.png" alt="Vue Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://vuejs.org/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Vue.js</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    För frontend har jag valt Vue.js. Det är ett välutvecklat JavaScript-ramverk, känt för sin flexibilitet och kraftfulla komponentbaserade arkitektur, vilket gör det idealiskt för att bygga dynamiska webbappar.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/tailwind-logo.png" alt="TailwindCSS Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://tailwindcss.com/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>TailwindCSS</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    TailwindCSS är ett utility-first CSS-ramverk som används för att snabbt och enkelt skapa responsiva och anpassningsbara användargränssnitt. Tailwind är ett oerhört populärt ramverk med ett stort community.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/daisyui-logo.png" alt="DaisyUI Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://daisyui.com/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>DaisyUI</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    DaisyUI är ett plugin för TailwindCSS som tillhandahåller färdiga komponenter som är enkla att använda och anpassa. Det hjälper till att säkerställa en enhetlig design genom hela applikationen.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/leaflet-logo.png" alt="Leaflet Logo" class="w-12 h-12 md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://leafletjs.com/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Leaflet</h1>
                  </a>
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
        <div class="container px-4 md:px-6 py-10 mx-auto">
          <div>
            <div>
              <h2 class="text-3xl font-semibold lg:text-4xl">Backend</h2>
              <div class="mt-2">
                <span class="inline-block w-40 h-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-3 h-1 ml-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-1 h-1 ml-1 rounded-full bg-red-500"></span>
              </div>
            </div>
            <div class="space-y-12 mt-14">
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/django-logo.svg" alt="Django Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://django-ninja.dev/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Django Ninja</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    Django Ninja är ett ramverk för att bygga snabba asynkrona REST-API:er med Django och Python. Med inbyggt stöd för autentisering "out of the box" gör detta till ett utmärkt val för min backend. I backend körs API:et på Daphne, en asynkron ASGI-server med stöd för websockets.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/postgresql-logo.svg" alt="PostgreSQL Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://www.postgresql.org/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>PostgreSQL</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    PostgreSQL är en kraftfull objekt-relationsdatabas med öppen källkod. Jag valde PostgreSQL för dess robusthet, snabbhet och att det helt enkelt fungerar så himla fint tillsammans med Django och Pydantic.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/celery-logo.svg" alt="Celery Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://docs.celeryq.dev/en/stable/index.html" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Celery</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    Celery är ett asynkront jobbkösystem som används för att hantera tidskrävande uppgifter i bakgrunden. Det hjälper till att hålla applikationen responsiv genom att flytta uppgifterna för bildhanteringen till bakgrundstasks.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/redis-logo.svg" alt="Redis Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://redis.io/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Redis</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    Redis är en snabb nyckel-värde-databashanterare som jag använder som en broker för Celery och för caching av data för att förbättra prestandan. Redis används även med websockets för att skicka meddelanden till frontend.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/nginx-logo.svg" alt="NginX Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://nginx.org/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>NginX</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    NginX är en högpresterande webbserver och reverse proxy-server. Den används för att hantera inkommande webbtrafik och som en proxy mellan klienter och backend-servrar. För SSL-kryptering använder jag certifikat från Let's Encrypt. Framför NginX sitter iptables och fail2ban för att blockera oönskad trafik.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/docker-logo.svg" alt="Docker Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://www.docker.com/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Docker</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    Docker är en plattform för att utveckla, leverera och köra applikationer i isolerade containrar. Det gör det enkelt att hantera beroenden och säkerställa att applikationen fungerar konsekvent oavsett var den körs.
                  </p>
                </div>
              </div>
              <div class="md:flex md:items-start md:-mx-4">
                <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/aws-logo.svg" alt="Amazon S3 Logo" class="w-16 h-auto rounded-lg md:mx-4">
                <div class="mt-4 md:mx-4 md:mt-0">
                  <a href="https://aws.amazon.com/s3/" target="_blank" rel="noopener noreferrer" class="text-2xl font-semibold text-inherit hover:text-inherit focus:text-inherit">
                    <h1>Amazon S3</h1>
                  </a>
                  <p class="mt-3 text-base-content">
                    Amazon S3 är en skalbar lagringslösning från Amazon Web Services (AWS). Jag använder S3 för lagring av de uppladdade fotona och även för lagring av andra statiska bilder på sidan. Det är en mycket stabil CDN med hög prestanda.
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
          <div class="container px-4 md:px-6 md:py-10 mx-auto">
            <div>
              <h2 class="text-3xl font-semibold lg:text-4xl">Infrastruktur</h2>
              <div class="mt-2">
                <span class="inline-block w-40 h-1 rounded-full bg-blue-500"></span>
                <span class="inline-block w-3 h-1 ml-1 rounded-full bg-blue-500"></span>
                <span class="inline-block w-1 h-1 ml-1 rounded-full bg-blue-500"></span>
              </div>
            </div>
            <div class="space-y-6 mt-6">
              <div>
                <a href="https://manjaro.org/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>Manjaro Linux</h3>
                </a>
                <p class="text-base mb-4">
                  Som utvecklingsmiljö kör jag Manjaro Linux. Det är en Linuxdistribution baserad på Arch Linux, känd för sin snabbhet och kraftfulla pakethantering.
                </p>
              </div>
              <div>
                <a href="https://github.com/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>Git/Github</h3>
                </a>
                <p class="text-base mb-4">
                  Jag använder Git för versionshantering, med Github för kodlagring. Det gör det enkelt att jobba med olika grenar och spåra ändringar i koden.
                </p>
              </div>
              <div>
                <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>CI/CD pipeline</h3>
                </a>
                <p class="text-base mb-4">
                  Github Actions används som CI/CD pipeline. Containrarna byggs automatiskt vid kodändring och pushas ut till produktion via Docker Hub.
                </p>
              </div>
              <div>
                <a href="https://virtualbox.org/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>Stagingserver i VirtualBox</h3>
                </a>
                <p class="text-base mb-4">
                  Som testserver kör jag en installation av Ubuntu 24.04 i VirtualBox på min utvecklingsdator. Den hostar en produktionsmiljö på mitt lokala nätverk.
                </p>
              </div>
              <div>
                <a href="https://www.digitalocean.com/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>Produktionsserver DigitalOcean</h3>
                </a>
                <p class="text-base mb-4">
                  Produktionsservern körs på Ubuntu 24.04 och ligger på en VPS hos DigitalOcean. Där hanteras även DNS-konfigurationen för domänen.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section class="bg-base-100 p-4 rounded-lg">
          <div class="container px-4 md:px-6 md:py-10 mx-auto">
            <div>
              <h2 class="text-3xl font-semibold lg:text-4xl">Externa tjänster</h2>
              <div class="mt-2">
                <span class="inline-block w-40 h-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-3 h-1 ml-1 rounded-full bg-red-500"></span>
                <span class="inline-block w-1 h-1 ml-1 rounded-full bg-red-500"></span>
              </div>
            </div>
            <div class="space-y-6 mt-6">
              <div>
                <a href="https://www.weatherapi.com/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>Weatherapi API</h3>
                </a>
                <p class="text-base mb-4">
                  Weatherapi API används för att hämta väderdata. Det används för att logga det aktuella vädret vid fångsttillfället och visa väderdata på startsidan.
                </p>
              </div>
              <div>
                <a href="https://www.geonames.org/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>Geonames API</h3>
                </a>
                <p class="text-base mb-4">
                  Geonames API används för att utifrån koordinaterna i fotot hämta platsnamnet för vattnet där fisken fångats.
                </p>
              </div>
              <div>
                <a href="https://platform.openai.com/docs/overview" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>OpenAI API</h3>
                </a>
                <p class="text-base mb-4">
                  OpenAI API används för att artbestämma fisken på fotot som laddas upp. Det är samma API som ChatGPT använder.
                </p>
              </div>
              <div>
                <a href="https://www.openstreetmap.org/" target="_blank" rel="noopener noreferrer" class="text-xl font-bold mb-2 text-inherit hover:text-inherit focus:text-inherit">
                  <h3>OpenStreetMap</h3>
                </a>
                <p class="text-base mb-4">
                  Kartan som används är OpenStreetMap, en öppen och lättanvänd karta med god dokumentation och ett kreativt community.
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

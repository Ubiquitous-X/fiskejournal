<template>
  <div class="block md:hidden">
    <InfoPanelSmallScreen />
  </div>
  <div class="flex justify-center">
    <div class="w-full lg:w-3/4 p-7 md:p-8">      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">        
        <div>
          <h1 class="text-xl md:text-2xl lg:text-3xl font-semibold mb-4">Välkommen till Ölunds Fiske!</h1>
          <p class="text-base mb-4">
            Ölunds Fiske är en webbapp som jag skapat för att automatiskt logga mina fångster i realtid på mina fisketurer. 
            Jag fiskar främst i Mälaren och mindre sjöar i och runt Strängnäs, oftast från min upplåsbara fiskekajak, men också tillsammans med vänner. 
            Det jag är ute efter att fånga är abborre, gös och gädda.
          </p>
          <p class="text-base mb-4">
            Detta är ett rent hobbyprojekt för att lära mig mer om att skapa och lansera en full stack webbapp och kombinera mina två passioner; programmering och fiske.
          </p>
          <p class="text-base mb-4">
            När jag fångar en fisk, fotar jag den. Fotot laddas automatiskt upp till servern och utifrån datat i fotot hämtas fångstplats, koordinater till kartan, aktuellt väder med mera från olika tjänster.
            OpenAI artbestämmer fisken automatiskt och allt sparas i databasen. Detta kombinerar modern teknik med en kärlek för naturen och fisket.
          </p>
          <p class="text-base mb-4">
            Mathias Ölund
          </p>
          <p class="text-sm mb-4">
            <i class="opacity-70">Läs mer om <router-link to="/om" class="text-primary underline">tekniken bakom appen</router-link> eller 
               se koden på <a href="https://github.com/Ubiquitous-X/fiskejournal" class="text-primary underline">Github</a>.
            </i>
          </p>
          <div class="flex space-x-4 mt-8">
            <router-link to="/fiskar" class="btn btn-primary btn-sm">
              <i class="fas fa-fish mr-1"></i>Alla fiskar
            </router-link>
            <router-link to="/karta" class="btn btn-primary btn-sm">
              <i class="fas fa-map mr-1"></i>Se karta
            </router-link>
          </div>
        </div>
        <div class="flex justify-center items-center">
          <div class="card card-compact bg-base-100 w-full lg:w-2/3 shadow-xl">
            <figure>
              <img src="https://fiskeapp.s3.eu-north-1.amazonaws.com/assets/kajak_profil.jpg" alt="Kajak" />
            </figure>
            <div class="card-body">
              <div class="flex flex-col lg:flex-row lg:items-center">
                <h2 class="card-title lg:mt-0.5">The battleship</h2>
                <span class="text-base font-normal italic lg:ml-2 mb-2 lg:mb-0">Intex Excursion Pro K2</span>
              </div>
              <p>
                <span class="font-bold">Gäddpåk:</span> Shimano Forcemaster 270H
              </p>
              <p>
                <span class="font-bold">Main gun:</span> Savage Gear SG4 6"6"
              </p>
              <p>
                <span class="font-bold">Light armament:</span> Shimano Forcemaster 165UL
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted } from 'vue';
import InfoPanelSmallScreen from '@/components/InfoPanelSmallScreen.vue';

export default defineComponent({
  name: "HomeView",
  components: {
    InfoPanelSmallScreen
  },
  setup() {
    const setCanonicalUrl = () => {
      const existingCanonicalLink = document.querySelector("link[rel='canonical']");
      if (existingCanonicalLink) {
        existingCanonicalLink.remove();
      }
      const link = document.createElement('link');
      link.setAttribute('rel', 'canonical');
      link.setAttribute('href', 'https://olundsfiske.se');
      document.head.appendChild(link);
    };

    onMounted(() => {
      setCanonicalUrl();
    });
  }
});
</script>


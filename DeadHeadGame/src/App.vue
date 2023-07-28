<template>
  <div class="surface-ground min-h-screen px-4 py-8 md:px-6 lg:px-8">
    <Toast/>
    <div class="shadow-2 border-round surface-card px-4 md:px-6 py-6">
      <div class="mb-5 font-bold text-6xl text-900">Grateful Dead Guesser</div>
      <p class="text-700 text-3xl mt-0 mb-6">Test your Grateful Dead knowledge by guessing the year of the concert</p>

      <div class="w-full flex justify-content-center flex-wrap">
        <Button v-if='song == null' rounded class='mb-4 w-3' label="Play" @click="get_song()" :loading="loading"></Button>
      </div>

      <div v-if="song != null" class="w-full flex justify-content-center flex-wrap">
        <audio class="w-6" controls>
          <source :src="song.song_url" type="audio/mpeg">
        </audio>
        <Button class="ml-3" icon="pi pi-refresh" rounded outlined aria-label="Filter" v-tooltip="'Get a new song'"
          @click="get_song()" />
        <Button class="ml-3" icon="pi pi-exclamation-circle" severity="warning" rounded outlined aria-label="Filter"
          v-tooltip="'Report a broken song'" @click="report.dialog = true" />
      </div>
      <div v-if="song != null" class="w-full flex justify-content-center flex-wrap mt-3">
        <InputText class="ml-3" type="text" placeholder="Enter Year" v-model="guess.year" />
        <Button class='ml-3' label="Submit" @click="guess_song()" />
      </div>

      <Dialog v-model:visible="report.dialog" appendTo="body" :modal="true" :breakpoints="{ '960px': '75vw', '640px': '100vw' }" :style="{ width: '60vw' }" :showHeader="false">
        <section class="flex flex-column w-full mt-4">
          <div class="flex w-full justify-content-between mb-4">
            <span class="w-4rem h-4rem border-circle flex justify-content-center align-items-center bg-yellow-100"><i
                class="pi pi-exclamation-circle text-yellow-700 text-4xl"></i></span>
            <Button type="button" icon="pi pi-times"
              class="p-button-rounded p-button-secondary p-button-text align-self-start"
              @click="report.dialog = false"></Button>
          </div>
          <p class="font-semibold text-xl mt-0 mb-2 text-900">Report Song</p>
          <p class="font-normal text-base mt-0 mb-3 text-600">Flag song as corrupt or invalid </p>
          <Dropdown :options="report.options" v-model="report.selected" optionLabel="name" appendTo="body" placeholder="Reason" styleClass="w-full border-round-lg"></Dropdown>
        </section>
        <template #footer>
          <div class="pt-3 flex">
            <Button @click="report.dialog = false" label="Cancel" class="p-button-text flex-grow-1"></Button>
            <Button @click="report_song()" label="Submit" class="flex-grow-1"></Button>
          </div>
        </template>
      </Dialog>

      <Dialog v-model:visible="result.dialog" appendTo="body" :modal="true" :breakpoints="{ '960px': '75vw', '640px': '100vw' }" :style="{ width: '60vw' }" :showHeader="false">
        <div class="flex flex-column align-items-center my-4">
          <span v-if="guess.year == song.year"
            class="flex align-items-center justify-content-center bg-cyan-100 text-cyan-800 mr-3 border-circle mb-3"
            style="width:64px;height:64px">
            <i class="pi pi-check text-5xl"></i>
          </span>
          <span v-if="guess.year != song.year"
            class="flex align-items-center justify-content-center bg-red-100 text-red-800 mr-3 border-circle mb-3"
            style="width:64px;height:64px">
            <i class="pi pi-times text-5xl"></i>
          </span>
          <div v-if="guess.year == song.year" class="font-bold text-2xl text-900">You are a true deadhead. {{ guess.year }}
            is correct!</div>
          <div v-if="guess.year != song.year" class="font-bold text-2xl text-900">Good guess! {{ guess.year }} is about {{
            Math.abs(song.year - guess.year) }} {{ (Math.abs(song.year - guess.year) > 1) ? "years" : "year" }} off.</div>
        </div>
        <!-- <div class="text-900 font-medium mb-2 text-xl">{{ song.title }}</div> -->
        <div class="flex mb-4 flex-column lg:flex-row">
          <div class="surface-50 p-3 flex-auto mx-0 my-3 lg:my-0">
            <div class="text-600 mb-3">Concert</div>
            <span class="text-blue-600 font-medium text-xl">{{ song.concert_title }}</span>
          </div>
        </div>
        <div class="flex mb-4 flex-column lg:flex-row">
          <div class="surface-50 p-3 flex-auto">
            <div class="text-600 mb-3">Song</div>
            <span class="text-blue-600 font-medium text-xl">{{ song.song_title }}</span>
          </div>
          <div class="surface-50 p-3 flex-auto mx-0 my-3 lg:my-0 lg:mx-3">
            <div class="text-600 mb-3">Year</div>
            <span class="text-blue-600 font-medium text-xl">{{ song.year }}</span>
          </div>
          <div class="surface-50 p-3 flex-auto">
            <div class="text-600 mb-3">Location</div>
            <span class="text-blue-600 font-medium text-xl">{{ song.coverage }}</span>
          </div>
        </div>
        <template #footer>
          <div class="flex justify-content-center">
            <Button icon="pi pi-refresh" @click="play_again()" label="Play Again" class="w-4 ml-2"></Button>
            <Button class="" icon="pi pi-exclamation-circle" severity="warning" rounded outlined aria-label="Filter" style="width: 3rem" v-tooltip="'Report a broken song'" @click="report.dialog = true" />
          </div>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      song: null,
      loading: false,
      guess: {
        submitted: false,
        year: null,
      },
      result: {
        dialog: false,
      },
      report: {
        options: [{ name: 'Too much static', value: 'Static' }, { name: 'Not a song', value: 'NonSong' }, {name: 'Other', value:'Other'}],
        selected: {},
        dialog: false
      }
    };
  },
  methods: {
    get_song() {
      let _self = this;
      _self.loading = true;
      _self.song = null;
      axios({
        url: "/song",
        method: "get",
      })
        .then(function (response) {
          _self.song = response.data
        })
        .catch(function (error) {
          console.log(error)
        })
        .finally(function () {
          _self.loading = false
        });
    },
    report_song() {
      let _self = this;
      let data = {
        "corrupted": _self.report.selected.value
      }
      axios({
        url: "/song/"+ _self.song.song_id,
        method: "PUT",
        data: data,
      })
        .then(function (response) {
          console.log(response)
          _self.show_toast('info','Song reported', 'We will take it out of circulation')
        })
        .catch(function (error) {
          console.log(error)
        })
        .finally(function () {
          _self.report.dialog = false
        });
    },

    show_toast(severity, summary, detail){
      this.$toast.add({ severity: severity, summary: summary, detail: detail, life: 5000 });
    },

    guess_song() {
      let _self = this;
      if(_self.guess.submitted == false){
        // CODE TO UPLOAD GUESS TO GUESSES TABLE 
      }
      _self.guess.submitted = true;
      _self.result.dialog = true;
    },
    play_again() {
      let _self = this
      _self.result.dialog = false;
      _self.guess.submitted = false;
      _self.guess.year = null;
      _self.song = null;
      _self.get_song();
    }
  },
  mounted() { },
}
</script>

<style>
body {
  font-family: var(--font-family);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.box {
  background-color: var(--green-500);
  color: #ffffff;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 1rem;
  padding-bottom: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-weight: bold;
  box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12);
}

@keyframes my-fadein {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes my-fadeout {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}

.my-fadein {
  animation: my-fadein 150ms linear;
}

.my-fadeout {
  animation: my-fadeout 150ms linear;
}</style>
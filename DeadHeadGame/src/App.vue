<!-- https://dribbble.com/shots/20210947-Music-app-design-mobile-app -->
<template>
  <div>
    <div class="surface-ground min-h-screen px-4 py-8 md:px-6 lg:px-8" style="background:radial-gradient(69.84% 69.84% at 50% 100%, rgba(21, 101, 192, 0.15) 0%, rgba(255, 255, 255, 0) 100%);">
      <Toast />
      <h3 class="text-center font-bold text-3xl md:text-6xl text-black-alpha-80 mt-0 mb-4">Test your Grateful Dead knowledge <br/> <span style="background: linear-gradient(90deg, rgba(0, 209, 255, 1) 0%, rgba(255, 109, 232, 1) 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; -webkit-text-fill-color: transparent;">Grateful Dead Guesser</span></h3>

      <div class="w-full flex justify-content-center flex-wrap">
        <Button v-if='song == null' rounded class='mb-4 w-3' label="Play" @click="get_song()" :loading="loading"></Button>
      </div>

      <ul v-if="song != null" class="list-none p-0 m-0">
          <li class="">
              <div class="p-1 flex justify-content-center">
                <!-- <audio class="lg:w-6 md:w-10" controls>
                  <source :src="song.song_url" type="audio/mpeg">
                </audio> -->
                <!-- <Button icon="pi pi-refresh" text rounded aria-label="New Song" v-tooltip="'Get a new song'" @click="get_song()" /> -->
                <!-- <Button icon="pi pi-exclamation-circle" severity="warning" text rounded aria-label="Report Song" v-tooltip="'Report a broken song'" @click="report.dialog = true" /> -->
              </div>
          </li>
          <li class="">
              <div class="py-2 flex justify-content-center flex-wrap">
                <span class="p-float-label">
                  <div class="p-inputgroup flex-1">
                    <InputNumber id="guess-input" v-model="guess.year" inputId="withoutgrouping" :useGrouping="false" />
                    <Button class='lg:ml-3' label="Submit" @click="guess_song()" />
                  </div>
                  <label for="number-input">Enter year</label>
                </span>
              </div>
          </li>
      </ul>

      <Dialog v-model:visible="report.dialog" appendTo="body" :modal="true"
        :breakpoints="{ '960px': '75vw', '640px': '100vw' }" :style="{ width: '60vw' }" :showHeader="false">
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
          <Dropdown :options="report.options" v-model="report.selected" optionLabel="name" appendTo="body"
            placeholder="Reason" styleClass="w-full border-round-lg"></Dropdown>
        </section>
        <template #footer>
          <div class="pt-3 flex">
            <Button @click="report.dialog = false" label="Cancel" class="p-button-text flex-grow-1"></Button>
            <Button @click="report_song()" label="Submit" class="flex-grow-1"></Button>
          </div>
        </template>
      </Dialog>

      <Dialog v-model:visible="result.dialog" appendTo="body" :modal="true"
        :breakpoints="{ '960px': '75vw', '640px': '100vw' }" :style="{ width: '60vw' }" :showHeader="false">
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
          <div v-if="guess.year == song.year" class="font-bold text-2xl text-900">You are a true deadhead. {{ guess.year
          }}
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
            <Button icon="pi pi-refresh" @click="play_again()" label="Play Again" class=""></Button>
            <Button class="ml-2" icon="pi pi-exclamation-circle" severity="warning" text aria-label="Filter"  v-tooltip="'Report a broken song'" @click="report.dialog = true" />
          </div>
        </template>
      </Dialog>
      
    </div>
    <div v-if="song != null" class="mobile-player">
      <AudioPlayer :url="song.song_url"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AudioPlayer from './components/AudioPlayer.vue';
export default {
  components: { AudioPlayer },
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
        options: [{ name: 'Too much static', value: 'Static' }, { name: 'Not a song', value: 'NonSong' }, { name: 'Other', value: 'Other' }],
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
        url: "/song/" + _self.song.song_id,
        method: "PUT",
        data: data,
      })
        .then(function (response) {
          _self.show_toast('info', 'Song reported', 'We will take it out of circulation')
        })
        .catch(function (error) {
          console.log(error)
        })
        .finally(function () {
          _self.report.dialog = false
        });
    },

    show_toast(severity, summary, detail) {
      this.$toast.add({ severity: severity, summary: summary, detail: detail, life: 5000 });
    },

    guess_song() {
      let _self = this;
      if (_self.guess.submitted == false) {
        let data = {
          "song_id": _self.song.song_id,
          "guess": _self.guess.year,
          "correct": _self.guess.year == _self.song.year
        }
        axios({
          url: "/guess",
          method: "PUT",
          data: data,
        })
          .then(function (response) {
            _self.guess.submitted = true;
          })
          .catch(function (error) {
            console.log(error)
          })
          .finally(function () {
          });
      }
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

@media only screen and (max-width: 600px) {
  /* Throw the .mobile-player in here to make it only show up on mobile devices */
}

.mobile-player {
    background-color: #333;
    overflow: hidden;
    position: fixed;
    bottom: 0;
    width: 100%;
    border-radius: 15px 15px 0px 0px ;
    height: 20vh;
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
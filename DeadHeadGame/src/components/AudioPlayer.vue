<template>
  <div id="audio-player-container" class="p-3">
    
    <div class="grid mb-3">
        <div class="col-12">
            <!-- <div class="text-center p-3 border-round-sm bg-primary font-bold">12</div> -->
            <!-- <AudioPlayerVue :url="url" /> -->
            <div id="waveform"></div>
        </div>
    </div>

    <div class="grid">
        <div class="col-4 flex justify-content-center align-content-center">
            <!-- <div class="text-center p-3 border-round-sm bg-primary font-bold">4</div> -->
            <Button size="large" icon="pi pi-refresh" text severity="danger" rounded aria-label="New Song" v-tooltip="'Get a new song'" @click="get_song()" />
        </div>
        <div class="col-4 flex justify-content-center align-content-center">
          <Button v-if="playing == false" icon="pi pi-play" rounded aria-label="Play" @click="toggleAudio()"/>
          <Button v-if="playing == true" icon="pi pi-pause" rounded aria-label="Pause" @click="toggleAudio()"/>
        </div>
        <div class="col-4 flex justify-content-center align-content-center">
            <!-- <div class="text-center p-3 border-round-sm bg-primary font-bold">4</div> -->
            <Button size="large" icon="pi pi-exclamation-circle" severity="warning" text rounded aria-label="Report Song" v-tooltip="'Report a broken song'" @click="report.dialog = true" />
        </div>
    </div>
 
    <div id="progress-bar"></div>
    <audio
        id="audio-player"
        style="display:none"
        ref="player">
        <source :src="url" type="audio/mpeg" />
    </audio>
    
  </div>
</template>

<script>
// import AudioPlayerVue from './AudioPlayer.vue';
import WaveSurfer from 'wavesurfer.js';
import axios from "axios";
// https://muhammadatt.medium.com/building-an-mp3-audio-player-in-vue-js-c5884207251c
export default {
  components: {
    // AudioPlayerVue,
  },
  props: ['url'],
  data() {
    return {
      playing: false,
    }
  },
  methods: {
    toggleAudio() {
      let _self = this;
      var audio = document.getElementById("waveform");
      if (audio.paused) {
        audio.play();
        _self.playing = true
      } else {
        audio.pause();
        _self.playing = false
      }
    },
    loadAudioData() {
      let _self = this;
      let params = { url: _self.url };
      axios({
        url: "/song/api",
        method: "get",
        params: params,
        headers: { Accept: "audio/basic" }, // Set the Accept header to expect audio data
      })
        .then(function (response) {
          console.log(response);
          // Process the audio data here, for example, initialize the waveform player
          _self.initializeWaveSurfer(response.data);
        })
        .catch(function (error) {
          console.log("ERROR");
          console.log(error);
        })
        .finally(function () {
        });
    },
    initializeWaveSurfer(audioData) {
      const options = {
        container: '#waveform',
        waveColor: 'white',
        progressColor: 'purple',
        cursorColor: 'white',
        barWidth: 3,
        barRadius: 10,
        barGap: 2,
        height: 50,
        responsive: true,
        normalize: true,
        backend: 'MediaElement',
      };

      this.waveSurfer = WaveSurfer.create(options);
      this.waveSurfer.loadBlob(new Blob([audioData]));

      // this.waveSurfer.on('play', () => {
      //   this.$refs.audio.play();
      // });

      // this.waveSurfer.on('pause', () => {
      //   this.$refs.audio.pause();
      // });
    },
  },
  mounted() {
    this.loadAudioData();
  },
}
</script>

<style>
#audio-player-container {
  height: 100%
}
</style>
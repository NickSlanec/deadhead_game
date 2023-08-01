<template>
  <div id="audio-player-container" class="p-3">
    
    <div class="grid mb-3">
        <div class="col-12">
            <!-- <div class="text-center p-3 border-round-sm bg-primary font-bold">12</div> -->
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
      var audio = document.getElementById("audio-player");
      if (audio.paused) {
        audio.play();
        _self.playing = true
      } else {
        audio.pause();
        _self.playing = false
      }
    },
  },
  mounted() {
  },
}
</script>

<style>
#audio-player-container {
  height: 100%
}
</style>
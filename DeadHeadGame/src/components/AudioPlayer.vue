<template>
  <div id="audio-player-container" class="p-3">
    <div class="grid mt-2">
      <div class="col-4 flex justify-content-end align-content-center">
        <!-- <div class="text-center p-3 border-round-sm bg-primary font-bold">4</div> -->
        <Button size="large" icon="pi pi-refresh" text style="color:white" rounded aria-label="New Song"
          v-tooltip.left="'Get a new song'" @click="$emit('getSong')" />
      </div>
      <div class="col-4 flex justify-content-center align-content-center">
        <button class="play-button" v-if="playing == false" icon="pi pi-play" aria-label="Play" @click="toggleAudio()">
          <i class="pi pi-play" style="font-size: 1.5rem; color:white"></i>
        </button>
        <button class="play-button" v-if="playing == true" icon="pi pi-pause" aria-label="Pause" @click="toggleAudio()">
          <i class="pi pi-pause" style="font-size: 1.5rem; color:white"></i>
        </button>
      </div>
      <div class="col-4 flex justify-content-start align-content-center">
        <!-- <div class="text-center p-3 border-round-sm bg-primary font-bold">4</div> -->
        <Button size="large" icon="pi pi-exclamation-circle" style="color:white" text rounded aria-label="Report Song"
          v-tooltip.right="'Report a broken song'" @click="$emit('reportSong')" />
      </div>
    </div>

    <div id="progress-bar" class="flex-grow mt-2">
      <div class="relative w-full h-full">
        <input v-model="playbackTime" type="range" min="0" :max="audioDuration" class="slider w-full h-full" id="position" name="position" />
        
        <div class="flex relative w-full h-full" style="justify-content: space-between;">
          <span class="text-sm" style="color: #ffffff"> {{elapsedTime()}} </span>
          <span class="text-sm" style="color: #ffffff"> {{totalTime()}} </span>
        </div>
      </div>
    </div>
    <audio id="audio-player" style="display:none" ref="player">
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
      playbackTime: 0,
      audioDuration: 100,
      audioLoaded: false,
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
    initSlider() {
      var audio = this.$refs.player;
      if (audio) {
        this.audioDuration = Math.round(audio.duration);
      }
    },
    //Convert audio current time from seconds to min:sec display
    convertTime(seconds) {
      const format = val => `0${Math.floor(val)}`.slice(-2);
      var hours = seconds / 3600;
      var minutes = (seconds % 3600) / 60;
      return [minutes, seconds % 60].map(format).join(":");
    },
    //Show the total duration of audio file
    totalTime() {
      var audio = this.$refs.player;
      if (audio) {
        var seconds = audio.duration;
        return this.convertTime(seconds);
      } else {
        return '00:00';
      }
    },
    //Display the audio time elapsed so far
    elapsedTime() {
      var audio = this.$refs.player;
      if (audio) {
        var seconds = audio.currentTime;
        return this.convertTime(seconds);
      } else {
        return '00:00';
      }
    },
    //Playback listener function runs every 100ms while audio is playing
    playbackListener(e) {
      var audio = this.$refs.player;
      //Sync local 'playbackTime' var to audio.currentTime and update global state
      this.playbackTime = audio.currentTime;

      //console.log("update: " + audio.currentTime);
      //Add listeners for audio pause and audio end events
      audio.addEventListener("ended", this.endListener);
      audio.addEventListener("pause", this.pauseListener);
    },
    //Function to run when audio is paused by user
    pauseListener() {
      this.playing = false;
      this.listenerActive = false;
      this.cleanupListeners();
    },
    //Function to run when audio play reaches the end of file
    endListener() {
      this.playing = false;
      this.listenerActive = false;
      this.cleanupListeners();
    },
    //Remove listeners after audio play stops
    cleanupListeners() {
      var audio = this.$refs.player;
      audio.removeEventListener("timeupdate", this.playbackListener);
      audio.removeEventListener("ended", this.endListener);
      audio.removeEventListener("pause", this.pauseListener);
      //console.log("All cleaned up!");
    },
    toggleAudio() {
      var audio = this.$refs.player;
      //var audio = document.getElementById("audio-player");
      if (audio.paused) {
        audio.play();
        this.playing = true;
      } else {
        audio.pause();
        this.playing = false;
      }
    },
  },
  mounted() {
    // nextTick code will run only after the entire view has been rendered
    this.$nextTick(function () {

      var audio = this.$refs.player;
      //Wait for audio to load, then run initSlider() to get audio duration and set the max value of our slider 
      // "loademetadata" Event https://www.w3schools.com/tags/av_event_loadedmetadata.asp
      audio.addEventListener(
        "loadedmetadata",
        function (e) {
          this.initSlider();
        }.bind(this)
      );
      // "canplay" HTML Event lets us know audio is ready for play https://www.w3schools.com/tags/av_event_canplay.asp
      audio.addEventListener(
        "canplay",
        function (e) {
          this.audioLoaded = true;
        }.bind(this)
      );
      //Wait for audio to begin play, then start playback listener function
      this.$watch("playing", function () {
        if (this.playing) {
          var audio = this.$refs.player;
          this.initSlider();
          //console.log("Audio playback started.");
          //prevent starting multiple listeners at the same time
          if (!this.listenerActive) {
            this.listenerActive = true;
            //for a more consistent timeupdate, include freqtimeupdate.js and replace both instances of 'timeupdate' with 'freqtimeupdate'
            audio.addEventListener("timeupdate", this.playbackListener);
          }
        }
      });
      //Update current audio position when user drags progress slider
      this.$watch("playbackTime", function () {
        var audio = this.$refs.player;
        var diff = Math.abs(this.playbackTime - this.$refs.player.currentTime);

        //Throttle synchronization to prevent infinite loop between playback listener and this watcher
        if (diff > 0.01) {
          this.$refs.player.currentTime = this.playbackTime;
        }
      });
    });
  }
}
</script>

<style>
#audio-player-container {
  height: 100%
}

.slider {
  -webkit-appearance: none;
  appearance: none;
  background: #21073e;
  height: 15px;
  border-radius: 15px; 
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%; 
  background: linear-gradient(155deg, rgba(248, 93, 198, 1) 0%, rgba(126, 75, 255, 1) 100%);
  cursor: pointer;
}

.play-button {
  background: rgb(248, 93, 198);
  background: linear-gradient(155deg, rgba(248, 93, 198, 1) 0%, rgba(126, 75, 255, 1) 100%);
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  border: none;
}
</style>
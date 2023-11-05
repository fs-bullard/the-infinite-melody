// Create an AudioContext
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

// Define a function to play a musical note for a given duration
function playNoteWithDuration(note, duration) {
  const oscillator = audioCtx.createOscillator();
  const gainNode = audioCtx.createGain();

  oscillator.connect(gainNode);
  gainNode.connect(audioCtx.destination);

  oscillator.type = 'sine';
  oscillator.frequency.value = note;

  gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
  oscillator.start(audioCtx.currentTime);
  oscillator.stop(audioCtx.currentTime + duration);
}

// Play a sequence of musical notes with different durations
playNoteWithDuration(440, 1); // A 440 Hz for 1 second
playNoteWithDuration(523.25, 0.5); // C 523.25 Hz for 0.5 seconds
playNoteWithDuration(659.25, 0.25); // E 659.25 Hz for 0.25 seconds
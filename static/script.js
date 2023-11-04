const playButton = document.getElementById("play-button");
const noteContainer = document.getElementById("note-container");

const audio = new Audio();
const audioURLs = {
    "A4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/A4.mp3",
    "A#4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/Bb4.mp3",
    "B4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/B4.mp3",
    "C4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/C4.mp3",
    "C#4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/Db4.mp3",
    "D4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/D4.mp3",
    "D#4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/Eb4.mp3",
    "E4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/E4.mp3",
    "F4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/F4.mp3",
    "F#4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/Gb4.mp3",
    "G4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/G4.mp3",
    "G#4":"https://github.com/fuhton/piano-mp3/blob/master/piano-mp3/Ab4.mp3"
};

// Set animation duration (using 100 bpm)
const width = window.screen.availWidth;
const crotchetWidth = 100;
const bpm = 100;
const animationDuration = width * (60/bpm) / crotchetWidth * 1000;

let noteIndex = 0;
let animationStartTime = null;

// For testing
const exampleNotes = [["C4", 1500]];

function createNoteElement(note) {
    const noteElement = document.createElement("div");
    noteElement.className = "note";
    noteElement.textContent = note;
    noteContainer.appendChild(noteElement);
    return noteElement;
}

function animateNote(noteElement, animationDuration) {
    noteElement.style.left = "0";
    const animation = noteElement.animate(
        [{ left: "5%" }, { left:"0%" }],
        { animationDuration, easing: "linear" }
    );

    noteIndex++;
    playNextNote();

    animation.onfinish = () => {
        noteElement.remove();
    };
}

function playNextNote() {
    if (noteIndex < exampleNotes.length) {
        console.log('playing note')
        const { note, duration} = exampleNotes[noteIndex];
        const noteElement = createNoteElement(note);
        const currentTime = audio.currentTime;

        if (animationStartTime === null) {
            animationStartTime = currentTime;
        }

        animateNote(noteElement, duration);
        audio.src = audioURLs[note];
        audio.currentTime = 0; // Reset audio to the beginning
        audio.resume
        audio.play();

        // Schedule the next note's animation
        setTimeout(() => {
            noteElement.remove();
            noteIndex++;
            playNextNote();
        }, duration);
    }
}

// Start the music playback
playButton.addEventListener("click", function() {
    playNextNote();
});
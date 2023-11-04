const playButton = document.getElementById("play-button");
const noteContainer = document.getElementById("note-container");

const audio = new Audio();
const audioURLs = {
    "A4":"static/piano-mp3/A4.mp3",
    "A#4":"static/piano-mp3/Bb4.mp3",
    "B4":"static/piano-mp3/B4.mp3",
    "C4":"static/piano-mp3/C4.mp3",
    "C#4":"static/piano-mp3/Db4.mp3",
    "D4":"static/piano-mp3/D4.mp3",
    "D#4":"static/piano-mp3/Eb4.mp3",
    "E4":"static/piano-mp3/E4.mp3",
    "F4":"static/piano-mp3/F4.mp3",
    "F#4":"static/piano-mp3/Gb4.mp3",
    "G4":"static/piano-mp3/G4.mp3",
    "G#4":"static/piano-mp3/Ab4.mp3"
};

// For testing
const exampleNotes = [["C4", 1500], ["D4", 1500],["E4", 1500],["F4", 1500],["G4", 1500]];
let noteIndex = 0;

// Set animation duration (using 100 bpm)
// const width = window.screen.availWidth;
// const crotchetWidth = 100;
// const bpm = 100;

// const animationDuration = width * (60/bpm) / crotchetWidth * 1000;
const animationDuration = 1000

function createNoteElement(note) {
    console.log("Creating note");
    
    const noteElement = document.createElement("div");
    // noteElement.className = "note";

    const noteImage = document.createElement("img");
    noteImage.className = "note";
    noteImage.src = "static/crochet.png";
    noteElement.appendChild(noteImage);
    noteContainer.appendChild(noteElement);
    return noteElement;
}

function animateNote(noteElement, animationDuration) {
    console.log("Animating note");
    noteElement.style.left = "0%";
    const animation = noteElement.animate(
        [{ left: "0" }, { left:"100%" }],
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
        console.log('Playing note' + noteIndex);

        // Find the current note and its duration
        const note = exampleNotes[noteIndex][0];
        const duration = exampleNotes[noteIndex][1];

        // Create the note
        const noteElement = createNoteElement(note);

        animateNote(noteElement, animationDuration);

        audio.src = audioURLs[note];
        audio.currentTime = 0; // Reset audio to the beginning
        audio.play();
        noteElement.remove();
        noteIndex++;
       
        // Schedule the next note's animation
        setTimeout(playNextNote(), 1000);
    }
}

// Start the music playback
playButton.addEventListener("click", function() {
    playNextNote();
});
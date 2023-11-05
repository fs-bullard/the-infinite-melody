const playButton = document.getElementById("play-button");
const noteContainer = document.getElementById("note-container");

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
const exampleNotes = [["C4", 1500], ["D4", 1500], ["E4", 1500], ["F4", 1500], ["G4", 1500]];
// const exampleNotes = [["C4", 1500]];

// Set animation duration (using 100 bpm)
const width = window.screen.availWidth;
const crotchetWidth = 100;
const bpm = 100;

let elapsedTime = 0;

const animationDuration = width * (60/bpm) / crotchetWidth * 1000;
console.log(animationDuration)
// const animationDuration = 10000;

function createNoteElement(note) {
    const noteElement = document.createElement("div");

    let noteImage = document.createElement("img");

    noteImage.className = "note";
    noteImage.src = 'static/crochet.png';
    noteElement.appendChild(noteImage);
    noteContainer.appendChild(noteImage);

    return noteElement;
}

function playNextNote(noteIndex) {
    const audio = new Audio();

    // Find the current note and its duration
    const note = exampleNotes[noteIndex][0];
    const duration = exampleNotes[noteIndex][1];

    // Create the note
    const noteElement = createNoteElement(note);

    audio.src = audioURLs[note];
    audio.currentTime = 0; // Reset audio to the beginning
    audio.play();

    elapsedTime += duration;
    
    // Schedule the next note's animation
    console.log(elapsedTime)
    setTimeout(() => {
        generateSingleNote(noteIndex + 1);
    }, duration)

    //TODO: Remove finished notes
    setTimeout(() => {
        noteElement.remove;
    }, elapsedTime + animationDuration)

}

function generateSingleNote(noteIndex) {
    if (noteIndex < exampleNotes.length) {
        playNextNote(noteIndex)
        noteIndex += 1;
    }
}

// Start the music playback
playButton.addEventListener("click", function() {
    let noteIndex = 0;
    generateSingleNote(noteIndex);
});
const playButton = document.getElementById("play-button");
const noteContainer = document.getElementById("note-container");
// const musicContainer = document.getElementById("music-container");

const heights = {
    "A":-63,
    "B":-53,
    "C":-45,
    "D":-35,
    "E":-88,
    "F":-81,
    "G":-71,
};

// For testing
// const exampleNotes = [[["C4", "E3", "G5"], 1500], ["rest", 3000], [["E4"], 500], [["F4"], 1500], [["G4"], 1500]];
const exampleNotes = [[['B3'], 1], [['A4'], 1], [['G3'], 1], [['F3'], 1], [['D4'], 1], [['C3'], 1], [['F5'], 1], [['F4'], 1], [['B5'], 1], [['C6'], 1], [['E3'], 1], [['G4'], 1], [['A4'], 1], [['rest'], 1], [['A2'], 1], [['D3'], 1], [['B3'], 1], [['C3'], 1], [['C4'], 1], [['E2'], 1], [['A2'], 1], [['G4', 'C5', 'E5'], 1], [['A4'], 1], [['A3'], 1], [['Bb4', 'G5', 'Bb5', 'G3', 'Bb3'], 1], [['F4'], 1], [['C5'], 1], [['C4', 'A4', 'C5'], 1], [['E3'], 1], [['B4'], 1], [['B3'], 1], [['D4', 'E4'], 1], [['E5'], 1], [['C2'], 1], [['E3'], 1], [['A3'], 1], [['D3'], 1], [['C3'], 1], [['D4', 'G4'], 1], [['G4', 'Db4', 'A2'], 1], [['G3'], 1], [['A3'], 1], [['G2'], 1], [['E3'], 1], [['G4'], 1], [['A4'], 1], [['B4'], 1], [['C5'], 1], [['D2'], 1], [['D4'], 1], [['C3'], 1], [['G4'], 1], [['C4'], 1], [['C6'], 1], [['A5', 'G5'], 1], [['C3'], 1], [['E3'], 1], [['rest'], 1], [['G3'], 1], [['A2'], 1], [['B4'], 1], [['A4', 'C5'], 1], [['G4'], 1], [['E3'], 1], [['F4'], 1], [['G5', 'E6'], 1], [['C6'], 1], [['D4', 'C3'], 1], [['D5', 'D3'], 1], [['F4', 'A4'], 1], [['A4', 'C5'], 1], [['F4', 'Ab4', 'F5', 'D3', 'E3'], 1], [['B4'], 1], [['B3'], 1], [['E5'], 1], [['G5', 'E5', 'C3', 'C4'], 1], [['E3'], 1], [['F4', 'Db5', 'Ab4'], 1], [['B4'], 1], [['B3', 'Gb3'], 1], [['D6', 'F4'], 1], [['G5'], 1], [['A4', 'E5', 'Db5'], 1], [['Eb4', 'C5', 'Ab3', 'C4'], 1], [['D5'], 1], [['F4'], 1], [['D4'], 1], [['D2'], 1], [['C3'], 1], [['C6'], 1], [['A5'], 1], [['G5'], 1], [['A4', 'E3', 'B3'], 1], [['G4'], 1], [['C5', 'D5'], 1], [['E5'], 1], [['C5'], 1], [['E4'], 1], [['rest'], 1], [['C4'], 1], [['D4'], 1], [['G5'], 1], [['B4'], 1], [['D5'], 1], [['G4', 'D4'], 1], [['G3'], 1], [['B3'], 1], [['F3'], 1], [['E3'], 1], [['D3'], 1], [['C4', 'E4'], 1], [['G4', 'D4'], 1], [['B4', 'E5', 'E4'], 1], [['F4'], 1], [['A4'], 1], [['F3'], 1], [['rest'], 1], [['C5', 'Eb5', 'C4', 'Eb4'], 1], [['E3'], 1], [['D1', 'D2', 'A2', 'D3', 'F3', 'A3'], 1], [['G3'], 1], [['D4'], 1], [['B3', 'D4'], 1], [['rest'], 1], [['A4'], 1], [['G4'], 1], [['G3'], 1], [['E4', 'A4', 'Db5', 'E3', 'A3', 'Db4'], 1], [['D4', 'Bb3'], 1], [['E5', 'G5', 'Bb5', 'E6'], 1], [['D5'], 1], [['A4'], 1], [['F4', 'F3'], 1], [['B3', 'G4'], 1], [['G2'], 1], [['G3'], 1], [['E4'], 1], [['D4', 'Gb4', 'D5'], 1], [['G4', 'B4'], 1], [['E5', 'A1'], 1], [['G4'], 1], [['A5'], 1], [['F4'], 1], [['C3', 'C4', 'C5', 'C6'], 1], [['D5', 'F3'], 1], [['A3'], 1], [['D4'], 1], [['D6'], 1], [['E3'], 1], [['F6'], 1], [['A2'], 1], [['G2'], 1], [['E4', 'Ab3'], 1], [['B4', 'B3'], 1], [['C4', 'D4', 'D3', 'C3'], 1], [['A4'], 1], [['D5', 'B4'], 1], [['F5'], 1], [['F4'], 1], [['C6', 'D6'], 1], [['C5'], 1], [['C6'], 1], [['B5'], 1], [['rest'], 1], [['A4'], 1], [['B3'], 1], [['Bb2', 'F3', 'Ab3', 'D4'], 1], [['A6'], 1], [['D3'], 1], [['D2'], 1], [['A2'], 1], [['F3'], 1], [['B2'], 1], [['E3'], 1], [['D2'], 1], [['rest'], 1], [['C4', 'C3'], 1], [['G2'], 1], [['C2'], 1], [['A4', 'A3', 'Bb5', 'Bb4'], 1], [['E4'], 1], [['C3'], 1], [['C5'], 1], [['Bb5', 'F5', 'C6', 'Ab5'], 1], [['D6'], 1], [['A5'], 1], [['E6'], 1], [['Bb4', 'G5'], 1], [['C6'], 1], [['C4', 'E4'], 1], [['C5'], 1], [['D5'], 1], [['D6'], 1], [['A4'], 1], [['F5'], 1], [['G4'], 1], [['B2'], 1], [['A3'], 1], [['G5'], 1], [['A5'], 1], [['rest'], 1], [['Gb4', 'B4'], 1], [['E5'], 1], [['G5'], 1], [['A4', 'A3'], 1], [['rest'], 1], [['A3'], 1], [['D4'], 1], [['C4'], 1], [['E4'], 1], [['G3'], 1], [['F4'], 1], [['D4'], 1], [['B3'], 1], [['B4'], 1], [['Ab5', 'E5'], 1], [['B6'], 1], [['D3'], 1], [['B3'], 1], [['F5', 'F4', 'D4', 'A3'], 1], [['A4'], 1], [['F5', 'G5', 'A5', 'B5'], 1], [['E5'], 1], [['G3'], 1], [['E4'], 1], [['E4', 'G4', 'C5', 'Db4', 'Gb4', 'Bb4'], 1], [['G2'], 1], [['E5', 'C6', 'E6'], 1], [['E5'], 1], [['D4', 'G5'], 1], [['B4'], 1], [['A5'], 1], [['G4'], 1], [['C5'], 1], [['D5'], 1], [['B4'], 1], [['C4', 'G3', 'E4'], 1], [['G4', 'Db5', 'A4'], 1], [['C5'], 1], [['F4', 'Bb2', 'Bb3'], 1], [['F5'], 1], [['Bb4', 'D5'], 1], [['F3', 'G3'], 1], [['E5'], 1], [['C5'], 1], [['F5'], 1], [['E6', 'C6'], 1], [['E4'], 1], [['B5'], 1], [['C6', 'C4', 'G5'], 1], [['B4'], 1], [['C6'], 1], [['Ab5', 'D5', 'Gb5', 'Ab4'], 1], [['rest'], 1], [['F6', 'B5', 'F5'], 1], [['D6'], 1], [['B4'], 1], [['G4', 'D5'], 1], [['C5', 'E5', 'A5', 'C6'], 1], [['rest'], 1], [['G5', 'Bb5'], 1], [['B5'], 1], [['G4', 'Eb4', 'G3'], 1], [['E6'], 1], [['C6'], 1], [['G5'], 1], [['E5'], 1], [['G3'], 1], [['A2'], 1], [['B5', 'D5', 'F5', 'Ab5'], 1], [['E6'], 1], [['D6'], 1], [['E5'], 1], [['B4'], 1], [['D4'], 1], [['E4'], 1], [['C5'], 1], [['G4'], 1], [['F5'], 1], [['E5'], 1], [['F6', 'Eb6', 'E6', 'D6'], 1], [['Eb3', 'C4'], 1], [['F4'], 1], [['G4'], 1], [['G3'], 1], [['B4'], 1], [['B5'], 1], [['C6'], 1], [['D6'], 1], [['C5'], 1], [['G4', 'C4'], 1], [['B3'], 1], [['E5', 'Eb5', 'D5'], 1], [['A5'], 1], [['Bb4', 'C5'], 1], [['F3'], 1], [['G4'], 1], [['rest'], 1], [['D5'], 1], [['C4'], 1]]



// Set animation duration (using 100 bpm)
const width = window.screen.availWidth;
const crotchetWidth = 100;
const bpm = 170;

let elapsedTime = 0;

const animationDuration = width * (60/bpm) / crotchetWidth * 1000;
console.log(animationDuration)
// const animationDuration = 10000;

function getNoteHeight(note) {
    prefix = note.slice(0, 1);
    return heights[prefix];
}

function createNoteElement(note) {
    const noteElement = document.createElement("div");

    let noteImage = document.createElement("img");

    noteImage.className = "note";
    if (note[1] == 'b') {
        noteImage.src = 'static/crochet_flat.png';
    } else {
        noteImage.src = 'static/crochet.png';
    }

    noteImage.style.bottom = `${String(getNoteHeight(note))}px`;
    noteElement.appendChild(noteImage);
    noteContainer.appendChild(noteImage);

    return noteElement;
}

function createRestElement() {
    const noteElement = document.createElement("div");

    let noteImage = document.createElement("img");

    noteImage.className = "rest";
    noteImage.src = 'static/quarter_rest.png';
    noteImage.style.bottom = "-75px";
    noteElement.appendChild(noteImage);
    noteContainer.appendChild(noteImage);
    return noteElement;
}

function playNextNote(noteIndex) {

    // Find the current note and its duration
    const note = exampleNotes[noteIndex][0];
    const duration = exampleNotes[noteIndex][1] * note.length * 60000 / bpm;

    // Create the note or rest
    if (note == 'rest') {
        createRestElement(note);
    } else {
        let i = 0;
        while (i < note.length) {
            const audio = new Audio();
            createNoteElement(note[i]);
            audio.src = `static/piano-mp3/${note[i]}.mp3`;
            audio.currentTime = 0; // Reset audio to the beginning
            audio.play();
            i++;
        }
    }

    elapsedTime += duration;
    
    // Schedule the next note's animation
    setTimeout(() => {
        generateSingleNote(noteIndex + 1);
    }, duration)  

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
    // Remove blur and button
    // musicContainer.style.filter = "none";
    generateSingleNote(noteIndex);
});
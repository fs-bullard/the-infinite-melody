const playButton = document.getElementById("play-button");
const muteButton = document.getElementById("mute-button");
const unmuteButton = document.getElementById("unmute-button");
const noteContainer = document.getElementById("note-container");

const bass_heights = [
    "F2",
    "G2",
    "A2",
    "B2",
    "C3",
    "D3",
    "E3",
    "F3",
    "G3",
    "A3",
    "B3"
];
const treb_heights = [
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
    "B4",
    "C4",
    "C5",
    "D5",
    "E5",
    "F5",
    "G5",
    "A5",
    "B5"
];
const bass_bottom = -227;
const treb_bottom = -92;
const dh = 8.6;

var notes = [];
var isPlaying = false;

const width = window.screen.availWidth;
const crotchetWidth = 100;
const bpm = 170;

let elapsedTime = 0;

const animationDuration = width * (60/bpm) / crotchetWidth * 1000;

function getNoteHeight(note) {
    const natural = note.slice(0, 1) + note.slice(-1);
    if (bass_heights.includes(natural)) {
        return bass_bottom + bass_heights.indexOf(natural)*dh;
    } else if (treb_heights.includes(natural)) {
        return treb_bottom + treb_heights.indexOf(natural)*dh;
    } else if (natural.slice(-1) == 0) {
        return bass_bottom + bass_heights.indexOf(natural.slice(0, 1) + "3")*dh;
    } else if (natural.slice(-1) == 1) {
        return bass_bottom + bass_heights.indexOf(natural.slice(0, 1) + "3")*dh;
    } else if (natural.slice(-1) == 2) {
        return bass_bottom + bass_heights.indexOf(natural.slice(0, 1) + "3")*dh;
    } else if (natural.slice(-1) == 6) {
        return treb_bottom + treb_heights.indexOf(natural.slice(0, 1) + "5")*dh;
    } else {
        return treb_bottom + treb_heights.indexOf(natural.slice(0, 1) + "5")*dh;
    } 
}

function createNoteElement(note, n) {
    const noteElement = document.createElement("div");

    let noteImage = document.createElement("img");

    noteImage.className = "note";
    if (note[1] == 'b') {
        if (n == 1) {
            noteImage.src = 'static/crochet_flat.png';
        } else if (n == 2 || n == 3) {
            noteImage.src = 'static/minim_flat.png';
        } else {
            noteImage.src = 'static/semibreve_flat.png';

        }
        
    } else {
        if (n == 1) {
            noteImage.src = 'static/crochet.png';
        } else if (n == 2 || n == 3) {
            noteImage.src = 'static/minim.png';
        } else {
            noteImage.src = 'static/semibreve.png';
        }

       
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

function playNextNote(noteIndex, note, dur) {

    // Find the current note and its duration
    const n = note.length
    const duration = dur * 60000 / bpm;

    // Create the note or rest
    if (note == 'rest') {
        createRestElement(note);
    } else {
        let i = 0;
        while (i < note.length) {      
            createNoteElement(note[i], n);
            if (isPlaying) {
                const audio = new Audio();
                audio.src = `static/piano-mp3/${note[i]}.mp3`;
                audio.currentTime = 0; // Reset audio to the beginning
                audio.play();
            }
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
    playNextNote(noteIndex, notes[noteIndex][0], notes[noteIndex][1]);
}

// Start the music playback
playButton.addEventListener("click", function() {
    let noteIndex = 0;
    isPlaying = true;
    generateSingleNote(noteIndex);
    this.style.display = "none";
    muteButton.style.display = "inline"
});

muteButton.addEventListener("click", function() {
    this.style.display = "none"
    unmuteButton.style.display = "inline"
    isPlaying = false;
})

unmuteButton.addEventListener("click", function() {
    this.style.display = "none"
    muteButton.style.display = "inline"
    isPlaying = true;
})

var socket = io.connect();
    //receive details from server
    socket.on("newnote", function (msg) {
        notes.push([msg.note, msg.duration]);

    });



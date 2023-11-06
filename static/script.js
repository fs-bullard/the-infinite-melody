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

var notes = [];

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
    const n = note.length;
    const duration = dur * n * 60000 / bpm;

    // Create the note or rest
    if (note == 'rest') {
        createRestElement(note);
    } else {
        let i = 0;
        while (i < note.length) {
            const audio = new Audio();
            createNoteElement(note[i], n);
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
    playNextNote(noteIndex, notes[noteIndex][0], notes[noteIndex][1]);
}

// Start the music playback
playButton.addEventListener("click", function() {
    let noteIndex = 0;
    generateSingleNote(noteIndex);
    this.style.display = "none";
});

var socket = io.connect();
  //receive details from server
  socket.on("newnote", function (msg) {
    notes.push([msg.note, msg.duration]);

    // // Show only MAX_DATA_COUNT data
    // if (myChart.data.labels.length > MAX_DATA_COUNT) {
    //   removeFirstData();
    // }
    // addData(msg.date, msg.value);
  });
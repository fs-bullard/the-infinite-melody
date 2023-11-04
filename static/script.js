const noteContainer = document.getElementById("note-container");
const exampleNotes = [["C4", 1.5], ["G4", 0.5]];

function createNote(note) {
    const noteElement = document.createElement("div");
    noteElement.className = "note";
    noteElement.textContent = note;
    noteContainer.appendChild(noteElement);

    // Duration needs to be adjusted for tempo?
    const animation = noteElement.animate(
        [{ left: "0%" }, { left:"100%" }],
        { duration: 4000, easing: "linear" }
    );

    animation.onfinish = () => {
        noteElement.remove();
        playNextNote();
    };
}

function playMusic() {
    let noteIndex = 0;
    const playbackInterval = 500;

    function play

}

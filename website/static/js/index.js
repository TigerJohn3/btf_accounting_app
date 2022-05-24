function deleteNote(noteID) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteID: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}
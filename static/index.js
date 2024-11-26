function deleteNote(noteId) {
    //send request to the delete-note endpoint
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        //reload the window
      window.location.href = "/";
    });
}
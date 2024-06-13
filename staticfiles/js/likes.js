const likeButtons = document.getElementsByClassName("btn-like");

for (let button of likeButtons) {
  let entryId = button.getAttribute("data-entry_id");
//   alert(`Setting button ${entryId}`);
  let oldPath = window.location.href.split("?")[0].slice(0, -1);
  let oldParams = window.location.href.split("?")[1];
  if (oldPath) {
    if (oldParams) {
      button.setAttribute("href", `${oldPath}/like/${entryId}/?${oldParams}`);
    } else {
      button.setAttribute("href", `${oldPath}/like/${entryId}/`);
    }
  } else {
    button.setAttribute("href", `like/${entryId}/`);
  }
}


// let commentParagraph = document.getElementById(`comment${commentId}`);
// let commentContent = commentParagraph.innerText;
// let hiddenFormDiv = document.getElementById(`commentform${commentId}`);
// let editCommentForm = document.getElementById(`editCommentForm${commentId}`);
// let inplaceCommentText = document.getElementById(`updatedComment${commentId}`);
// hiddenFormDiv.removeAttribute('class', 'visually-hidden');
// commentParagraph.setAttribute('class', 'visually-hidden');
// commentText.value = commentContent;
// inplaceCommentText.value = commentContent;
//submitButton.innerText = "Update";
// commentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);

// for (let button of deleteButtons) {
//     button.addEventListener("click", (e) => {
//         let commentId = e.target.getAttribute("data-comment_id");
//         let oldPath = window.location.href.split('?')[0].slice(0, -1);
//         //let (deleteConfirm.href);
//         deleteConfirm.href = `${oldPath}/delete-comment/${commentId}/`;
//         //deleteModal.show();
//     });
// }

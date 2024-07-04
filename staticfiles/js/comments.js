/* This script enables the editing and deleting of comments.
*/
window.addEventListener("DOMContentLoaded", function () {
  // Comment edit/delete buttons
  const editButtons = document.getElementsByClassName("btn-edit");
  const deleteButtons = document.getElementsByClassName("btn-delete");
  // Modal delete button
  const deleteConfirm = document.getElementById("deleteCommentConfirm");
  // Path to return to
  const oldPath = window.location.href.split("?")[0];

  // Handle the edit comment functionality
  for (let button of editButtons) {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      // Get the comment ID and text to be edited
      let commentId = e.currentTarget.getAttribute("data-comment-id");
      let commentParagraph = document.getElementById(`comment${commentId}`);
      let commentContent = commentParagraph.innerText;
      // Get the form with the in-place text field and 'Update' button
      let hiddenFormDiv = document.getElementById(`commentform${commentId}`);
      let editCommentForm = document.getElementById(
        `editCommentForm${commentId}`
      );
      let inplaceCommentText = document.getElementById(
        `updatedComment${commentId}`
      );
      // Show the 'Update' form
      hiddenFormDiv.removeAttribute("class", "d-none");
      // Hide the comment paragraph to be edited
      commentParagraph.setAttribute("class", "visually-hidden");
      // Pre-fill the text area with the old comment text
      inplaceCommentText.value = commentContent;
      // Prepare the path for the form submit button
      editCommentForm.setAttribute(
        "action",
        `${oldPath}edit-comment/${commentId}/`
      );
    });
  }

  // Handle the delete comment functionality
  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      // Prepare the modal delete button with the correct path and comment ID
      let commentId = e.currentTarget.getAttribute("data-comment-id");
      deleteConfirm.href = `${oldPath}delete-comment/${commentId}/`;
    });
  }
});

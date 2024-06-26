// import 'bootstrap';
// window.Modal = bootstrap.Modal;
window.addEventListener("DOMContentLoaded", function () {
  alert('loaded')
  alert(document.getElementById(`comment${15}`))
  const editButtons = document.getElementsByClassName("btn-edit");
  // const commentText = document.getElementById("id_content");
  const commentForm = document.getElementById("commentForm");

  // const deleteModal = new Modal(document.getElementById("deleteModal"));
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteConfirm = document.getElementById("deleteCommentConfirm");

  for (let button of editButtons) {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      let commentId = e.currentTarget.getAttribute("data-comment_id");
      alert(commentId)
      let commentParagraph = document.getElementById(`comment${commentId}`);
      let commentContent = commentParagraph.innerText;
      let hiddenFormDiv = document.getElementById(`commentform${commentId}`);
      hiddenFormDiv.removeAttribute("class", "d-none");

      let editCommentForm = document.getElementById(
        `editCommentForm${commentId}`
      );
      let inplaceCommentText = document.getElementById(
        `updatedComment${commentId}`
      );
      //hiddenFormDiv.setAttribute("aria-hidden", "false");
      commentParagraph.setAttribute("class", "visually-hidden");
      // commentText.value = commentContent;
      inplaceCommentText.value = commentContent;
      //submitButton.innerText = "Update";
      let oldPath = window.location.href.split("?")[0].slice(0, -1);
      // commentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);
      editCommentForm.setAttribute(
        "action",
        `${oldPath}/edit-comment/${commentId}/`
      );
    });
  }

  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      alert(e.currentTarget)
      let commentId = e.currentTarget.getAttribute("data-comment_id");
      let oldPath = window.location.href.split("?")[0].slice(0, -1);
      //let (deleteConfirm.href);
      alert(commentId);
      deleteConfirm.href = `${oldPath}/delete-comment/${commentId}/`;
      //deleteModal.show();
    });
  }
});

/* This script finds all buttons associated with a previously uploaded audio file
 * as well as the hidden modal delete button and prepares the delete path
 * with the correct file ID.
 */

window.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteConfirm = document.getElementById("deleteFileConfirm");
  const oldPath = window.location.href.split("?")[0];

  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      let fileId = e.currentTarget.getAttribute("data-file-id");
      deleteConfirm.href = `${oldPath}delete-file/${fileId}/`;
    });
  }
});

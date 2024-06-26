// import 'bootstrap';
// window.Modal = bootstrap.Modal;

// const editButtons = document.getElementsByClassName("btn-edit");
// const commentText = document.getElementById("id_content");
window.addEventListener("DOMContentLoaded", function () {

  // const deleteModal = new Modal(document.getElementById("deleteModal"));
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteConfirm = document.getElementById("deleteFileConfirm");

  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      let fileId = e.currentTarget.getAttribute("data-file_id");
      alert(fileId)
      let oldPath = window.location.href.split("?")[0].slice(0, -1);
      //let (deleteConfirm.href);
      deleteConfirm.href = `${oldPath}/delete-file/${fileId}/`;
      //alert(`${oldPath}/delete-file/${fileId}/`);
      //deleteModal.show();
    });
  }

});

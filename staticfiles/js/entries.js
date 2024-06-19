// import 'bootstrap';
// window.Modal = bootstrap.Modal;

// const editButtons = document.getElementsByClassName("btn-edit");
// const commentText = document.getElementById("id_content");
const commentForm = document.getElementById("commentForm");
const saveBtn = document.getElementById("btn-save-entry");


// const deleteModal = new Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName('btn-delete');
const deleteConfirm = document.getElementById('deleteConfirm');


for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let fileId = e.target.getAttribute("data-file_id");
        let oldPath = window.location.href.split('?')[0].slice(0, -1);
        //let (deleteConfirm.href);
        deleteConfirm.href = `${oldPath}/delete-file/${fileId}/`;
        //alert(`${oldPath}/delete-file/${fileId}/`);
        //deleteModal.show();
    });
}


$("#modalSave").modal({
    backdrop: "static",
    keyboard: true,
    show: true,
  });
  saveBtn.addEventListener("click", (e) => {
    e.preventDefault();
    alert(`${document.getElementById("modalSave").getAttributeNames}`);
    alert(e.detail);
  });
  
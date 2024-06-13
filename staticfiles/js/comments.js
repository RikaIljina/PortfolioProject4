// import 'bootstrap';
// window.Modal = bootstrap.Modal;

const editButtons = document.getElementsByClassName("btn-edit");
// const commentText = document.getElementById("id_content");
const commentForm = document.getElementById("commentForm");

// const deleteModal = new Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName('btn-delete');
const deleteConfirm = document.getElementById('deleteConfirm');


for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("data-comment_id");
        let commentParagraph = document.getElementById(`comment${commentId}`);
        let commentContent = commentParagraph.innerText;
        let hiddenFormDiv = document.getElementById(`commentform${commentId}`);
        let editCommentForm = document.getElementById(`editCommentForm${commentId}`);
        let inplaceCommentText = document.getElementById(`updatedComment${commentId}`);
        hiddenFormDiv.removeAttribute('class', 'visually-hidden');
        commentParagraph.setAttribute('class', 'visually-hidden');
        // commentText.value = commentContent;
        inplaceCommentText.value = commentContent;
        //submitButton.innerText = "Update";
        let oldPath = window.location.href.split('?')[0].slice(0, -1);
       // commentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);
        editCommentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);
    });
}

for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("data-comment_id");
        let oldPath = window.location.href.split('?')[0].slice(0, -1);
        //let (deleteConfirm.href);
        deleteConfirm.href = `${oldPath}/delete-comment/${commentId}/`;
        //deleteModal.show();
    });
}
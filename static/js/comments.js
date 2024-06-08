const editButtons = document.getElementsByClassName("btn-edit");
// const commentText = document.getElementById("id_content");
const commentForm = document.getElementById("commentForm");

// hiddenFormDiv.removeAttribute('class', 'visually-hidden');
// commentParagraph.setAttribute('class', 'visually-hidden');

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
        oldPath = window.location.href.slice(0, -1);
        commentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);
        editCommentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);
    });
}
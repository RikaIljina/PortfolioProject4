const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_content");

for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("data-comment_id");
        let commentContent = document.getElementById(`comment${commentId}`).innerText;
        commentText.value = commentContent;
        submitButton.innerText = "Update";
        oldPath = window.location.href.slice(0, -1);
        commentForm.setAttribute("action", `${oldPath}/edit-comment/${commentId}/`);
    });
}
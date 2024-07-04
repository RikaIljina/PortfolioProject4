/* This script finds all active 'Like' buttons on a page, and on click checks
 * whether they belong to an already liked entry.
 * The link URL is prepared accordingly.
 * It also makes sure to preserve any GET parameters of the page the Like button
 * is clicked on.
 */

window.addEventListener("DOMContentLoaded", function () {
  const likeButtons = document.getElementsByClassName("btn-like");
  var currentPath = window.location.href.split("?");
  const oldPath = currentPath[0];
  const oldParams = currentPath[1];

  for (let button of likeButtons) {
    button.addEventListener("click", (e) => {
      let liked = button.getAttribute("data-liked");
      let favoriteView = button.getAttribute("data-favorite-view");
      // The ID can be the 'Like' object ID or the 'Entry' object ID depending on
      // the view
      let delId = button.getAttribute("data-entry-id");
      let mainPath = "";

      // Prepare 'delete' path for liked entries
      if (favoriteView) {
        mainPath = "like/delete-by-like/";
      } else if (liked) {
        mainPath = "like/delete-by-entry/";
        // Prepare 'add like' path for not-liked entries
      } else {
        mainPath = "like/";
      }

      if (oldPath) {
        if (oldParams) {
          button.setAttribute(
            "href",
            `${oldPath}${mainPath}${delId}/?${oldParams}`
          );
        } else {
          button.setAttribute("href", `${oldPath}${mainPath}${delId}/`);
        }
      } else {
        if (oldParams) {
          button.setAttribute("href", `${mainPath}${delId}/?${oldParams}`);
        } else {
          button.setAttribute("href", `${mainPath}${delId}/`);
        }
      }
    });
  }
});

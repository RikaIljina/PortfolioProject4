// The menu toggle button in the navbar has a hover effect that stops working
// once the button is clicked and therefore focused. The following code removes
// the focus from the button.

document.getElementById("toggler-btn").addEventListener("click", function () {
  // Use setTimeout to remove focus from the icon after clicking it
  setTimeout(() => {
    this.blur();
  }, 500);
});

document
  .getElementById("sidebar-toggle-btn")
  .addEventListener("click", function () {
    // Use setTimeout to remove focus from the icon after clicking it
    setTimeout(() => {
      this.blur();
    }, 500);
  });

// Prevent filter items from collapsing once opened (on large screens)
window.addEventListener("DOMContentLoaded", function () {
  var sideBar = document.getElementById("sidebar");
  var sideBarState = getComputedStyle(sideBar).position;
  var filterCategories = document.getElementsByClassName("filter-cat");
//   alert(filterCategories);
  for (filterCat of filterCategories) {
    if (
      sideBarState != "absolute" &&
      filterCat.classList.contains("force-show")
    ) {
      filterCat.classList.add("show");
    }
  }
});

// Hide filter on small devices when sidebar is overlaying content
// function hideFilter(item) {
//   var w = window.innerWidth;
//   var sideBar = document.getElementById("sidebar");
//   var sideBarState = getComputedStyle(sideBar).position;
//   var filterCategory = item.parentElement.parentElement;
//   if (sideBarState === "absolute") {
//     filterCategory.classList.remove("show");
//   }
// }

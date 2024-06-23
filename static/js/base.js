// Prevent filter items from collapsing once opened (on large screens)
window.addEventListener("DOMContentLoaded", function () {
  var sideBar = document.getElementById("sidebar");
  var sideBarState = getComputedStyle(sideBar).position;
  var filterLinks = document.getElementsByClassName("filter-link");
  var filterTitles = document.getElementsByClassName("filter-title");
  var filterCategories = document.getElementsByClassName("filter-cat");

  if (sideBarState === "absolute") {
    var sidebarCollapsed = true;
  } else {
    var sidebarCollapsed = false;
  }


  //   alert(filterCategories);
  for (let filterCat of filterCategories) {
    if (
      sideBarState != "absolute" &&
      filterCat.classList.contains("force-show") &&
      !sidebarCollapsed
    ) {
      filterCat.classList.add("show");
    } else if (sidebarCollapsed) {
      filterCat.classList.remove("show");
    }
  }
  for (let link of filterLinks) {
    link.addEventListener("click", function () {
      if (sideBarState === "absolute") {
        var currentTitle = link.children[1];
        // only do it if it is uncollapsed
        if (link.getAttribute("aria-expanded") === "true") {
          currentTitle.classList.remove("d-none");
          currentTitle.classList.add("d-inline");
        } else {
          currentTitle.classList.add("d-none");
          currentTitle.classList.remove("d-inline");
        }
        if (currentTitle.classList.contains("d-none")) {
          for (title of filterTitles) {
            title.classList.add("d-none");
            title.classList.remove("d-inline");
          }
        } else {
          for (title of filterTitles) {
            title.classList.remove("d-none");
            title.classList.add("d-inline");
          }
        }
        // for (title of filterTitles) {
        //   title.classList.toggle("d-none");
        //   title.classList.toggle("d-md-none");
        //   title.classList.toggle("d-inline");
        //   title.classList.toggle("d-md-inline");
        // }
      } else {
        if (!sidebarCollapsed && filterTitles[0].classList.contains("d-none")) {
          for (title of filterTitles) {
            title.classList.remove("d-none");
            title.classList.add("d-inline");
          }
        } else if (!sidebarCollapsed) {
          for (title of filterTitles) {
            title.classList.add("d-none");
            title.classList.remove("d-inline");
            for (cat of filterCategories) {
              cat.classList.remove("show");
            }
          }
        }
      }
    });
  }
});

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
    // Toggle the expand/collapse button icon
    for (let element of this.children) {
      element.classList.toggle("d-none");
      element.classList.toggle("d-inline");
    }

    if (
      document.querySelector("#toggle-icon-expand").classList.contains("d-none") // || d-md-inline
    ) {
      sidebarCollapsed = false;
    } else {
      sidebarCollapsed = true;
    }

    var filterCategories = document.getElementsByClassName("filter-cat");
    for (cat of filterCategories) {
      cat.classList.remove("show");
    }

    var filterTitles = document.getElementsByClassName("filter-title");
    for (title of filterTitles) {
      if (!sidebarCollapsed) {
        title.classList.remove("d-none");
        title.classList.add("d-inline");
      } else {
        title.classList.add("d-none");
        title.classList.remove("d-inline");
      }
    }

    // Use setTimeout to remove focus from the icon after clicking it
    setTimeout(() => {
      this.blur();
    }, 100);
  });


  // window.addEventListener("resize", () => {
  //   if (sidebarCollapsed === true) {
  //     document.querySelector("#toggle-icon-expand").classList.remove("d-none");
  //     document.querySelector("#toggle-icon-expand").classList.add("d-md-inline");
  //     document.querySelector("#toggle-icon-collapse").classList.add("d-none");
  //     document.querySelector("#toggle-icon-collapse").classList.remove("d-md-inline");
  //   }
  // });


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

const msgAlerts = document.querySelectorAll(".alert");

for (let msg of msgAlerts) {
  if (msg.classList.contains("success")) {
    msg.style.backgroundColor = "rgb(194, 240, 128)";
  } else {
    msg.style.backgroundColor = "#e6646e";
  }
}

const activeTooltips = document.querySelectorAll(".active-tooltip");
for (var activeTooltip of activeTooltips) {
  var tooltip = new bootstrap.Tooltip(activeTooltip, (placement = "top"));
  tooltip.show();
}

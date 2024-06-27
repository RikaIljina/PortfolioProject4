var sidebarCollapsed = true;
var sidebarAutoCollapse = false;
const sideBar = document.getElementById("sidebar");
// var sideBarState = getComputedStyle(sideBar).position;

// Prevent filter items from collapsing once opened (on large screens)
window.addEventListener("DOMContentLoaded", function () {
  setMsgColor();
  activateTooltips();

  const noSidebar = document.querySelector(".no-sidebar");
  if (noSidebar) {
    sideBar.classList.add("d-none");
  } else {
    var filterLinks = document.getElementsByClassName("filter-link");
    var filterCategories = document.getElementsByClassName("filter-cat");
    const sideBar = document.getElementById("sidebar");
    var sideBarState = getComputedStyle(sideBar).position;

    // Check whether the user is on a mobile device
    if (sideBarState === "absolute") {
      sidebarAutoCollapse = true;
    } else {
      sidebarAutoCollapse = false;
    }

    // Keep the list of usernames or tags expanded if the user is not on a
    // mobile device and if they already clicked on a filter and the view
    // shows a filtered selection of entries
    for (let filterCat of filterCategories) {
      if (!sidebarAutoCollapse && filterCat.classList.contains("force-show")) {
        expandSidebar();
        filterCat.classList.add("show");
        break;
      } else if (
        !sidebarAutoCollapse &&
        filterCat.classList.contains("force-show")
      ) {
        filterCat.classList.remove("show");
      }
    }

    for (let link of filterLinks) {
      link.addEventListener("click", function () {
        // If the user clicks on an expandable item, no matter on what device, and
        // the sidebar is collapsed, the sidebar will be expanded
        if (link.getAttribute("aria-expanded") === "true" && sidebarCollapsed) {
          expandSidebar();
        }
        setTimeout(() => {
          document.querySelector("#about-link-container").style.width =
            getComputedStyle(sideBar).width;
        }, 200);
      });
    }

    document.querySelector("#about-link-container").style.width =
      getComputedStyle(sideBar).width;

    if (sideBarState === "absolute") {
      // let newHeight = getComputedStyle(sideBar).height;
      let newHeight = getComputedStyle(
        document.querySelector(".main-content")
      ).height; //style.minHeight; // = newHeight; //`calc(${getComputedStyle(sideBar).height} + 10rem);` //"calc(100vh + 10rem)";
      document.querySelector("#sidebar").style.height = newHeight;
    }

    document
      .getElementById("sidebar-toggle-btn")
      .addEventListener("click", function () {
        if (sidebarCollapsed) {
          expandSidebar();
        } else {
          collapseSidebar();
        }

        // Use setTimeout to remove focus from the icon after clicking it
        setTimeout(() => {
          this.blur();
        }, 100);
      });

    window.addEventListener("resize", () => {
      var sideBarState = getComputedStyle(sideBar).position;
      if (sideBarState === "absolute") {
        sidebarAutoCollapse = true;
      } else {
        sidebarAutoCollapse = false;
      }

      if (sideBarState === "absolute") {
        // let newHeight = getComputedStyle(sideBar).height;
        let newHeight = getComputedStyle(
          document.querySelector(".main-content")
        ).height; //style.minHeight; // = newHeight; //`calc(${getComputedStyle(sideBar).height} + 10rem);` //"calc(100vh + 10rem)";
        document.querySelector("#sidebar").style.height = newHeight;
      }
      document.querySelector("#about-link-container").style.width =
        getComputedStyle(sideBar).width;
    });

    window.addEventListener("scroll", function () {
      const aboutLink = document.querySelector("#about-link-container");
      const menu = document.querySelector("#menu");
      const menuBottom = menu.getBoundingClientRect().bottom;
      const aboutLinkTop = aboutLink.getBoundingClientRect().top;

      if (aboutLinkTop < menuBottom) {
        aboutLink.classList.add("overlay-shadow");
      } else {
        aboutLink.classList.remove("overlay-shadow");
      }
    });
  }
});

function collapseSidebar() {
  // Toogle button icon
  document.querySelector("#toggle-icon-expand").classList.add("d-inline");
  document.querySelector("#toggle-icon-expand").classList.remove("d-none");
  document.querySelector("#toggle-icon-collapse").classList.add("d-none");
  document.querySelector("#toggle-icon-collapse").classList.remove("d-inline");

  sidebarCollapsed = true;

  // Hide the block with usernames or tags
  var filterCategories = document.getElementsByClassName("filter-cat");
  for (cat of filterCategories) {
    cat.classList.remove("show");
  }

  // Hide all sidebar nav item titles
  var filterTitles = document.getElementsByClassName("filter-title");
  for (title of filterTitles) {
    title.classList.add("d-none");
    title.classList.remove("d-inline");
  }

  sideBar.style.minWidth = "initial";
  document.querySelector("#about-link-container").style.width = "initial";
}

function expandSidebar() {
  // Toogle button icon
  document.querySelector("#toggle-icon-expand").classList.remove("d-inline");
  document.querySelector("#toggle-icon-expand").classList.add("d-none");
  document.querySelector("#toggle-icon-collapse").classList.remove("d-none");
  document.querySelector("#toggle-icon-collapse").classList.add("d-inline");

  sidebarCollapsed = false;

  // Show all sidebar nav item titles
  var filterTitles = document.getElementsByClassName("filter-title");
  for (title of filterTitles) {
    title.classList.remove("d-none");
    title.classList.add("d-inline");
  }

  if (sidebarAutoCollapse) {
    sideBar.style.minWidth = "95%";
  } else {
    sideBar.style.minWidth = "17%";
  }
  document.querySelector("#about-link-container").style.width =
    getComputedStyle(sideBar).width;
}

// The menu toggle button in the navbar has a hover effect that stops working
// once the button is clicked and therefore focused. The following code removes
// the focus from the button.
// document.getElementById("toggler-btn").addEventListener("click", function () {
//   // Use setTimeout to remove focus from the icon after clicking it
//   setTimeout(() => {
//     this.blur();
//   }, 500);
// });

function setMsgColor() {
  const msgAlerts = document.querySelectorAll(".alert");

  for (let msg of msgAlerts) {
    if (msg.classList.contains("success")) {
      msg.style.backgroundColor = "rgb(194, 240, 128)";
    } else {
      msg.style.backgroundColor = "#e6646e";
    }
  }
}

function activateTooltips() {
  // Needed for form field error messages
  const activeTooltips = document.querySelectorAll(".active-tooltip");
  for (var activeTooltip of activeTooltips) {
    var tooltip = new bootstrap.Tooltip(activeTooltip, (placement = "top"));
    tooltip.show();
  }

  const hoverTooltips = document.querySelectorAll(".hover-tooltip");
  for (var hoverTooltip of hoverTooltips) {
    var tooltip = new bootstrap.Tooltip(hoverTooltip, (placement = "top"));
  }
}

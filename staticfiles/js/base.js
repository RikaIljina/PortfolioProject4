/* This script manages:
 * - the sidebar behavior
 * - the color of the info/error messages shown to the user as feedback
 * - tooltip activation
 */

var sidebarCollapsed = false;
var sidebarAutoCollapse = false;
// Check if the user has already changed the sidebar state and it is therefore
// saved in the storage. If not, set it to false.
if (!localStorage.getItem("sidebarCollapsed")) {
  localStorage.setItem("sidebarCollapsed", "false");
}

window.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const noSidebar = document.querySelector(".no-sidebar");

  setMsgColor();
  activateTooltips();

  // Hide sidebar on pages with no sidebar (error pages)
  if (noSidebar) {
    sidebar.classList.add("d-none");
  } else {
    var filterLinks = document.getElementsByClassName("filter-link");
    var filterCategories = document.getElementsByClassName("filter-cat");
    var sidebarPos = getComputedStyle(sidebar).position;

    // Check whether the user is on a mobile device and make sure sidebar collapses automatically.
    // The sidebar position on mobile devices is 'absolute'
    if (sidebarPos === "absolute") {
      sidebarAutoCollapse = true;
      collapseSidebar(sidebar);
    } else {
      sidebarAutoCollapse = false;
      // Check the previous state of the sidebar as set by the toggle button
      if (localStorage.getItem("sidebarCollapsed") === "false") {
        expandSidebar(sidebar);
      } else {
        collapseSidebar(sidebar);
      }
    }

    // Prevent filter items from collapsing once opened (on large screens):
    // Keep the list of usernames or tags expanded if the user is not on a
    // mobile device and if they already clicked on a filter and the view
    // shows a filtered selection of entries.
    // Do not expand the list if the user has collapsed the sidebar in the
    // filter view.
    for (let filterCat of filterCategories) {
      if (
        !sidebarAutoCollapse &&
        filterCat.classList.contains("force-show") &&
        localStorage.getItem("sidebarCollapsed") === "false"
      ) {
        $(filterCat).collapse("show");
        break;
      } else if (
        sidebarAutoCollapse &&
        filterCat.classList.contains("force-show")
      ) {
        collapseSidebar(sidebar);
      }
    }

    for (let link of filterLinks) {
      link.addEventListener("click", function () {
        // If the user clicks on an expandable item, no matter on what device, and
        // the sidebar is collapsed, the sidebar will be expanded
        if (link.getAttribute("aria-expanded") === "true" && sidebarCollapsed) {
          expandSidebar(sidebar);
        }
        // Adjust the 'about' link container with the position 'absolute' at the
        // bottom of the sidebar. Give it some time because it is sometimes
        // too fast and receives the wrong width.
        setTimeout(() => {
          document.querySelector("#about-link-container").style.width =
            getComputedStyle(sidebar).width;
        }, 200);
      });
    }

    // Adjust the 'about' link container with the position 'absolute' at the
    // bottom of the sidebar once everything has been loaded. Give it some time
    // because it is sometimes too fast and receives the wrong width.
    setTimeout(() => {
      document.querySelector("#about-link-container").style.width =
        getComputedStyle(sidebar).width;
    }, 200);

    // Try to adjust the sidebar height on mobile devices to the main content
    // container height
    if (sidebarPos === "absolute") {
      let newHeight = getComputedStyle(
        document.querySelector(".main-content")
      ).height;
      document.querySelector("#sidebar").style.height = newHeight;
    }

    // Toggle button functionality
    document
      .getElementById("sidebar-toggle-btn")
      .addEventListener("click", function () {
        if (sidebarCollapsed) {
          expandSidebar(sidebar);
        } else {
          collapseSidebar(sidebar);
        }

        // Use setTimeout to remove focus from the toggle icon after clicking it
        setTimeout(() => {
          this.blur();
        }, 100);
      });

    // Listen for window resize and adjust the sidebar accordingly
    window.addEventListener("resize", () => {
      var sidebarPos = getComputedStyle(sidebar).position;
      if (sidebarPos === "absolute") {
        sidebarAutoCollapse = true;
      } else {
        sidebarAutoCollapse = false;
      }

      if (sidebarPos === "absolute") {
        let newHeight = getComputedStyle(
          document.querySelector(".main-content")
        ).height;
        document.querySelector("#sidebar").style.height = newHeight;
      }
      setTimeout(() => {
        document.querySelector("#about-link-container").style.width =
          getComputedStyle(sidebar).width;
      }, 200);
    });

    // Listen for scrolling and adjust the 'about' link container at the bottom
    // to give it a shadow if it overlays other sidebar elements
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

/** This function handles all processes needed to collapse the sidebar.
 */
function collapseSidebar(sidebar) {
  // Toogle button icon
  document.querySelector("#toggle-icon-expand").classList.add("d-inline");
  document.querySelector("#toggle-icon-expand").classList.remove("d-none");
  document.querySelector("#toggle-icon-collapse").classList.add("d-none");
  document.querySelector("#toggle-icon-collapse").classList.remove("d-inline");

  // Remember the new sidebar state
  sidebarCollapsed = true;
  localStorage.setItem("sidebarCollapsed", sidebarCollapsed);

  // Hide the block with usernames or tags
  var filterCategories = document.getElementsByClassName("filter-cat");
  for (let cat of filterCategories) {
    $(cat).collapse("hide");
    cat.classList.remove("force-show");
  }

  // Hide all sidebar nav item titles
  var filterTitles = document.getElementsByClassName("filter-title");
  for (let title of filterTitles) {
    title.classList.add("d-none");
    title.classList.remove("d-inline");
  }

  // Reset the sidebar width
  sidebar.style.minWidth = "initial";
  document.querySelector("#about-link-container").style.width = "initial";
}

/** This function handles all processes needed to expand the sidebar.
 */
function expandSidebar(sidebar) {
  // Toogle button icon
  document.querySelector("#toggle-icon-expand").classList.remove("d-inline");
  document.querySelector("#toggle-icon-expand").classList.add("d-none");
  document.querySelector("#toggle-icon-collapse").classList.remove("d-none");
  document.querySelector("#toggle-icon-collapse").classList.add("d-inline");

  // Remember the new sidebar state
  sidebarCollapsed = false;
  localStorage.setItem("sidebarCollapsed", sidebarCollapsed);

  // Show all sidebar nav item titles
  var filterTitles = document.getElementsByClassName("filter-title");
  for (let title of filterTitles) {
    title.classList.remove("d-none");
    title.classList.add("d-inline");
  }

  // Set the sidebar width
  if (sidebarAutoCollapse) {
    sidebar.style.minWidth = "95%";
  } else {
    sidebar.style.minWidth = "17%";
  }

  // Adjust the 'about' link container with the position 'absolute' at the
  // bottom of the sidebar. Give it some time because it is sometimes
  // too fast and receives the wrong width.
  setTimeout(() => {
    document.querySelector("#about-link-container").style.width =
      getComputedStyle(sidebar).width;
  }, 200);
}

/** This function sets a green or red background color for messages at the top of
 * the main content container depending on the type of the message.
 */
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

/** Finds all elements that use bootstrap tooltips and initializes them.
 * Always shows active tooltips which are used to display errors on login/signup
 * form fields.
 *  activeTooltips - Elements that show tooltips once they receive a text value
 *  hoverTooltips  - Elements that show tooltips on hover
 */

function activateTooltips() {
  const activeTooltips = document.querySelectorAll(".active-tooltip");
  const hoverTooltips = document.querySelectorAll(".hover-tooltip");

  for (let activeTooltip of activeTooltips) {
    let tooltip = new bootstrap.Tooltip(activeTooltip, (placement = "top"));
    tooltip.show();
    activeTooltip.addEventListener("hide.bs.tooltip", (e) => {
      e.preventDefault();
    });
  }

  for (let hoverTooltip of hoverTooltips) {
    let tooltip = new bootstrap.Tooltip(hoverTooltip, (placement = "top"));
  }
}

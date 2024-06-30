var sidebarCollapsed = true;
var sidebarAutoCollapse = false;
const sidebar = document.getElementById("sidebar");

window.addEventListener("DOMContentLoaded", function () {
  setMsgColor();
  activateTooltips();

  // Hide sidebar on pages with no sidebar (error pages)
  const noSidebar = document.querySelector(".no-sidebar");
  if (noSidebar) {
    sidebar.classList.add("d-none");
  } else {
    var filterLinks = document.getElementsByClassName("filter-link");
    var filterCategories = document.getElementsByClassName("filter-cat");
    const sidebar = document.getElementById("sidebar");
    var sidebarPos = getComputedStyle(sidebar).position;

    // Check whether the user is on a mobile device
    if (sidebarPos === "absolute") {
      sidebarAutoCollapse = true;
      collapseSidebar();
    } else {
      sidebarAutoCollapse = false;
    }

    if (localStorage.getItem("sidebarCollapsed") === "false") {
      expandSidebar();
    }

    // Prevent filter items from collapsing once opened (on large screens)
    // Keep the list of usernames or tags expanded if the user is not on a
    // mobile device and if they already clicked on a filter and the view
    // shows a filtered selection of entries
    for (let filterCat of filterCategories) {
      if (!sidebarAutoCollapse && filterCat.classList.contains("force-show") &&
        localStorage.getItem("sidebarCollapsed") === "false") {
        $(filterCat).collapse('show');
        break;
      } else if (
        sidebarAutoCollapse &&
        filterCat.classList.contains("force-show")
      ) {
        alert(sidebarAutoCollapse);
        collapseSidebar();
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
            getComputedStyle(sidebar).width;
        }, 200);
      });
    }

    document.querySelector("#about-link-container").style.width =
      getComputedStyle(sidebar).width;

    if (sidebarPos === "absolute") {
      let newHeight = getComputedStyle(
        document.querySelector(".main-content")
      ).height;
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
      document.querySelector("#about-link-container").style.width =
        getComputedStyle(sidebar).width;
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
  localStorage.setItem("sidebarCollapsed", sidebarCollapsed);

  // Hide the block with usernames or tags
  var filterCategories = document.getElementsByClassName("filter-cat");
  for (let cat of filterCategories) {
    alert(cat);
    $(cat).collapse("hide");
    cat.classList.remove("force-show");
  }

  // Hide all sidebar nav item titles
  var filterTitles = document.getElementsByClassName("filter-title");
  for (let title of filterTitles) {
    title.classList.add("d-none");
    title.classList.remove("d-inline");
  }

  sidebar.style.minWidth = "initial";
  document.querySelector("#about-link-container").style.width = "initial";
}

function expandSidebar() {
  // Toogle button icon
  document.querySelector("#toggle-icon-expand").classList.remove("d-inline");
  document.querySelector("#toggle-icon-expand").classList.add("d-none");
  document.querySelector("#toggle-icon-collapse").classList.remove("d-none");
  document.querySelector("#toggle-icon-collapse").classList.add("d-inline");

  sidebarCollapsed = false;
  localStorage.setItem("sidebarCollapsed", sidebarCollapsed);

  // Show all sidebar nav item titles
  var filterTitles = document.getElementsByClassName("filter-title");
  for (let title of filterTitles) {
    title.classList.remove("d-none");
    title.classList.add("d-inline");
  }

  if (sidebarAutoCollapse) {
    sidebar.style.minWidth = "95%";
  } else {
    sidebar.style.minWidth = "17%";
  }
  document.querySelector("#about-link-container").style.width =
    getComputedStyle(sidebar).width;
}

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
 *  @type {NodeList object} activeTooltips - Elements that show tooltips once they receive a text value
 *  @type {NodeList object} hoverTooltips  - Elements that show tooltips on hover
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

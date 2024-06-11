const userFilter = document.getElementById("filter-user");

userFilter.addEventListener("click", (e) => {
  let showLabel = e.target.parentElement.getAttribute("class"); //.nextSibling; //.getAttribute("class");
  alert(showLabel.includes("collapsed"))
  // are there params in the link?
  if (window.location.href.includes("?")) {
    let param_list = window.location.href.split("?");
    alert(param_list);
    var clean_link = param_list[0];
    var new_params = [];
    var old_params = param_list[1].split('&');
    alert(param_list.slice(1));
    for (item of old_params) {
      if (item && !item.includes("filter")) {
        alert(item);
        alert("inside if");
        // make list without filter param
        new_params.push(item);
      }
    }
    
    alert(new_params.length)
    if (new_params.length != 0) {
        temp = new_params.join("&");
        alert(temp)
      new_params = `?${temp}`;
    alert("param join");
    alert(`new link should be`);
    alert(`${clean_link}${new_params}`);
 
    } else {
      new_params = "";
    }
  } else {
    var clean_link = window.location.href;
    var new_params = "";
    alert("inside else");
  }

  if (showLabel.includes("collapsed")) {
    alert("collapsed");
    alert(`${clean_link}${new_params}`);
    // go to link with old params but not filter param
    window.location.href = `${clean_link}${new_params}`;
  } else {
    if (new_params) {
        alert('inside &')
      window.location.href = `${clean_link}${new_params}&filter=users`;
    } else {
        alert('inside ?')

      window.location.href = `${clean_link}?filter=users`;
    }
  }
});

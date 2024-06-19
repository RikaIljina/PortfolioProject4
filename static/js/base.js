

// The menu toggle button in the navbar has a hover effect that stops working 
// once the button is clicked and therefore focused. The following code removes
// the focus from the button.
document.getElementById('toggler-btn').addEventListener('click', function() {
    // Use setTimeout to remove focus from the icon after clicking it
    setTimeout(() => {
        this.blur();
    }, 100);
});

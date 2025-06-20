// Shows the filename next to them when file inputs change
document.addEventListener("DOMContentLoaded", () => {
    // Finds every file input on the page
    document.querySelectorAll("input[type = 'file']".forEach(input => {
        const filenameDisplay = document.createElement("span");
        filenameDisplay.className = "file-name";
        filenameDisplay.style.marginLeft = "0.5rem";

        // Inserts it right after the input
        input.parentNode.insertBefore(filenameDisplay, input.nextSibling);

        // Updates the span when a user selects a file
        input.addEventListener("change", () => {
            if(input.files && input.files.length > 0){
                filenameDisplay.textContent = input.files[0].name;
            }
            else{
                filenameDisplay.nextContent = "";
            }
        });
    }));
});
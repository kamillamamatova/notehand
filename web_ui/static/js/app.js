/* This event listener waits for the entire HTML document to be loaded and parsed before running
the code inside it. This prevents errors from trying to find elements that haven't been created yet */
document.addEventListener("DOMContentLoaded", () => {
    // Grabs inputs, buttons, and preview containers
    const templateInput = document.querySelector('input[name = "template"]');
    const txtInput = document.querySelector('input[name = "transcript"]');
    // Selects the button with id="segment-btn"
    const segBtn = document.querySelector('#segment-btn');
    // Selects the button with id="render-btn"
    const renderBtn = document.querySelector('#render-btn');
    // Selects the div with id="template-preview"
    const templatePreview = document.querySelector('#template-preview');
    // Selects the div with id="transcript-preview"
    const transcriptPreview = document.querySelector('#transcript-preview');

    // Disable buttons initially
    if(segBtn) segBtn.disabled = true;
    if(renderBtn) renderBtn.disabled = true;

    // Enhances the template upload input
    // Only adds the listener if the template input element exists
    if (templateInput){
        // 'change' is the event that fires when the user selects a file
        templateInput.addEventListener("change", () => {
            // Clears previous preview content
            templatePreview.innerHTML = "";

            const file = templateInput.files[0];

            // If no file is selected, disable the button and return
            if(!file){
                segBtn.disabled = true;
                return;
            }

            // Shows filename
            const nameSpan = document.createElement("span");
            // Assigns it to a class for styling
            nameSpan.className = "file-name";
            // Sets the text content to the file name
            nameSpan.textContent = file.name;
            // Adds the span to the preview area
            templatePreview.appendChild(nameSpan);
            
            // Shows a live thumbnail
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            // Releases the memory used by the temporary URL once the image is loaded
            img.onload = () => URL.revokeObjectURL(img.src);
            // Adds the image to the preview area
            templatePreview.appendChild(img);

            // Enables button
            segBtn.disabled = false;
        });
    }

    // Enhances the transcript upload inpit
    if(txtInput){
        txtInput.addEventListener("change", () => {
            // Clears previous preview content
            transcriptPreview.innerHTML = "";
            const file = txtInput.files[0];

            // If no file is selected, disable the button and return
            if(!file){
                renderBtn.disabled = true;
                return;
            }

            // Displays filename
            const nameSpan = document.createElement("span");
            nameSpan.className = "file-name";
            nameSpan.textContent = file.name;
            transcriptPreview.appendChild(nameSpan);

            // Enables button
            renderBtn.disabled = false;
        });
    }
});
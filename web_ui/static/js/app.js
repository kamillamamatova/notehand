// Shows the filename next to them when file inputs change
document.addEventListener("DOMContentLoaded", () => {
    // Grabs inputs, buttons, and preview containers
    const templateInput = document.querySelector('input[name = "template"]');
    const txtInput = document.querySelector('input[name = "transcript"]');
    const segBtn = document.querySelector('#segment-btn');
    const renderBtn = document.querySelector('#render-btn');
    const templatePreview = document.querySelector('template-preview');
    const txtPreview = document.querySelector('transcript-preview');

    // Buttons disabled
    segBtn.disabled = true;
    renderBtn.disabled = true;

    // Enhances the template upload input with filename and live image preview
    templateInput.addEventListener("change", () => {
        // Clears any old preview
        templatePreview.innerHTML = "";

        const file = templateInput.files[0];
        if(!file){
            segBtn.disabled = true;
            return;
        }

        // Shows the filename
        let nameSpan = templateInput.nextElementSibling;
        if(!nameSpan || !nameSpan.classList.contains("file-name")){
            nameSpan = document.createElement("span");
            nameSpan.className = "file-name";
            nameSpan.style.marginLeft = "0.5rem";
            templateInput.parentNode.insertBefore(nameSpan, templateInput.nextSibling);
        }
        nameSpan.textContent = file.name;

        // Shows a live thumbnail
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.onload = () => URL.revokeObjectURL(img.src);
        img.style.maxWidth = "100%";
        img.style.marginTop = "1rem";
        templePrev.appendChild(img);

        // Enables the segment button
        segBtn.disabled = false;
    });

    // Enhances the transcript upload input with filename display
    txtInput.addEventListener("change", () => {
        // Displays filename in its preview container
        txtPrev.textContent = txtInput.files[0]?.name || "";

        // Enables the render button if a file is chosen
        renderBtn.disabled = txtInput.files.length == 0;
    });
});
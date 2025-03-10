function generateSound() {
    let effectText = document.getElementById("soundText").value;
    
    if (!effectText) {
        alert("Please enter a sound effect name!");
        return;
    }

    let formData = new FormData();
    formData.append("effect", effectText);

    fetch("/generate/", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            let audioContainer = document.getElementById("audioContainer");
            audioContainer.innerHTML = `
                <audio controls>
                    <source src="${data.audio_url}" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
                <br>
                <a href="${data.audio_url}" download>Download Sound</a>
            `;
        })
        .catch(error => console.error("Error:", error));
}

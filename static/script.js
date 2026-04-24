document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    const voiceSelect = document.getElementById('voice-select');
    const generateBtn = document.getElementById('generate-btn');
    const statusMessage = document.getElementById('status-message');

    async function fetchVoices() {
        const response = await fetch('/api/voices');
        const voices = await response.json();
        voices.forEach(voice => {
            const option = document.createElement('option');
            option.value = voice.name;
            option.textContent = `${voice.name} (${voice.gender})`;
            voiceSelect.appendChild(option);
        });
    }

    async function generateAudio() {
        const text = textInput.value.trim();
        const voice = voiceSelect.value;

        if (!text) {
            alert('Please enter some text');
            return;
        }

        generateBtn.disabled = true;
        statusMessage.textContent = 'Generating...';

        try {
            const response = await fetch('/api/speech', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, voice }),
            });

            const result = await response.json();

            if (result.status === 'success') {
                statusMessage.innerHTML = `Saved: <a href="/output/${result.filename}" download>${result.filename}</a>`;
            } else {
                statusMessage.textContent = 'Error: ' + result.detail;
            }
        } catch (error) {
            statusMessage.textContent = 'Error: ' + error;
        } finally {
            generateBtn.disabled = false;
        }
    }

    generateBtn.addEventListener('click', generateAudio);
    fetchVoices();
});
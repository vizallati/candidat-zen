document.addEventListener('DOMContentLoaded', function () {
    // Fade in the form when the page loads
    const form = document.getElementById('scriptForm');
    form.style.display = 'block';

    // Add animation when clicking the "Apply for jobs" button
    const runButton = document.getElementById('runButton');
    const resultDiv = document.getElementById('result');

    runButton.addEventListener('click', async () => {
        resultDiv.innerText = 'Running...';

        try {
            const formData = new FormData(form);
            const response = await fetch('http://127.0.0.1:5000/apply', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.result) {
                resultDiv.innerText = data.result;

                // Add animation when displaying the result
                resultDiv.style.display = 'block';
            } else {
                resultDiv.innerText = 'An error occurred.';
            }
        } catch (error) {
            resultDiv.innerText = 'Error: ' + error.message;
        }
    });
});

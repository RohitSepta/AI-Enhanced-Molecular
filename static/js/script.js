function generateResponse() {
    const textInput = document.getElementById('textInput');
    const responseElement = document.getElementById('response');

    // Check if the textarea element is found
    if (!textInput) {
        console.error('Textarea element not found');
        return;
    }

    // Get the value of the textarea
    const text = textInput.value;

    // Check if the text is empty
    if (!text.trim()) {
        responseElement.textContent = 'Please enter a message.';
        return;
    }

    // Make a request to the server to generate a response
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            responseElement.textContent = 'Error: ' + data.error;
        } else {
            responseElement.textContent = data.response;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        responseElement.textContent = 'An error occurred. Please try again later.';
    });
}
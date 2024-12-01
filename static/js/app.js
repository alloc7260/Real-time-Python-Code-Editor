// Establish WebSocket connection with the server
const socket = io.connect('http://' + document.domain + ':' + location.port);

// Initialize CodeMirror editor
const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'python',
    lineNumbers: true,
    theme: 'default',
    matchBrackets: true
});

// Event listener to detect changes in the code editor
editor.on('keyup', function (cm, event) {
    const code = cm.getValue(); // Get current code from editor
    socket.emit('code_change', code); // Send code to server via WebSocket
});

editor.on('change', function (cm, change) {
    const code = cm.getValue(); // Get current code from editor
    socket.emit('code_change', code); // Send code to server via WebSocket
});

// Handle the output from the server
socket.on('output', function (data) {
    document.getElementById('output').textContent = data.output;
});

// Handle Dark Mode toggle
document.getElementById('dark-mode-toggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
    const darkMode = document.body.classList.contains('dark-mode');

    // Store dark mode preference in localStorage
    localStorage.setItem('darkMode', darkMode);
});

// Check for dark mode preference on page load
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Handle file input (importing a Python file)
function loadFile(event) {
    const file = event.target.files[0]; // Get the selected file
    if (file && file.name.endsWith('.py')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const fileContent = e.target.result; // Get the content of the file
            editor.setValue(fileContent); // Load the content into the editor
        };
        reader.readAsText(file); // Read the file as text
    } else {
        alert('Please select a valid Python file (.py)');
    }

    // Clear the file input
    event.target.value = '';
};

// Establish WebSocket connection with the server
const socket = io.connect('http://' + document.domain + ':' + location.port);

// Initialize CodeMirror editor
const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'python',
    lineNumbers: true,
    matchBrackets: true
});

// Function to handle code changes and emit them to the server
function handleCodeChange(cm) {
    const code = cm.getValue(); // Get current code from editor
    socket.emit('code_change', code); // Send code to server via WebSocket
}

// Attach code change event listeners to the editor
editor.on('keyup', handleCodeChange);
editor.on('change', handleCodeChange);

// Handle the output from the server
socket.on('output', function (data) {
    document.getElementById('output').textContent = data.output;
});

// Function to toggle dark mode
function toggleDarkMode() {
    const darkModeEnabled = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', darkModeEnabled);

    // Update toggle button icon
    document.getElementById('dark-mode-toggle').textContent = darkModeEnabled ? '🌞' : '🌜';
}

// Initialize dark mode based on saved preference
function initializeDarkMode() {
    const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
    document.body.classList.toggle('dark-mode', darkModeEnabled);
    document.getElementById('dark-mode-toggle').textContent = darkModeEnabled ? '🌞' : '🌜';
}

// Handle Dark Mode toggle
document.getElementById('dark-mode-toggle').addEventListener('click', toggleDarkMode);
initializeDarkMode();

// Handle file download
document.getElementById('download-file').addEventListener('click', function () {
    const code = editor.getValue(); // Get the current code from the editor
    const blob = new Blob([code], { type: 'text/plain' }); // Create a Blob with the code content
    const a = document.createElement('a'); // Create an anchor element
    a.href = URL.createObjectURL(blob); // Create a downloadable object URL
    a.download = 'code.py'; // Set the default file name
    a.click(); // Trigger the download
});

// Handle file upload
document.getElementById('upload-file').addEventListener('click', function () {
    document.getElementById('file').click(); // Programmatically trigger the file input click
});

// Handle file input (importing a Python file)
function loadFile(event) {
    const file = event.target.files[0]; // Get the selected file
    if (file && file.name.endsWith('.py')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            editor.setValue(e.target.result); // Load the content into the editor
        };
        reader.readAsText(file); // Read the file as text
    } else {
        alert('Please select a valid Python file (.py)');
    }

    // Clear the file input
    event.target.value = '';
}

// Attach the file input change event listener
document.getElementById('file').addEventListener('change', loadFile);

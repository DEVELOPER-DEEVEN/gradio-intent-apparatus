"""
Simple web server for the Intent Apparatus using built-in Python libraries.
This provides a basic web interface without requiring Gradio.
"""

import http.server
import socketserver
import json
import urllib.parse
from demo import SimpleWebInterface


class IntentApparatusHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for the Intent Apparatus web interface."""
    
    def __init__(self, *args, **kwargs):
        self.interface = SimpleWebInterface()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.serve_html()
        elif self.path == '/style.css':
            self.serve_css()
        elif self.path == '/script.js':
            self.serve_js()
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/execute':
            self.handle_command()
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_html(self):
        """Serve the main HTML page."""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Intent Apparatus</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎯 Intent Apparatus</h1>
            <p>Natural Language OS Automation Tool</p>
        </header>
        
        <div class="warning-box">
            <strong>⚠️ Safety Warning:</strong> This tool can control your mouse and keyboard. 
            Currently running in DEMO mode with simulated actions.
            Install pyautogui for real automation.
        </div>
        
        <div class="main-content">
            <div class="input-section">
                <h3>Enter Command</h3>
                <textarea id="commandInput" placeholder='e.g., "click at 100, 200" or "type &quot;Hello World&quot;" or "press enter"'></textarea>
                <button id="executeBtn">🚀 Execute</button>
            </div>
            
            <div class="output-section">
                <h3>Result</h3>
                <div id="status"></div>
                <div id="message"></div>
            </div>
            
            <div class="history-section">
                <h3>Execution History</h3>
                <div id="history">No commands executed yet.</div>
                <button id="clearBtn">🗑️ Clear History</button>
            </div>
            
            <div class="examples-section">
                <h3>Command Examples</h3>
                <div class="examples">
                    <h4>MOUSE ACTIONS:</h4>
                    <ul>
                        <li>click at 100, 200</li>
                        <li>right click at 300, 400</li>
                        <li>double click at 150, 250</li>
                        <li>move mouse to 500, 600</li>
                    </ul>
                    
                    <h4>KEYBOARD ACTIONS:</h4>
                    <ul>
                        <li>type "Hello World"</li>
                        <li>press enter</li>
                        <li>ctrl+c</li>
                        <li>alt+tab</li>
                    </ul>
                    
                    <h4>OTHER ACTIONS:</h4>
                    <ul>
                        <li>scroll up</li>
                        <li>scroll down 5</li>
                        <li>take a screenshot</li>
                        <li>capture screen</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <script src="/script.js"></script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_css(self):
        """Serve the CSS stylesheet."""
        css_content = """
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 15px;
    padding: 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    overflow: hidden;
}

.header {
    text-align: center;
    padding: 30px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin: 0;
}

.header h1 {
    margin: 0;
    font-size: 2.5em;
}

.header p {
    margin: 10px 0 0 0;
    opacity: 0.9;
}

.warning-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 15px;
    margin: 20px;
    color: #856404;
}

.main-content {
    padding: 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.input-section, .output-section, .history-section, .examples-section {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #dee2e6;
}

.input-section {
    grid-column: 1;
}

.output-section {
    grid-column: 2;
}

.history-section {
    grid-column: 1 / -1;
}

.examples-section {
    grid-column: 1 / -1;
}

h3 {
    margin: 0 0 15px 0;
    color: #495057;
}

#commandInput {
    width: 100%;
    height: 80px;
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 5px;
    font-size: 14px;
    resize: vertical;
    font-family: inherit;
}

#executeBtn, #clearBtn {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    margin-top: 10px;
    transition: background-color 0.2s;
}

#executeBtn:hover, #clearBtn:hover {
    background: #0056b3;
}

#clearBtn {
    background: #6c757d;
}

#clearBtn:hover {
    background: #545b62;
}

#status {
    font-weight: bold;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
}

.success {
    color: #155724;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
}

.error {
    color: #721c24;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
}

#message, #history {
    background: white;
    padding: 10px;
    border: 1px solid #dee2e6;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
}

.examples {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.examples h4 {
    margin: 0 0 10px 0;
    color: #007bff;
}

.examples ul {
    margin: 0;
    padding-left: 20px;
}

.examples li {
    margin: 5px 0;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    color: #6c757d;
}

@media (max-width: 768px) {
    .main-content {
        grid-template-columns: 1fr;
    }
    
    .input-section, .output-section {
        grid-column: 1;
    }
}
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(css_content.encode())
    
    def serve_js(self):
        """Serve the JavaScript code."""
        js_content = """
document.addEventListener('DOMContentLoaded', function() {
    const commandInput = document.getElementById('commandInput');
    const executeBtn = document.getElementById('executeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const status = document.getElementById('status');
    const message = document.getElementById('message');
    const history = document.getElementById('history');
    
    let executionHistory = [];
    
    function executeCommand() {
        const command = commandInput.value.trim();
        if (!command) {
            showStatus('error', 'Please enter a command.');
            return;
        }
        
        executeBtn.disabled = true;
        executeBtn.textContent = '⏳ Executing...';
        
        fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({command: command})
        })
        .then(response => response.json())
        .then(data => {
            showStatus(data.success ? 'success' : 'error', data.status);
            message.textContent = data.message;
            
            // Add to history
            const historyItem = `${executionHistory.length + 1}. ${data.success ? '✅' : '❌'} '${command}' - ${data.message}`;
            executionHistory.push(historyItem);
            updateHistory();
            
            // Clear input on success
            if (data.success) {
                commandInput.value = '';
            }
        })
        .catch(error => {
            showStatus('error', 'Network error: ' + error.message);
            message.textContent = 'Failed to execute command due to network error.';
        })
        .finally(() => {
            executeBtn.disabled = false;
            executeBtn.textContent = '🚀 Execute';
        });
    }
    
    function showStatus(type, text) {
        status.className = type;
        status.textContent = text;
    }
    
    function updateHistory() {
        if (executionHistory.length === 0) {
            history.textContent = 'No commands executed yet.';
        } else {
            history.textContent = executionHistory.slice(-10).join('\\n');
        }
    }
    
    function clearHistory() {
        executionHistory = [];
        updateHistory();
        showStatus('success', 'History cleared');
        message.textContent = '';
    }
    
    // Event listeners
    executeBtn.addEventListener('click', executeCommand);
    clearBtn.addEventListener('click', clearHistory);
    
    // Execute on Enter (Ctrl+Enter for new line)
    commandInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.ctrlKey && !e.shiftKey) {
            e.preventDefault();
            executeCommand();
        }
    });
    
    // Focus on command input
    commandInput.focus();
});
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(js_content.encode())
    
    def handle_command(self):
        """Handle command execution requests."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            command = data.get('command', '')
            status, message = self.interface.process_command(command)
            
            success = status.startswith('✅')
            
            response = {
                'success': success,
                'status': status,
                'message': message
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                'success': False,
                'status': '❌ Error',
                'message': f'Server error: {str(e)}'
            }
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())


def start_server(port=8080):
    """Start the web server."""
    # Create a custom handler class with the interface
    class CustomHandler(IntentApparatusHandler):
        def __init__(self, *args, **kwargs):
            self.interface = SimpleWebInterface()
            super(http.server.BaseHTTPRequestHandler, self).__init__(*args, **kwargs)
    
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"🎯 Intent Apparatus Web Server starting...")
        print(f"🌐 Server running at http://localhost:{port}")
        print(f"⚠️  Currently in DEMO mode (simulated actions)")
        print(f"📝 Install pyautogui for real OS automation")
        print(f"🛑 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped.")


if __name__ == "__main__":
    start_server()
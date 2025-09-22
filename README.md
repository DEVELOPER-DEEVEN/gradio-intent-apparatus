# 🎯 Gradio Intent Apparatus

An intelligent automation tool that allows users to control their operating system using natural language commands. Simply describe what you want to do, and the Intent Apparatus will execute mouse clicks, keyboard inputs, and other OS interactions for you.

## ✨ Features

- **Natural Language Processing**: Convert everyday language into precise OS actions
- **Mouse Control**: Click at specific coordinates, move mouse, right-click, double-click
- **Keyboard Automation**: Type text, press keys, execute key combinations
- **Screen Capture**: Take screenshots automatically after certain actions
- **Web Interface**: User-friendly Gradio-based interface
- **Safety Features**: Built-in failsafe mechanisms and error handling
- **Execution History**: Track and review all executed commands

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/DEVELOPER-DEEVEN/gradio-intent-apparatus.git
cd gradio-intent-apparatus

# Run the setup script
python setup.py

# Or install dependencies manually
pip install -r requirements.txt
```

### 2. Launch the Application

```bash
python app.py
```

The web interface will be available at `http://localhost:7860`

## 📝 Command Examples

### Mouse Actions
- `click at 100, 200` - Left click at coordinates (100, 200)
- `right click at 300, 400` - Right click at coordinates (300, 400)
- `double click at 150, 250` - Double click at coordinates (150, 250)
- `move mouse to 500, 600` - Move mouse cursor to coordinates (500, 600)

### Keyboard Actions
- `type "Hello World"` - Type the specified text
- `press enter` - Press the Enter key
- `press ctrl+c` - Press Ctrl+C combination
- `hit the space key` - Press the space bar
- `alt+tab` - Switch between applications

### Scrolling
- `scroll up` - Scroll up 3 times (default)
- `scroll down 5` - Scroll down 5 times
- `scroll 3 times up` - Scroll up 3 times

### Screen Capture
- `take a screenshot` - Capture the current screen
- `capture screen` - Same as above
- `screenshot` - Take a screenshot

## ⚠️ Safety Information

### Important Warnings
- **This tool can control your mouse and keyboard** - Use with extreme caution
- **Test in a safe environment** - Close important applications before testing
- **Failsafe mechanism** - Move your mouse to any corner of the screen to stop all automation
- **No undo function** - Actions are executed immediately and cannot be undone

### Best Practices
1. **Start with simple commands** like taking screenshots or moving the mouse
2. **Verify coordinates** before clicking - use screenshot tools to identify positions
3. **Keep sensitive applications closed** while testing
4. **Use in a controlled environment** away from important work

## 🛠️ Technical Details

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux with GUI
- **Dependencies**: See `requirements.txt`

### Core Components
- **`automation_engine.py`**: Low-level OS interaction using PyAutoGUI
- **`intent_parser.py`**: Natural language processing and command parsing
- **`app.py`**: Gradio web interface and application logic

### Architecture
```
User Input (Natural Language)
         ↓
    Intent Parser
         ↓
   Automation Engine
         ↓
    OS Actions (Mouse/Keyboard)
```

## 🔧 Development

### Project Structure
```
gradio-intent-apparatus/
├── app.py                 # Main application
├── automation_engine.py   # OS automation logic
├── intent_parser.py       # NLP command parsing
├── requirements.txt       # Python dependencies
├── setup.py              # Installation script
└── README.md             # This file
```

### Adding New Commands
1. Add regex patterns to `intent_parser.py`
2. Implement action logic in `automation_engine.py`
3. Update the command execution logic in `app.py`

## 🐛 Troubleshooting

### Common Issues

**"PyAutoGUI can't find display"**
- Ensure you're running in a GUI environment
- On Linux, check that `DISPLAY` environment variable is set

**"Permission denied for accessibility"**
- On macOS: Grant accessibility permissions in System Preferences
- On Linux: Ensure your user has access to input devices

**"Commands not recognized"**
- Check the command examples in the web interface
- Ensure proper spelling and format
- Use quotes around text to be typed

**"Failsafe triggered"**
- Mouse moved to screen corner - this is a safety feature
- Restart the application to continue

### Getting Help
1. Check the command examples in the web interface
2. Review the execution history for error messages
3. Ensure all dependencies are properly installed
4. Test with simple commands first

## 📄 License

This project is open source. Please use responsibly and in accordance with your local laws and regulations.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## ⚖️ Disclaimer

This tool is for educational and automation purposes. Users are responsible for:
- Ensuring compliance with local laws and regulations
- Using the tool safely and responsibly
- Not using it for malicious purposes
- Understanding the risks of automated OS control

**Use at your own risk. The developers are not responsible for any damage or misuse of this tool.**
"""
Main Gradio application for the Intent Apparatus automation tool.
"""

import gradio as gr
import time
import os
from typing import List, Tuple
from automation_engine import AutomationEngine, ActionResult
from intent_parser import IntentParser, ParsedIntent


class IntentApparatus:
    """Main application class for the Intent Apparatus."""
    
    def __init__(self):
        self.automation_engine = AutomationEngine()
        self.intent_parser = IntentParser()
        self.execution_history: List[Tuple[str, ActionResult]] = []
    
    def process_command(self, command: str) -> Tuple[str, str, str]:
        """Process a natural language command and execute the action."""
        if not command.strip():
            return "❌ Error", "Please enter a command.", ""
        
        # Parse the command
        parsed_intent = self.intent_parser.parse_command(command)
        
        if not parsed_intent:
            examples = self._get_example_commands()
            return (
                "❌ Unable to parse command", 
                f"Could not understand the command: '{command}'\n\n{examples}",
                ""
            )
        
        # Execute the action
        result = self._execute_action(parsed_intent)
        
        # Store in history
        self.execution_history.append((command, result))
        
        # Format response
        status = "✅ Success" if result.success else "❌ Error"
        message = result.message
        
        # Take screenshot for certain actions
        screenshot_path = ""
        if result.success and parsed_intent.action_type in ['click', 'move', 'screenshot']:
            screenshot_path = self.automation_engine.take_screenshot()
            if screenshot_path:
                screenshot_path = os.path.abspath(screenshot_path)
        
        return status, message, screenshot_path
    
    def _execute_action(self, intent: ParsedIntent) -> ActionResult:
        """Execute an automation action based on parsed intent."""
        try:
            if intent.action_type == 'click':
                x = intent.parameters.get('x')
                y = intent.parameters.get('y')
                button = intent.parameters.get('button', 'left')
                clicks = intent.parameters.get('clicks', 1)
                
                if clicks == 2:
                    # Double click
                    self.automation_engine.click_at_position(x, y, button)
                    time.sleep(0.1)
                    return self.automation_engine.click_at_position(x, y, button)
                else:
                    return self.automation_engine.click_at_position(x, y, button)
            
            elif intent.action_type == 'type':
                text = intent.parameters.get('text')
                return self.automation_engine.type_text(text)
            
            elif intent.action_type == 'key':
                if 'keys' in intent.parameters:
                    keys = intent.parameters['keys']
                    return self.automation_engine.key_combination(keys)
                else:
                    key = intent.parameters.get('key')
                    return self.automation_engine.press_key(key)
            
            elif intent.action_type == 'scroll':
                direction = intent.parameters.get('direction')
                clicks = intent.parameters.get('clicks', 3)
                return self.automation_engine.scroll(direction, clicks)
            
            elif intent.action_type == 'move':
                x = intent.parameters.get('x')
                y = intent.parameters.get('y')
                return self.automation_engine.move_mouse(x, y)
            
            elif intent.action_type == 'screenshot':
                screenshot_path = self.automation_engine.take_screenshot()
                if screenshot_path:
                    return ActionResult(
                        success=True,
                        message=f"Screenshot saved as {screenshot_path}",
                        action_type="screenshot"
                    )
                else:
                    return ActionResult(
                        success=False,
                        message="Failed to take screenshot",
                        action_type="screenshot"
                    )
            
            else:
                return ActionResult(
                    success=False,
                    message=f"Unknown action type: {intent.action_type}",
                    action_type="unknown"
                )
        
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Execution error: {str(e)}",
                action_type=intent.action_type
            )
    
    def _get_example_commands(self) -> str:
        """Get formatted example commands."""
        examples = self.intent_parser.get_action_examples()
        formatted_examples = []
        
        for action_type, command_list in examples.items():
            formatted_examples.append(f"**{action_type.upper()}:**")
            for cmd in command_list[:2]:  # Show first 2 examples
                formatted_examples.append(f"  • {cmd}")
        
        return "**Example commands:**\n\n" + "\n".join(formatted_examples)
    
    def get_screen_info(self) -> str:
        """Get current screen information."""
        width, height = self.automation_engine.get_screen_size()
        return f"Screen size: {width}x{height} pixels"
    
    def get_execution_history(self) -> str:
        """Get formatted execution history."""
        if not self.execution_history:
            return "No commands executed yet."
        
        history_lines = []
        for i, (command, result) in enumerate(self.execution_history[-10:], 1):  # Last 10 commands
            status = "✅" if result.success else "❌"
            history_lines.append(f"{i}. {status} `{command}` - {result.message}")
        
        return "\n".join(history_lines)
    
    def clear_history(self) -> str:
        """Clear execution history."""
        self.execution_history.clear()
        return "History cleared."


def create_gradio_interface():
    """Create and configure the Gradio interface."""
    app = IntentApparatus()
    
    # Custom CSS for better styling
    css = """
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        color: #856404;
    }
    """
    
    with gr.Blocks(css=css, title="Intent Apparatus - OS Automation Tool") as interface:
        gr.HTML("""
        <div class="header">
            <h1>🎯 Intent Apparatus</h1>
            <p>Natural Language OS Automation Tool</p>
        </div>
        """)
        
        gr.HTML("""
        <div class="warning-box">
            <strong>⚠️ Safety Warning:</strong> This tool can control your mouse and keyboard. 
            Use with caution and ensure you understand the commands before executing them. 
            Move your mouse to any corner of the screen to activate the safety failsafe.
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                command_input = gr.Textbox(
                    label="Enter your command in natural language",
                    placeholder="e.g., 'click at 100, 200' or 'type \"Hello World\"' or 'press enter'",
                    lines=2
                )
                
                with gr.Row():
                    execute_btn = gr.Button("🚀 Execute", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear History", variant="secondary")
                
                status_output = gr.Textbox(label="Status", interactive=False)
                message_output = gr.Textbox(label="Result", lines=3, interactive=False)
                
                screenshot_output = gr.Image(label="Screenshot (if applicable)", visible=True)
            
            with gr.Column(scale=1):
                screen_info = gr.Textbox(
                    label="Screen Information",
                    value=app.get_screen_info(),
                    interactive=False
                )
                
                history_output = gr.Textbox(
                    label="Execution History (Last 10)",
                    lines=10,
                    interactive=False,
                    value="No commands executed yet."
                )
                
                examples_box = gr.Textbox(
                    label="Command Examples",
                    value=app._get_example_commands(),
                    lines=15,
                    interactive=False
                )
        
        # Event handlers
        def execute_command(command):
            status, message, screenshot_path = app.process_command(command)
            history = app.get_execution_history()
            
            # Handle screenshot
            screenshot = None
            if screenshot_path and os.path.exists(screenshot_path):
                screenshot = screenshot_path
            
            return status, message, screenshot, history, ""  # Clear input
        
        def clear_history():
            result = app.clear_history()
            return result, "No commands executed yet."
        
        execute_btn.click(
            fn=execute_command,
            inputs=[command_input],
            outputs=[status_output, message_output, screenshot_output, history_output, command_input]
        )
        
        # Also execute on Enter key
        command_input.submit(
            fn=execute_command,
            inputs=[command_input],
            outputs=[status_output, message_output, screenshot_output, history_output, command_input]
        )
        
        clear_btn.click(
            fn=clear_history,
            outputs=[status_output, history_output]
        )
    
    return interface


def main():
    """Main entry point for the application."""
    interface = create_gradio_interface()
    
    print("🎯 Starting Intent Apparatus...")
    print("⚠️  WARNING: This tool can control your mouse and keyboard!")
    print("📝 Access the web interface to start automating...")
    
    # Launch the interface
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False
    )


if __name__ == "__main__":
    main()
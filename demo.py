"""
Demo version of the Intent Apparatus that works without external dependencies.
This demonstrates the core functionality using built-in Python libraries.
"""

import re
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from mock_automation import AutomationEngine
from intent_parser import IntentParser, ActionResult


class SimpleWebInterface:
    """Simple text-based interface for demonstration."""
    
    def __init__(self):
        self.automation_engine = AutomationEngine()
        self.intent_parser = IntentParser()
        self.execution_history: List[Tuple[str, ActionResult]] = []
    
    def process_command(self, command: str) -> Tuple[str, str]:
        """Process a natural language command and execute the action."""
        if not command.strip():
            return "❌ Error", "Please enter a command."
        
        # Parse the command
        parsed_intent = self.intent_parser.parse_command(command)
        
        if not parsed_intent:
            examples = self._get_example_commands()
            return (
                "❌ Unable to parse command", 
                f"Could not understand the command: '{command}'\n\n{examples}"
            )
        
        # Execute the action
        result = self._execute_action(parsed_intent)
        
        # Store in history
        self.execution_history.append((command, result))
        
        # Format response
        status = "✅ Success" if result.success else "❌ Error"
        message = result.message
        
        return status, message
    
    def _execute_action(self, intent) -> ActionResult:
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
                        message=f"[SIMULATED] Screenshot saved as {screenshot_path}",
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
            formatted_examples.append(f"{action_type.upper()}:")
            for cmd in command_list[:2]:  # Show first 2 examples
                formatted_examples.append(f"  • {cmd}")
        
        return "Example commands:\n\n" + "\n".join(formatted_examples)
    
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
            history_lines.append(f"{i}. {status} '{command}' - {result.message}")
        
        return "\n".join(history_lines)


def demo_interface():
    """Run a simple command-line demo of the Intent Apparatus."""
    interface = SimpleWebInterface()
    
    print("🎯 Intent Apparatus - Demo Mode")
    print("=" * 50)
    print("⚠️  This is a demonstration mode using simulated actions.")
    print("   Install pyautogui and gradio for full functionality.")
    print()
    print(interface.get_screen_info())
    print()
    print("Available commands:")
    print(interface._get_example_commands())
    print()
    print("Type 'quit' to exit, 'history' to see execution history")
    print("=" * 50)
    
    while True:
        try:
            command = input("\n🎯 Enter command: ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if command.lower() == 'history':
                print("\n📝 Execution History:")
                print(interface.get_execution_history())
                continue
            
            if not command:
                continue
            
            status, message = interface.process_command(command)
            print(f"\n{status}")
            print(f"📄 {message}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break


def test_functionality():
    """Test the core functionality with predefined commands."""
    interface = SimpleWebInterface()
    
    test_commands = [
        "click at 100, 200",
        "type \"Hello World\"",
        "press enter",
        "ctrl+c",
        "scroll up 3",
        "move mouse to 500, 600",
        "take a screenshot",
        "invalid command that should fail"
    ]
    
    print("🧪 Testing Intent Apparatus Functionality")
    print("=" * 50)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. Testing: '{command}'")
        status, message = interface.process_command(command)
        print(f"   {status}")
        print(f"   📄 {message}")
    
    print("\n📝 Final Execution History:")
    print(interface.get_execution_history())


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Interactive demo")
    print("2. Automated tests")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            demo_interface()
        elif choice == "2":
            test_functionality()
        else:
            print("Invalid choice. Running interactive demo...")
            demo_interface()
    
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")
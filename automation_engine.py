"""
Automation Engine for OS interactions based on natural language commands.
"""

import pyautogui
import time
import re
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Configure pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ActionResult:
    """Result of an automation action."""
    success: bool
    message: str
    action_type: str


class AutomationEngine:
    """Main automation engine for executing OS commands."""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"Screen size: {self.screen_width}x{self.screen_height}")
    
    def click_at_position(self, x: int, y: int, button: str = 'left') -> ActionResult:
        """Click at specific coordinates."""
        try:
            if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
                return ActionResult(
                    success=False,
                    message=f"Coordinates ({x}, {y}) are outside screen bounds",
                    action_type="click"
                )
            
            pyautogui.click(x, y, button=button)
            return ActionResult(
                success=True,
                message=f"Clicked at position ({x}, {y}) with {button} button",
                action_type="click"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to click: {str(e)}",
                action_type="click"
            )
    
    def type_text(self, text: str) -> ActionResult:
        """Type text using keyboard."""
        try:
            pyautogui.typewrite(text)
            return ActionResult(
                success=True,
                message=f"Typed text: '{text}'",
                action_type="type"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to type text: {str(e)}",
                action_type="type"
            )
    
    def press_key(self, key: str) -> ActionResult:
        """Press a specific key."""
        try:
            pyautogui.press(key)
            return ActionResult(
                success=True,
                message=f"Pressed key: {key}",
                action_type="key_press"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to press key: {str(e)}",
                action_type="key_press"
            )
    
    def key_combination(self, keys: List[str]) -> ActionResult:
        """Press key combination (e.g., ctrl+c)."""
        try:
            pyautogui.hotkey(*keys)
            return ActionResult(
                success=True,
                message=f"Pressed key combination: {'+'.join(keys)}",
                action_type="key_combination"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to press key combination: {str(e)}",
                action_type="key_combination"
            )
    
    def scroll(self, direction: str, clicks: int = 3) -> ActionResult:
        """Scroll in a direction."""
        try:
            if direction.lower() == 'up':
                pyautogui.scroll(clicks)
            elif direction.lower() == 'down':
                pyautogui.scroll(-clicks)
            else:
                return ActionResult(
                    success=False,
                    message=f"Invalid scroll direction: {direction}",
                    action_type="scroll"
                )
            
            return ActionResult(
                success=True,
                message=f"Scrolled {direction} {clicks} clicks",
                action_type="scroll"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to scroll: {str(e)}",
                action_type="scroll"
            )
    
    def move_mouse(self, x: int, y: int) -> ActionResult:
        """Move mouse to position."""
        try:
            if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
                return ActionResult(
                    success=False,
                    message=f"Coordinates ({x}, {y}) are outside screen bounds",
                    action_type="mouse_move"
                )
            
            pyautogui.moveTo(x, y)
            return ActionResult(
                success=True,
                message=f"Moved mouse to ({x}, {y})",
                action_type="mouse_move"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to move mouse: {str(e)}",
                action_type="mouse_move"
            )
    
    def take_screenshot(self) -> Optional[str]:
        """Take a screenshot and return the filename."""
        try:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return filename
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions."""
        return self.screen_width, self.screen_height
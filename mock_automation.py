"""
Minimal automation engine without PyAutoGUI dependency for demonstration.
This version simulates the automation actions and can be used to test the interface.
"""

import time
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ActionResult:
    """Result of an automation action."""
    success: bool
    message: str
    action_type: str


class MockAutomationEngine:
    """Mock automation engine for testing without actual OS control."""
    
    def __init__(self):
        self.screen_width, self.screen_height = 1920, 1080  # Mock screen size
        logger.info(f"Mock screen size: {self.screen_width}x{self.screen_height}")
    
    def click_at_position(self, x: int, y: int, button: str = 'left') -> ActionResult:
        """Mock click at specific coordinates."""
        try:
            if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
                return ActionResult(
                    success=False,
                    message=f"Coordinates ({x}, {y}) are outside screen bounds",
                    action_type="click"
                )
            
            logger.info(f"MOCK: Would click at ({x}, {y}) with {button} button")
            return ActionResult(
                success=True,
                message=f"[SIMULATED] Clicked at position ({x}, {y}) with {button} button",
                action_type="click"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to click: {str(e)}",
                action_type="click"
            )
    
    def type_text(self, text: str) -> ActionResult:
        """Mock type text using keyboard."""
        try:
            logger.info(f"MOCK: Would type text: '{text}'")
            return ActionResult(
                success=True,
                message=f"[SIMULATED] Typed text: '{text}'",
                action_type="type"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to type text: {str(e)}",
                action_type="type"
            )
    
    def press_key(self, key: str) -> ActionResult:
        """Mock press a specific key."""
        try:
            logger.info(f"MOCK: Would press key: {key}")
            return ActionResult(
                success=True,
                message=f"[SIMULATED] Pressed key: {key}",
                action_type="key_press"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to press key: {str(e)}",
                action_type="key_press"
            )
    
    def key_combination(self, keys: List[str]) -> ActionResult:
        """Mock press key combination (e.g., ctrl+c)."""
        try:
            logger.info(f"MOCK: Would press key combination: {'+'.join(keys)}")
            return ActionResult(
                success=True,
                message=f"[SIMULATED] Pressed key combination: {'+'.join(keys)}",
                action_type="key_combination"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to press key combination: {str(e)}",
                action_type="key_combination"
            )
    
    def scroll(self, direction: str, clicks: int = 3) -> ActionResult:
        """Mock scroll in a direction."""
        try:
            if direction.lower() not in ['up', 'down']:
                return ActionResult(
                    success=False,
                    message=f"Invalid scroll direction: {direction}",
                    action_type="scroll"
                )
            
            logger.info(f"MOCK: Would scroll {direction} {clicks} clicks")
            return ActionResult(
                success=True,
                message=f"[SIMULATED] Scrolled {direction} {clicks} clicks",
                action_type="scroll"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to scroll: {str(e)}",
                action_type="scroll"
            )
    
    def move_mouse(self, x: int, y: int) -> ActionResult:
        """Mock move mouse to position."""
        try:
            if not (0 <= x <= self.screen_width and 0 <= y <= self.screen_height):
                return ActionResult(
                    success=False,
                    message=f"Coordinates ({x}, {y}) are outside screen bounds",
                    action_type="mouse_move"
                )
            
            logger.info(f"MOCK: Would move mouse to ({x}, {y})")
            return ActionResult(
                success=True,
                message=f"[SIMULATED] Moved mouse to ({x}, {y})",
                action_type="mouse_move"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to move mouse: {str(e)}",
                action_type="mouse_move"
            )
    
    def take_screenshot(self) -> Optional[str]:
        """Mock take a screenshot and return the filename."""
        try:
            timestamp = int(time.time())
            filename = f"mock_screenshot_{timestamp}.png"
            logger.info(f"MOCK: Would take screenshot: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get mock screen dimensions."""
        return self.screen_width, self.screen_height


# For compatibility, we'll try to import the real engine but fall back to mock
try:
    # This will fail without pyautogui installed
    from automation_engine import AutomationEngine
    print("✅ Real automation engine available")
except ImportError:
    # Use the mock engine instead
    AutomationEngine = MockAutomationEngine
    print("⚠️ Using mock automation engine (install pyautogui for real automation)")
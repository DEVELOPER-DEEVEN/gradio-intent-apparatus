"""
Natural Language Processing module for parsing user intents into automation actions.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ActionResult:
    """Result of an automation action."""
    success: bool
    message: str
    action_type: str


@dataclass
class ParsedIntent:
    """Parsed user intent with action details."""
    action_type: str
    parameters: Dict
    confidence: float
    raw_command: str


class IntentParser:
    """Parse natural language commands into automation actions."""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[Tuple[str, str]]]:
        """Initialize regex patterns for different action types."""
        return {
            'click': [
                (r'right\s+click\s+(?:at\s+)?(?:position\s+)?(?:\()?(\d+)(?:\s*,\s*|\s+)(\d+)(?:\))?', 'right_coordinates'),
                (r'double\s+click\s+(?:at\s+)?(?:position\s+)?(?:\()?(\d+)(?:\s*,\s*|\s+)(\d+)(?:\))?', 'double_coordinates'),
                (r'(?:left\s+)?click\s+(?:at\s+)?(?:position\s+)?(?:\()?(\d+)(?:\s*,\s*|\s+)(\d+)(?:\))?', 'coordinates'),
            ],
            'type': [
                (r'type\s+["\']([^"\']+)["\']', 'text'),
                (r'write\s+["\']([^"\']+)["\']', 'text'),
                (r'enter\s+["\']([^"\']+)["\']', 'text'),
                (r'input\s+["\']([^"\']+)["\']', 'text'),
            ],
            'key': [
                (r'press\s+(?:the\s+)?(\w+)(?:\s+key)?', 'single_key'),
                (r'hit\s+(?:the\s+)?(\w+)(?:\s+key)?', 'single_key'),
                (r'press\s+(\w+)\s*\+\s*(\w+)', 'key_combo'),
                (r'(\w+)\s*\+\s*(\w+)', 'key_combo'),
            ],
            'scroll': [
                (r'scroll\s+(up|down)(?:\s+(\d+))?', 'direction'),
                (r'scroll\s+(\d+)\s+times?\s+(up|down)', 'direction_count'),
            ],
            'move': [
                (r'move\s+(?:mouse\s+)?(?:to\s+)?(?:position\s+)?(?:\()?(\d+)(?:\s*,\s*|\s+)(\d+)(?:\))?', 'coordinates'),
                (r'move\s+(?:cursor\s+)?(?:to\s+)?(?:position\s+)?(?:\()?(\d+)(?:\s*,\s*|\s+)(\d+)(?:\))?', 'coordinates'),
            ],
            'screenshot': [
                (r'take\s+(?:a\s+)?screenshot', 'simple'),
                (r'capture\s+screen', 'simple'),
                (r'screenshot', 'simple'),
            ]
        }
    
    def parse_command(self, command: str) -> Optional[ParsedIntent]:
        """Parse a natural language command into an intent."""
        command = command.lower().strip()
        
        if not command:
            return None
        
        for action_type, patterns in self.patterns.items():
            for pattern, pattern_type in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    parameters = self._extract_parameters(match, pattern_type, action_type)
                    if parameters is not None:  # Allow empty dicts for commands like screenshot
                        return ParsedIntent(
                            action_type=action_type,
                            parameters=parameters,
                            confidence=0.8,  # Simple confidence score
                            raw_command=command
                        )
        
        return None
    
    def _extract_parameters(self, match, pattern_type: str, action_type: str) -> Optional[Dict]:
        """Extract parameters from regex match."""
        try:
            if pattern_type == 'coordinates':
                return {
                    'x': int(match.group(1)),
                    'y': int(match.group(2)),
                    'button': 'left'
                }
            elif pattern_type == 'right_coordinates':
                return {
                    'x': int(match.group(1)),
                    'y': int(match.group(2)),
                    'button': 'right'
                }
            elif pattern_type == 'double_coordinates':
                return {
                    'x': int(match.group(1)),
                    'y': int(match.group(2)),
                    'button': 'left',
                    'clicks': 2
                }
            elif pattern_type == 'text':
                return {'text': match.group(1)}
            elif pattern_type == 'single_key':
                key = match.group(1).lower()
                # Map common key names
                key_mapping = {
                    'enter': 'enter',
                    'return': 'enter',
                    'space': 'space',
                    'spacebar': 'space',
                    'tab': 'tab',
                    'escape': 'esc',
                    'esc': 'esc',
                    'delete': 'delete',
                    'backspace': 'backspace',
                    'ctrl': 'ctrl',
                    'alt': 'alt',
                    'shift': 'shift',
                    'windows': 'winleft',
                    'win': 'winleft',
                    'cmd': 'cmd',
                    'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
                    'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
                    'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
                    'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
                    'home': 'home', 'end': 'end', 'pageup': 'pageup', 'pagedown': 'pagedown'
                }
                return {'key': key_mapping.get(key, key)}
            elif pattern_type == 'key_combo':
                key1 = match.group(1).lower()
                key2 = match.group(2).lower()
                # Map key names for combinations
                key_mapping = {
                    'ctrl': 'ctrl', 'control': 'ctrl',
                    'alt': 'alt',
                    'shift': 'shift',
                    'cmd': 'cmd', 'command': 'cmd',
                    'win': 'winleft', 'windows': 'winleft'
                }
                return {
                    'keys': [
                        key_mapping.get(key1, key1),
                        key_mapping.get(key2, key2)
                    ]
                }
            elif pattern_type == 'direction':
                direction = match.group(1)
                clicks = int(match.group(2)) if match.group(2) else 3
                return {'direction': direction, 'clicks': clicks}
            elif pattern_type == 'direction_count':
                clicks = int(match.group(1))
                direction = match.group(2)
                return {'direction': direction, 'clicks': clicks}
            elif pattern_type == 'simple':
                return {}
            
        except (ValueError, IndexError) as e:
            logger.error(f"Failed to extract parameters: {e}")
            return None
        
        return None
    
    def get_action_examples(self) -> Dict[str, List[str]]:
        """Get example commands for each action type."""
        return {
            'click': [
                "click at 100, 200",
                "left click at position (300, 400)",
                "right click at 150, 250",
                "double click at 500, 600"
            ],
            'type': [
                'type "Hello World"',
                'write "This is a test"',
                'enter "some text here"',
                'input "username123"'
            ],
            'key': [
                "press enter",
                "hit the space key",
                "press ctrl+c",
                "alt+tab"
            ],
            'scroll': [
                "scroll up",
                "scroll down 5",
                "scroll 3 times up"
            ],
            'move': [
                "move mouse to 100, 200",
                "move cursor to position (300, 400)"
            ],
            'screenshot': [
                "take a screenshot",
                "capture screen",
                "screenshot"
            ]
        }
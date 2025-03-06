import readline
import os
from typing import Optional
import click

class CommandHistory:
    def __init__(self, function: str):
        self.history_file = os.path.expanduser(f'~/.clippy/{function}__history')
        self._load_history()
        
    def _load_history(self):
        """Load command history from file"""
        if os.path.exists(self.history_file):
            try:
                readline.read_history_file(self.history_file)
            except Exception:
                pass
    
    def save_history(self):
        """Save command history to file"""
        try:
            readline.write_history_file(self.history_file)
        except Exception:
            pass
    
    def add_to_history(self, command: str):
        """Add a command to history"""
        if command.strip():  # Only add non-empty commands
            readline.add_history(command)
            self.save_history()

def get_input_with_history(prompt: str, function: str) -> str:
    """
    Get input from user with command history support.
    Press up/down arrows to cycle through history.
    """
    history = CommandHistory(function)
    
    # Set up readline
    readline.set_auto_history(True)
    
    try:
        return click.prompt(prompt)
    finally:
        history.save_history() 
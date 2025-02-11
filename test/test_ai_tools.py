import pytest
import os
from clippy.tools.ai import load_prompt_template, execute_prompt
from langchain.schema import AIMessage
from unittest.mock import patch, MagicMock

def test_load_prompt_template():
    # Test loading existing template
    template_content = load_prompt_template('base_system')
    assert isinstance(template_content, str)
    assert len(template_content) > 0

    # Test loading non-existent template
    with pytest.raises(FileNotFoundError):
        load_prompt_template('non_existent_template')

    # Test template with variables
    variables = {'test_var': 'test_value'}
    template_content = load_prompt_template('base_system', variables)
    assert isinstance(template_content, str)

@patch('clippy.tools.ai.ChatOpenAI')
def test_execute_prompt(mock_chat):
    # Setup mock
    mock_instance = MagicMock()
    mock_chat.return_value = mock_instance
    mock_instance.invoke.return_value = AIMessage(content="Test response")

    # Test without system prompt
    response = execute_prompt("Test prompt")
    assert response == "Test response"
    mock_instance.invoke.assert_called_once()

    # Reset mock
    mock_instance.invoke.reset_mock()

    # Test with system prompt
    response = execute_prompt("Test prompt", system_prompt="System prompt")
    assert response == "Test response"
    mock_instance.invoke.assert_called_once()

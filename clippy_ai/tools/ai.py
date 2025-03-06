from jinja2 import Template
import os

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel

from clippy_ai.utils import logger

def configure_openai_model(model="gpt-4o-mini", temperature=0.5, api_key=None):
    """Configure the model for the AI tool"""
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)


def load_prompt_template(prompt, variables=None):
    """Load a system prompt template from the templates directory and render with variables"""
   
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    template_path = os.path.join(template_dir, f"{prompt}.md")

    try:
        with open(template_path, 'r') as file:
            template = Template(file.read())
            if variables is not None:
                return template.render(variables)
            return template.render()
    except FileNotFoundError:
        raise FileNotFoundError(f"System prompt template '{prompt}.md' not found in templates directory")


def execute_prompt(prompt, model, system_prompt=None):  # pragma: no cover
    """Execute a prompt and return the response"""
    
    messages = [HumanMessage(content=prompt)]

    if system_prompt:
        messages.insert(0, SystemMessage(content=system_prompt))

    response = model.invoke(messages)
    return response.content

def execute_prompt_structured(baseModel: BaseModel, prompt, model, system_prompt=None):
    """Execute a prompt and return the response as structured data"""
    
    messages = [HumanMessage(content=prompt)]

    if system_prompt:
        messages.insert(0, SystemMessage(content=system_prompt))
    
    logger.debug(f"Prompt: {prompt}")
    logger.debug(f"Model: {model.model_name}")
    logger.debug(f"System prompt: {system_prompt}")


    structured_model = model.with_structured_output(baseModel, method="json_mode")
    
    try:
        response = structured_model.invoke(messages)
        logger.debug(f"Response: {response}")
        return response
    except Exception as e:
        logger.log_error(f"Error executing prompt: {e}")
        return None
#!/usr/bin/env python
import os
import click
import pkg_resources
from datetime import datetime
from clippy.tools.ai import configure_openai_model, execute_prompt, load_prompt_template
import clippy.utils.logger as logger
import clippy.utils.helper as utils
import clippy.utils.config as config

VERSION = pkg_resources.require("clippy")[0].version  
 
def debug_logging(verbose):
    if verbose == 1:
        click.echo(click.style("Debugging Level is set", fg='green'))
        logger.enable_debug()

@click.group()
@click.version_option(version=VERSION, prog_name='clippy')
def clippy():  # pragma: no cover
    pass


@click.command()
@click.option('--v', count=True, help='Enable verbose logging')
def configure(v):
    debug_logging(v)
    logger.log_bl("Running configuration")
    apikey = click.prompt('OPENAI_API_KEY')
    config.set_env('default', 'OPENAI_API_KEY', apikey)
    logger.log_bl("Configuration Complete")


@click.command()
@click.option('--v', count=True, help='Enable verbose logging')
@click.argument('prompt', required=True)
def ai(v, prompt):
    """Send a prompt to OpenAI and get a response"""
    debug_logging(v)
    logger.debug("Sending prompt to OpenAI")
    api_key = config.get_env('default', 'OPENAI_API_KEY')
    if not api_key:
        logger.log_error("No API key configured. Please run 'clippy configure' first")
        return
    
    model = configure_openai_model(model="gpt-4o-mini",temperature=0, api_key=api_key)
    
    system_prompt = load_prompt_template('base_system')
    response = execute_prompt(prompt, model, system_prompt=system_prompt)
    logger.log_bl(response)
    logger.debug("Response received from OpenAI")

@click.command()
@click.option('--v', count=True, help='Enable verbose logging')
@click.argument('prompt', required=True)
def cmd(v, prompt):
    """Send a prompt to OpenAI and get a response"""
    debug_logging(v)
    logger.debug("Sending prompt to OpenAI")
    api_key = config.get_env('default', 'OPENAI_API_KEY')
    if not api_key:
        logger.log_error("No API key configured. Please run 'clippy configure' first")
        return
    
    model = configure_openai_model(model="gpt-4o-mini",temperature=0, api_key=api_key)
    
    prompt_template = load_prompt_template('mac_commands', {'input': prompt})
    response = execute_prompt(prompt_template, model)
    logger.log_bl(f"Suggested command: {response}")
    logger.debug("Response received from OpenAI")
    output = utils.cmd_exec(response)
    logger.log_bl("Command output:")
    logger.log_bl(output)
    logger.debug("Command executed successfully")


clippy.add_command(configure)
clippy.add_command(ai)
clippy.add_command(cmd)
if __name__ == '__main__':  # pragma: no cover
    clippy()
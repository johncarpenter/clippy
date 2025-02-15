#!/usr/bin/env python
import os
import click
import pkg_resources
from datetime import datetime
from clippy.tools.ai import configure_openai_model, execute_prompt, load_prompt_template
import clippy.utils.logger as logger
import clippy.utils.helper as utils
import clippy.utils.config as config    
from clippy.tools.tmetric import get_tmetric_projects, add_tmetric_time_entry, TimeEntry
from clippy.tools.ai import execute_prompt_structured
from clippy.tools.tmetric import TimeEntry

from clippy.tools.harvest import get_harvest_projects, add_harvest_time_entry


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
    logger.debug("Configuration is located in ~/.clippy/config.ini")


    openaikey = config.get_env('default', 'OPENAI_API_KEY')
    apikey = click.prompt(f'OPENAI_API_KEY (leave blank to skip) {openaikey[:5] if openaikey else ""}', default='')
    if apikey:
        logger.debug(f"Setting OPENAI_API_KEY: {apikey}")
        config.set_env('default', 'OPENAI_API_KEY', apikey)

    tmetric_token = config.get_env('default', 'TMETRIC_TOKEN')
    tmetric_token = click.prompt(f'TMETRIC_TOKEN (leave blank to skip) {tmetric_token[:5] if tmetric_token else ""}', default='')
    if tmetric_token:
        config.set_env('default', 'TMETRIC_TOKEN', tmetric_token)
    

    harvest_token = config.get_env('default', 'HARVEST_TOKEN')
    harvest_token = click.prompt(f'HARVEST_TOKEN (leave blank to skip) {harvest_token[:5] if harvest_token else ""}', default='')
    if harvest_token:
        config.set_env('default', 'HARVEST_TOKEN', harvest_token)

    harvest_account_id = config.get_env('default', 'HARVEST_ACCOUNT_ID')
    harvest_account_id = click.prompt(f'HARVEST_ACCOUNT_ID (leave blank to skip) {harvest_account_id[:5] if harvest_account_id else ""}', default='')
    if harvest_account_id:
        config.set_env('default', 'HARVEST_ACCOUNT_ID', harvest_account_id)

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
@click.option('-p', '--prompt', prompt=True)
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
    logger.debug(f"Suggested command: {response}")
    logger.debug("Response received from OpenAI")
    output = utils.cmd_exec(response)
    logger.debug("Command output:")
    logger.log_bl(output)
    logger.debug("Command executed successfully")

@click.command()
@click.option('-v', count=True, help='Enable verbose logging')
@click.option('-p', '--prompt', prompt=True)
@click.option('-s', '--system', type=click.Choice(['tmetric', 'harvest', 'all']), default='all', help='Select timesheet system', prompt=True)

def time(v, prompt, system):
    """Enter time into the timesheet systems"""
    debug_logging(v)
    logger.debug("Parsing the time entry")

    today = datetime.now(tz=datetime.now().astimezone().tzinfo).strftime('%Y-%m-%d (%A)')

    logger.debug(f"Today's date: {today}")
    api_key = config.get_env('default', 'OPENAI_API_KEY')
    if not api_key:
        logger.log_error("No API key configured. Please run 'clippy configure' first")
        return
    
    if system == 'tmetric' or system == 'all':
        tmetric_token = config.get_env('default', 'TMETRIC_TOKEN')
        if not tmetric_token:
            logger.log_error("No TMetric token configured. Please run 'clippy configure' first") 
            return

   
        # Get projects from tmetric
        projects = get_tmetric_projects()
        logger.debug(f"TMetric Projects: {projects}")

        model = configure_openai_model(model="gpt-4o-mini",temperature=0, api_key=api_key)
        prompt_template = load_prompt_template('timesheets', {'input': prompt, 'projects': projects, 'today': today})
        response = execute_prompt_structured(TimeEntry, prompt_template, model)
        
        if click.confirm(f"Add time entry to tmetric: {response.model_dump()}", abort=False):
            # Add time entry to tmetric
            add_tmetric_time_entry(response)
            logger.log_bl(f"Time entry added to tmetric: {response}")

    # Add time entry to harvest
    if system == 'harvest' or system == 'all':
        harvest_token = config.get_env('default', 'HARVEST_TOKEN')
        if not harvest_token:
            logger.log_error("No Harvest token configured. Please run 'clippy configure' first") 
            return

        projects = get_harvest_projects()

        model = configure_openai_model(model="gpt-4o-mini",temperature=0, api_key=api_key)
        prompt_template = load_prompt_template('timesheets', {'input': prompt, 'projects': projects, 'today': today})
        response = execute_prompt_structured(TimeEntry, prompt_template, model)


        if response:
            logger.log_bl(f"Time entry received from OpenAI: {response.model_dump()}")
            if click.confirm(f"Add time entry to harvest: {response.model_dump()}", abort=False):
                add_harvest_time_entry(response)
                logger.log_bl(f"Time entry added to harvest: {response}")
        else:
            logger.log_error("No time entry received from OpenAI")

    


clippy.add_command(configure)
clippy.add_command(ai)
clippy.add_command(cmd)
clippy.add_command(time)
if __name__ == '__main__':  # pragma: no cover
    clippy()
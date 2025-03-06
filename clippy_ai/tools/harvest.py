# Tools to connect to Harvest time tracking system

import requests
import json
from pydantic import BaseModel, Field
import clippy_ai.utils.config as config  
import clippy_ai.utils.logger as logger

from datetime import datetime
from clippy_ai.tools.tmetric import TimeEntry

HOST_URL = "https://api.harvestapp.com/v2"

USER_AGENT = "Clippy/1.0"


def get_harvest_token_and_account_id():
    """Get the harvest token and account id from rest call"""
    harvest_token = config.get_env('default', 'HARVEST_TOKEN')
    harvest_account_id = config.get_env('default', 'HARVEST_ACCOUNT_ID')
    if harvest_token and harvest_account_id:
        logger.debug(f"Using cached token: {harvest_token}")
        return harvest_token, harvest_account_id

def get_harvest_user_id():
    """Get the harvest user id from rest call"""

    if config.get_env('default', 'HARVEST_USER_ID'):
        return config.get_env('default', 'HARVEST_USER_ID')

    harvest_token, harvest_account_id = get_harvest_token_and_account_id()
    headers = {
        "Authorization": f"Bearer {harvest_token}",
        "Harvest-Account-Id": harvest_account_id,
        "User-Agent": USER_AGENT
    }
    response = requests.get(f"{HOST_URL}/users/me", headers=headers)
    if response.status_code == 200:
        me = response.json()
        logger.debug(f"Harvest Users: {me}")
        config.set_env('default', 'HARVEST_USER_ID', str(me['id']))
        return me['id']
    else:
        logger.log_error(f"Error getting harvest user id: {response.json()}")
        return None


def get_harvest_projects():
    """Get the harvest projects from rest call"""
    harvest_token, harvest_account_id = get_harvest_token_and_account_id()
    headers = {
        "Authorization": f"Bearer {harvest_token}",
        "Harvest-Account-Id": harvest_account_id,
        "User-Agent": USER_AGENT
    }
    response = requests.get(f"{HOST_URL}/projects?is_active=true", headers=headers)
    if response.status_code == 200:
        allprojects = response.json()
        logger.debug(f"Harvest Projects: {allprojects}")
        projects = []
        for project in allprojects['projects']:
            projects.append({
                'id': project['id'],
                'name': project['name'],
                'client': project.get('client', {}).get('name', 'Jot'),
                'status': 'active'  ,
                'isBillable': project['is_billable'],
            })
        return projects
    else:
        return None


def get_harvest_tasks(project_id):
    """Get the harvest tasks from rest call"""
    harvest_token, harvest_account_id = get_harvest_token_and_account_id()
    headers = {
        "Authorization": f"Bearer {harvest_token}",
        "Harvest-Account-Id": harvest_account_id,
        "User-Agent": USER_AGENT
    }
    response = requests.get(f"{HOST_URL}/projects/{project_id}/task_assignments?is_active=true", headers=headers)
    if response.status_code == 200:
        alltasks = response.json()
        logger.debug(f"Harvest Tasks: {alltasks}")
        return alltasks['task_assignments']
    else:
        logger.log_error(f"Error getting harvest tasks: {response.json()}")
        return None

def add_harvest_time_entry(time_entry: TimeEntry):
    """Add a time entry to harvest"""

    start = datetime.fromisoformat(time_entry.start_time)
    end = datetime.fromisoformat(time_entry.end_time)
    duration = end - start
    hours = duration.total_seconds() / 3600

    default_tasks = get_harvest_tasks(time_entry.project.id)
    if default_tasks:
        default_task = default_tasks[0]['task']['id']

    time_entry_dict = {
        "user_id": get_harvest_user_id(),
        "project_id": time_entry.project.id,
        "task_id": default_task,
        "spent_date": time_entry.start_time.split('T')[0],
        "hours": hours,
        "notes": time_entry.description,
    }

    logger.log_bl(f"Adding time entry to harvest: {time_entry_dict}")
    harvest_token, harvest_account_id = get_harvest_token_and_account_id()
    headers = {
        "Authorization": f"Bearer {harvest_token}",
        "Harvest-Account-Id": harvest_account_id,
        "User-Agent": USER_AGENT
    }

    response = requests.post(f"{HOST_URL}/time_entries", headers=headers, json=time_entry_dict)

    if response.status_code == 201:
        return response.json()
    else:
        logger.log_error(f"Error adding time entry to harvest: {response.json()}")
        return None

# tools to interact with tmetric rest endpoints

from datetime import datetime, timedelta
import requests
import json
from pydantic import BaseModel, Field
import clippy_ai.utils.config as config
import clippy_ai.utils.logger as logger

HOST_URL = "https://app.tmetric.com/api/v3"

class Project(BaseModel):
    id: int = Field(default=0, description='The id of the project')
    name: str = Field(default="", description='The name of the project')
    client: str = Field(default="", description='The client of the project')

class TimeEntry(BaseModel):
    start_time: str = Field(default=(datetime.now() - timedelta(minutes=30)).isoformat(), description='The start time of the time entry in YYYY-MM-DDTHH:MM:SS format, use the current timezone')
    end_time: str = Field(default=datetime.now().isoformat(), description='The end time of the time entry in YYYY-MM-DDTHH:MM:SS format, use the current timezone')
    project: Project = Field(default_factory=lambda: Project(), description='The project of the time entry')
    description: str = Field(default="", description='The description of the time entry, Do not include date and time in the description')




def get_tmetric_user_info():
    """Get the tmetric user info from rest call"""
    
    userid = config.get_env('default', 'TMETRIC_USER_ID')
    accountid = config.get_env('default', 'TMETRIC_ACCOUNT_ID')
    if userid and accountid:
        logger.debug(f"Using cached user info: {userid} {accountid}")
        return {
            'userId': userid,
            'accountId': accountid
        }
    
    logger.debug("Fetching user info from tmetric")
    url = f"{HOST_URL}/user"
    headers = {
        "Authorization": f"Bearer {get_tmetric_token()}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        logger.debug(f"User info: {user_info}")
        config.set_env('default', 'TMETRIC_USER_ID', str(user_info['id']))
        config.set_env('default', 'TMETRIC_ACCOUNT_ID', str(user_info['accounts'][0]['id']  ))
        return {
            'userId': user_info['id'],
            'accountId': user_info['accounts'][0]['id']
        }

    else:
        logger.log_error(f"Failed to fetch user info from tmetric: {response.status_code}")
        raise Exception(f"Failed to fetch user info from tmetric: {response.status_code}")


def get_tmetric_token():
    """Get the tmetric token from the config"""
    token = config.get_env('default', 'TMETRIC_TOKEN')
    if token:
        logger.debug(f"Using cached token: {token}")
        return token
    else:
        logger.log_error("No token configured. Please run 'clippy configure' first")
        raise Exception("No token configured. Please run 'clippy configure' first")




def get_tmetric_projects():
    """Get the tmetric projects from rest call"""

    user_info = get_tmetric_user_info()
    if not user_info:
        return None
    
    userid = user_info['userId']
    accountid = user_info['accountId']

    url = f"{HOST_URL}/accounts/{accountid}/timeentries/projects"
    headers = {
        "Authorization": f"Bearer {get_tmetric_token()}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        allprojects = response.json()
        projects = []
        for project in allprojects:
            projects.append({
                'id': project['id'],
                'name': project['name'],
                'client': project.get('client', {}).get('name', 'Jot'),
                'status': project['status'],
                'isBillable': project['isBillable'],
            })
        return projects
    else:
        return None



def add_tmetric_time_entry(time_entry: TimeEntry):
    """Add a time entry to tmetric"""
    user_info = get_tmetric_user_info()
    if not user_info:
        return None
    

    url = f"{HOST_URL}/accounts/{user_info['accountId']}/timeentries"
    headers = {
        "Authorization": f"Bearer {get_tmetric_token()}"
    }

    logger.log_bl(f"Adding time entry to tmetric: {time_entry.model_dump()}")

    time_entry_dict = {
        "startTime": time_entry.start_time,
        "endTime": time_entry.end_time,
        "note": time_entry.description,
        "project":{
            "id": time_entry.project.id,
        },
    }


    response = requests.post(url, headers=headers, json=time_entry_dict)

    if response.status_code == 200:
        return response.json()
    else:
        logger.log_error(f"Failed to add time entry to tmetric: {response.status_code}")
        raise Exception(f"Failed to add time entry to tmetric: {response.status_code}")







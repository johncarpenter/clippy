
Please parse the following line of text to extract the following fields:
	1.	Start Time: Extract the start time in the format YYYY-DD-MM'T'hh:mm:ss.
	2.	End Time: Extract the end time in the format YYYY-DD-MM'T'hh:mm:ss.
	3.	Project: Use the project name from the provided list based on the client’s ID. Match the client ID to determine the corresponding project.
	4.	Description: Extract the description (free-form text) from the input, Do not include date and time in the description or relative dates "today". Don't include the project name in the description. 

Return the extracted data in the following JSON structure:

{
  "start_time": "YYYY-DD-MM'T'hh:mm:ss",
  "end_time": "YYYY-DD-MM'T'hh:mm:ss",
  "project": {
    "id": <project_id>,
    "name": "<project_name>",
    "client": "<client_name>"
  },
  "description": "<description>"
}

Example Input:

2025-02-14T08:00:00 2025-02-14T09:00:00 Jot Sales Completed the sales report for Jot client

Example Output:

{
  "start_time": "2025-02-14T08:00:00",
  "end_time": "2025-02-14T09:00:00",
  "project": {
    "id": 132536,
    "name": "Jot Sales",
    "client": "Jot"
  },
  "description": "Completed the sales report for Jot client"
}

This prompt will parse the input for the start and end times, match the project from the provided list based on the client ID, and structure the output in JSON format as requested.

The list of project information comes from the following json:
{{projects}}

Today is {{today}}. Relative dates and named days will refer to this date. Named days will refer to the current week. Wednesday for example will be the previous Wednesday.

Dates and times will be assumed to be standard business hours.

Use the current timezone for the dates and times.

------ Parse this line of text below ---------
{{input}}
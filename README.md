# Clippy AI

Clippy AI is a set of command-line tools designed to make your life easier when working with AI, time tracking, and more.

## Features

- **AI Assistance**: Send prompts to OpenAI models and get responses directly in your terminal
- **Time Tracking**: Integrate with TMetric and Harvest for seamless time entry management
- **Configuration Management**: Easy setup for API keys and preferences

## Installation

You can install Clippy AI directly from PyPI:

```bash
pip install clippy-ai
```

## Usage

To use Clippy AI, you can run the following command:

```bash
clippy --version
```


To run the script and display the available commands: 

```bash
%> clippy

Usage: clippy [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  configure
  ai
  cmd
  time
```

### Configure the tool

The first time you run the tool you will be prompted to configure it. You will need to provide your OpenAI API key. You can do that by running the ```clippy configure``` command. 

```bash
clippy configure
```

### Functions

Currently the tool has the following functions:

- `ai`: Send a prompt to OpenAI and get a response
- `cmd`: Send a prompt to OpenAI and get a response that executes a command
- `configure`: Configure the OpenAI API key
- `time`: Track time spent on a task

## AI Assistant

The `ai` command allows you to send prompts directly to OpenAI and get responses:

```bash
clippy ai "What is the capital of France?"
```

## Command Execution

The `cmd` command allows you to send prompts to OpenAI and get a response that executes a command:

```bash
clippy cmd "List all files in the current directory"
```

## Time Tracking

Time tracking can be configured to use TMetric and/or Harvest Tools. 

The `time` command allows you to track time spent on a task:

```bash
clippy time -p "Development task, worked from 9-11 today"
```




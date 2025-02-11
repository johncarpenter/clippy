# AI Tools

Clippy is a collection of command-line tools for working with AI. `clippy` is a python library and you will need python run time installed. 

### Prerequisites

- Python 3.10 or newer
- pip (Python package installer)
- An OpenAI API key
- Pyenv is optional but suggested.
```brew install pyenv``` is a good way to do this.


## Getting Started

Installing or updating the command line tool is done with 

```bash
pip install -U git+ssh://git@github.com/johncarpenter/clippy.git
```
You will need git configured on your local machine. 

This will install ```clippy``` command line tools.

## Usage

To run the script and display the available commands: 

```bash
%> clippy

Usage: clippy [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  configure
  
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

## Configuration

The `configure` command allows you to configure the OpenAI API key:

```bash
clippy configure
```
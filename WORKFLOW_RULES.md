# This file should be checked regularly so that the commands are not forgotten.
# The workflow is as follows: ChatGPT handles the oversight and prompt generation. The user then passes the generated prompt to the agent. The agent’s work report is relayed back to ChatGPT, which is responsible for the verification process. All testing is conducted by the user in a local environment.
# Technical decision: Selecting the safest and most appropriate solution, given the application's architecture and financial objectives—this is ChatGPT's responsibility.
# Verifiable execution—modifying code, updating documentation, and reviewing tests—must be supported by concrete evidence; a task should not be declared complete simply because a decision has been made.

# temporary rules for Stage 7:
    Primary reference documents moving forward:

    - reply.md: Interim report on the execution of the current prompt.
    - STAGE7_MASTER_WORKING_PACKET.md : Remaining Jobs Checklist.
    - In the STAGE7_MASTER_WORKING_PACKET.md file, each task must include a checkbox and a number.
    

# Follow the steps below to generate each new prompt
## Make each prompt in 2 blocks. One for Agent and one for User
## Each task in each prompt must have a number
## Each prompt must receive the report of each task with the number of that task from the agent.

## Prompt specifications for the agent:
### The number of tasks should not be too many and should not be too few, unless the end of the prompt is sub-prompt.
### It is up to the user to choose the model to execute the prompt. The prompt does not need to suggest a usage model to the user
### Each prompt must declare the required files to the model
### Prompt reporting should be such that each task performed has a name that the user matches with his own list
### Audit prompts should not merely state "what to examine"; they must also specify what evidence is required to accept a conclusion, and which conclusions remain impermissible given the available evidence.
### The agent only examines files that have been explicitly provided to it. If another file is required, it must state the exact name of the file and the reason why it is needed.


## Prompt specifications for the user in Farsi:
### The complete list of required files should be announced to the user
### Only the list of tasks should be given to the user
### The expected result of the task should be announced in a few words. such as checking and reporting or creating and changing code
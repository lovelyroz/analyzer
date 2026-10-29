# This file should be checked regularly so that the commands are not forgotten.
# Follow the steps below to generate each new prompt
## Make each prompt in 2 blocks. One for Agent and one for User

## Prompt specifications for the agent:
### The number of tasks should not be too many and should not be too few, unless the end of the prompt is sub-prompt.
### It is up to the user to choose the model to execute the prompt. The prompt does not need to suggest a usage model to the user
### Each prompt must declare the required files to the model
### Prompt reporting should be such that each task performed has a name that the user matches with his own list
### Audit prompts should not merely state "what to examine"; they must also specify what evidence is required to accept a conclusion, and which conclusions remain impermissible given the available evidence.


## Prompt specifications for the user in Farsi:
### The complete list of required files should be announced to the user
### Only the list of tasks should be given to the user
### The expected result of the task should be announced in a few words. such as checking and reporting or creating and changing code
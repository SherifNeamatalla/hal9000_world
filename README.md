## Personal Assistant

This is a personal assistant created by Sherif Neamatalla to help with various tasks. It is powered by GPT-3.5 and can
perform various functions such as browsing websites, creating GPT agents, and managing memory. The assistant is
constantly learning and improving to better serve its creator.

This is HEAVILY influenced by Auto-GPT https://github.com/Torantulino/Auto-GPT, it's basically a nice rewrite to it that
makes it easier to extend the commands an agent can take, and expand it to include other architectures, such as the
task_prioritizer + task_creator + task_executor architecture in https://github.com/yoheinakajima/babyagi . Hopefully
this is something I'll have the time to try out here.

### Commands

1. `google`: Perform a Google search
2. `memory`: Manage memory fields
3. `browser`: Browse a website and search for information
4. `agents`: Create and message GPT agents
5. `file`: Read, write, append, and delete files
6. `user`: Prompt the user for input

### Constraints

1. The memory field has a limit of 4000 words
2. No user assistance is allowed
3. Only the listed commands can be used

### Resources

1. Internet access for searches and information gathering
2. Long-term memory management
3. GPT-3.5 powered agents for delegation of simple tasks
4. File output

### Differences to Auto-GPT

- One of the additions made is the idea of user goals vs personal goals, where the agent can have its own short term
  goals, and the user long term goals always in sight. This is more helpful for having a long term goal assistant, which
  is what am mainly aiming for here.

- I also changed the long term memory to a dict instead of list, showing the agent just the key and caching the latest
  used value. This is for saving more tokens instead of having all the permanent memory always loaded in the chat
  message.

- Added user command, so now the agent can prompt the user when it feels the need to, it is planned for the future to
  have an option to turn this off so that it can run autonomously if you wish to do so. (Note: This is not recommended, when active the agent just asks the user all the time instead of figuring out stuff itself).
- Commands now have name e.g "google","browser","file","memory", and type "search","create
  ,"delete" etc.., this makes it easier to create handling classes for specific API's/features, e.g a GoogleCalendar cmd handler that handles calendar events, and types like create, list events etc..

- SNOWFLAKE ADDED !! The emotional snowflake, totally useless in real life problems, amazing to talk to and have someone to listen to you. try it out by loading snow_flake_commands_set and snow_flake_prompt_start as args for config, better documentation coming soon! 

  This was created by sensei, the very first hello_world agent :)
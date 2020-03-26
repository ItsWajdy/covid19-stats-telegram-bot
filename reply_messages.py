start_message = '''*What can this bot do?*

~APP_NAME~ is a great source of old and new stats and graphs relating to the Covid19 pandemic.
All information provided by ~APP_NAME~ is sourced from [https://worldometer/coronavirus/](https://worldometer/coronavirus/).

For a list of avaliable commands and features, issue the commane /help.

For more information about this bot, visit the [GitHub](https://github.com/ItsWajdy/covid19-stats-telegram-bot) repository.'''

help_message = '''~APP_NAME~ can help you get information about the Covid19 pandemic regarding the following:
- Total cases
- New cases
- Total deaths
- New deaths
- Total recovered
- Active cases

Any of the previous insights can be asked about for a certain country or for the entire world.
Any of the previous insights can be asked about for current day or they can be drawn as a function of time (starting with March 24th).

Send a _*regular*_ message starting with the insight name (as mentioned above), followed by country name (or the word "worldwide"), follwed by "today" for today's figures or "graph" for a complete graph.

A sample message might look like:
new cases china today'''

error_parsing_message = '''*Message not understood*

Check your spelling or type /help for a list of possible commands and message.'''

error_message = '''*Error! Could not get wanted information*

*Please report this error*'''

today_response_message = '''There were *{}* *{}* so far today {}'''
# ResearchAnalyzer
Open-source python API under GNU license for automation of ResearchLoggers' logs analysis. It offers reports on:

- Clicks
- Keystrokes
- Pauses
- Translation phases (provided that some preconditions are fulfilled)





## How to use

### Dependencies
- termcolor [sudo apt-get install python-termcolor]
- matplotlib
- colous [pip install colour]
- Python Image Library (PIL) [sudo apt-get install python-pil]



### Methods
The LogInfo object provides information on the data by using descriptive statistics. It must be instantiated by providing:

- A clicks log.
- A keystroke log.
- A system log.



#### Clicks
- **get_unique_pressed_clicks()**: Returns a set with all unique types of clicks used during the logging session.
- **get_all_pressed_clicks()**: Returns a list of pairs for each event in the session. Format:
````
(x coordinate, y coordinate, screen resolution, button type, click type, program name, window title)
````
- **get_click_info()**: Returns a list of tuples. Each tuple has the following format:
````
(button type, [down times], up time, press duration, [down x], [down y], up x, 'up y)
````
- **print_click_summary()**: It displays a summary of the click data:
     - Total amount of clicks.
     - Windows in which clicks are pressed.
     - Types of clicks used.
     - Mean click press time.
     - Click press time variance.
     - Click press time standard deviation.
- **plot_clicks_in_screenshot()**: Marks in a screenshot where clicks were made.
![Visualization of clicks in the screen session](/images/clicks_in_screen.png)


#### Keystrokes
- **get_unique_pressed_keys()**: Returns a set with all unique types of keystrokes used during the logging session. Examples: period, comma, a, c, z, downarrow, etc.
- **get_all_pressed_keys()**: Returns a list of pairs for each key event that occurred in the session. Format:
````
(key name, key type, window name, window title)
````
- **get_letter_info()**: Returns a list of tuples. Each tuple has the following format:
````
(key type, [down times], up time, press time, [down x], [down y], up x, up y)
````
-  **print_key_summary()**: It displays a summary of the keystroke data:
     - Total amount of pressed keys.
     - Unique pressed keys.
     - Windows in which keys are pressed.
     - Mean key press time.
     - Key press time variance.
     - Key press time standard deviation.
     - Unique function keys used.
     - Unique erase keys used.
     - Unique movement keys used.
     - Unique key combos used.
- **plot_keystroke_progression_graph(bin_size)**: It plots the amount of pressed down keys against time. Each of the bin size can be specified in seconds.

![Keystroke progression graph](/images/keystroke_progression_graph.png)

- **plot_clicks_progression_graph(bin_size)**: It plots the amount of pressed down clicks against time. Each of the bin size can be specified in seconds.

![Clicks progression graph](/images/clicks_progression_graph.png)



#### Resources
- **get_time_by_active_window()**: It returns a dictionary whose key is the name of a window used and its value is the time spent in it (in milliseconds). A special entry "total" contains the total session time.
- **plot_window_distribution_pie_chart()**: Plots a pie chart of the times spent in each window in the session.

![Window time distribution pie chart](/images/pie_chart_window_distribution.png)



#### Phases
- **get_orientation_info()**: Returns a tuple with the format (start time, start end).
- **get_drafting_info()**: Returns a tuple with the format (start time, start end).
- **get_orientation_info()**: Returns a tuple with the format (start time, start end).
- **get_total_session_time()**: Returns an integer with the total session time.
- **print_phases_summary()**: Prints a summary of the phases (orientation, drafting, revision and the whole session).
     - Start and end time.
     - Phase duration.
     - Percentage of the session dedicated to the phase.



#### Pauses
- **print_pauses()**: Prints an enumeration of all the pauses in the session, including the start and end of each one.
- **print_pause_summary(begin, end)**: Prints a summary of the pauses in the interval [begin, end]. It includes:
     - Total amount of pauses in the session.
     - Amount of:
         - Short pauses.
         - Medium pauses.
         - Large pauses.
         - Non significant pauses.
     - Mean pause time.
     - Pause time variance.



### Example
An usage example of ResearchAnalyzer can be found in main.py; it uses the ResearchLogger's example log files on the "example_log" folder.

The keystrokes summary looks like:
![Keystrokes summary](/images/keys_summary.png)

The clicks summary looks like:
![Clicks summary](/images/clicks_summary.png)

**Note**: You need to collect your own data with ResearchLogger to analyze your own datasets.
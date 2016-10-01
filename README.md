# ResearchAnalyzer
Open-source python API under GNU license for automation of ResearchLoggers' logs analysis. It offers reports on:

- Clicks
- Keystrokes
- Pauses
- Translation phases (provided that some preconditions are fulfilled)

## How to use

### Methods
The LogInfo object provides information on the data by using descriptive statistics. It must be instantiated by providing: (a) A clicks log (b) A keystroke log (c) A system log.

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
- **print_click_summary()**: It displays a summary of the click data: (a) Total amount of clicks (b) Windows in which clicks are pressed (c) Types of clicks used (d) Mean click press time (e) Click press time variance (f) Click press time standard deviation.


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
-  **print_key_summary()**: It displays a summary of the keystroke data: (a) Total amount of pressed keys (b) Unique pressed keys (c) Windows in which keys are pressed (d) Mean key press time (e) Key press time variance (f) Key press time standard deviation. (g) Unique function keys used (h) Unique erase keys used (g) Unique movement keys used (h) Unique key combos used.

### Example
An example can be found in main.py. Note: You need to collect your own data to use the example.
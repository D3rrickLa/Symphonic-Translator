# Symphonic Translator
Overview
Symphonic Translator is a Python-based application designed to capture MIDI input and translate it into keyboard shortcuts and basic command executions. This project allows musicians, producers, and developers to streamline their workflow by mapping MIDI messages from keyboards, knobs, and faders to specific actions on their computer.

## Features
MIDI Input Handling: Capture MIDI messages from a MIDI device.
Keyboard Shortcuts: Map MIDI note inputs to specific keyboard shortcuts to control applications or perform actions.
Command Execution: Run basic command line commands (CMD) based on MIDI inputs.
Future Enhancements: Plans to extend functionality to support MIDI control from knobs and faders, as well as the ability to run Python scripts directly from MIDI commands.
## Requirements
Python 3.x
Required libraries:
mido: For handling MIDI messages.
PySide6: For creating the user interface.
Other dependencies as needed (please list any additional libraries here).
## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/symphonic-translator.git
    cd symphonic-translator
    ```

2. Install required libraries: You can install the required libraries using pip:

    ```bash
        pip install -r requirements.txt
    ```
3. Run the application: You can start the application by running:

    ```bash
    python main.py
    ```

## Usage
1. tarting the Application: Launch the application, and it will prompt you to select a MIDI input device.

2. Mapping MIDI to Actions:

    - Once the MIDI device is connected, you can define the actions that correspond to various MIDI notes.
    - The application currently supports mapping MIDI notes to keyboard shortcuts.
    - Stopping the Application: Use the stop button in the UI to safely terminate the MIDI listener thread.

## Future Development
### Planned Features
- Knob and Fader Support: Extend the application to handle MIDI control messages from knobs and faders for more comprehensive control options.
- Script Execution: Implement functionality to execute Python scripts based on MIDI input.
- User Configuration: Create a user-friendly interface for configuring MIDI mappings and actions.

## Contributing
Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Thanks to the Mido library for handling MIDI input and output.
Thanks to PySide6 for building the user interface.

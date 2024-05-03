# vosk_stt_app
A lightweight, local speech recognition application based on vosk.

## Features
- **Local Operation**: All processing is done locally, without the need for an internet connection, protecting user privacy.
- **Lightweight**: The program is small in size and uses minimal resources, suitable for various computing environments.
- **Easy to Use**: Operate through a graphical interface with one-click recording and text conversion.
- **High Recognition Rate**: Utilizes the vosk model to provide accurate speech recognition.

## Environment Requirements
- Python 3.x
- pyaudio
- vosk
- numpy

## Installation Steps
1. Ensure that Python 3.x is installed on your system.
2. Install the required Python libraries:
   ```
   pip install pyaudio vosk numpy
   ```
3. Download the vosk model files and place them in the specified path of the program.

## Usage
1. Run the program, and the interface will prompt "Click the button on the right to start recording."
2. Click the "Start Recording" button to begin recording.
3. After 2 seconds of silence during recording, the program will automatically end the recording and begin conversion.
4. Once the conversion is complete, the text will automatically appear in the text box below.

## Notes
- When recording, please ensure a quiet environment to improve recognition accuracy.
- If the recording to text conversion fails, check if the model file path is correct and try recording again.

## Code Structure
- `speech_to_text`: The core function responsible for recording and speech recognition.
- `notice`: Used to display information in the status box.
- `run`: Starts the thread for recording and recognition.
- `root.mainloop`: The Tkinter event loop, waiting for user operations.

## Contributions and Feedback
Suggestions for improvements or code contributions to this project are welcome. For any issues, please provide feedback through Issues.

## Open Source License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT), for more details, see the `LICENSE` file in the project.

# Telegram Catizen Bot 😺

A bot written for the Telegram game that automatically matches cats with the same level.

## Demonstration 📱

![](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDNobmxtc3R2eDlib3VyMGUzdGpueHR6djF3ODRiN3NuNzE1ZjhlayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bmoAntYFi8DpnwIHfA/giphy.gif)

## Features 💡

- Automatically clicks on predefined areas within the Telegram window.
- Pauses/resumes clicking on right mouse button click.
- Exits the program on spacebar press.

## How to run? 🚀

1. Download the Repository:
- Clone the repository or download the ZIP file and extract it.

`git clone https://github.com/mykolamysak/CatizenBot.git`

Or download the ZIP file and extract it:
- Go to the repository page on GitHub.
- Click the "Code" button and select "Download ZIP".
- Extract the downloaded ZIP file.

2. Navigate to the dist Folder:

- Open the terminal (Command Prompt, PowerShell, or any terminal of your choice).
- Navigate to the dist folder where the catizen.exe file is located.

`cd path_to_downloaded_repository/CatizenBot/dist`

3. Run the catizen.exe File:

- In the terminal, run the catizen.exe file by typing the following command:

`./catizen.exe`

Or simply double-click the catizen.exe file from your file explorer.

## AI Version 🤖

The [AI Version](https://github.com/mykolamysak/CatizenBot/tree/ai-version) of the Telegram Catizen Bot incorporates OCR (Optical Character Recognition) to read the cat levels and attempts to match them based on their last digit. This experimental feature was developed out of curiosity and to explore the potential of integrating AI into the bot.

### Model and Training

The OCR functionality is powered by Tesseract, an open-source OCR engine developed by Google. Tesseract is renowned for its accuracy and has been trained on a wide variety of text and languages, making it suitable for extracting numerical data from images in various scenarios.

### Algorithm

1. **Window Detection**: The bot identifies the Telegram window on the screen to capture relevant screenshots.

2. **Image Processing**: 
    - The bot captures a screenshot of the Telegram window and crops it to focus on the specific areas where cat levels are displayed.
    - These areas are then highlighted and saved as separate image files for further processing.

3. **OCR (Optical Character Recognition)**:
    - The bot uses Tesseract OCR to extract text from the highlighted areas.
    - Extracted text is filtered to identify numerical values, representing the levels of cats.

4. **Number Matching**:
    - The bot identifies numbers with identical last digits.
    - It prioritizes single-digit numbers and matches them with corresponding multi-digit numbers that share the same last digit.

5. **Automated Actions**:
    - The bot performs drag-and-drop actions to match the identified cats based on their levels, simulating human interactions within the Telegram game.

### Performance and Limitations

While the AI version showcases the integration of OCR and automated actions, it may not always produce accurate results. The main limitations include:
- **OCR Accuracy**: Variations in text clarity, font, and image quality can affect the accuracy of Tesseract OCR.
- **Context Understanding**: The bot's logic is based on simple pattern recognition (last digit matching), which might not always align with the game's more complex requirements.
## Developed by 👷 
- Mykola Mysak

## License 🔒
This project is licensed under the MIT License. See the LICENSE file for details.

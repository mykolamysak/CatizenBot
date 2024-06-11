import pygetwindow as gw
import pyautogui
from PIL import Image, ImageDraw
import os
import cv2
import pytesseract
import re
import random
from pynput import mouse
from pynput.mouse import Button, Controller

mouse_controller = Controller()
pause_clicking = True  # The algorithm will be paused at startup

def get_telegram_window_bbox():
    windows = gw.getWindowsWithTitle('Telegram')
    if windows:
        window = windows[0]
        return (window.left, window.top, window.width, window.height)
    return None

def perform_ocr(img):
    # Set Tesseract path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Perform OCR
    text = pytesseract.image_to_string(img, config='--psm 6 --oem 3')

    # Use regular expressions to extract numbers
    numbers = re.findall(r'\d+', text)
    return numbers

def on_click(x, y, button, pressed):
    global pause_clicking
    if button == Button.right and pressed:
        pause_clicking = not pause_clicking
        print(f"Clicking {'paused' if pause_clicking else 'resumed'}")
        return True

# Add mouse listener
listener = mouse.Listener(on_click=on_click)
listener.start()

def process_image(bbox):
    # Capture screenshot of the specified region
    screenshot_path = "telegram_screenshot.png"
    screenshot = pyautogui.screenshot(region=bbox)
    screenshot.save(screenshot_path)

    # Open the screenshot
    image = Image.open(screenshot_path)

    # Define margins (in pixels) inside the cropped area
    margin_top = 500
    margin_right = 100
    margin_bottom = 200
    margin_left = 100

    # Calculate the coordinates for the cropped area
    crop_left = margin_left
    crop_top = margin_top
    crop_right = bbox[2] - margin_right
    crop_bottom = bbox[3] - margin_bottom

    # Crop the image
    cropped_image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Define the areas to highlight
    highlight_areas = [
        (10, 243, 163, 43),
        (10, 166, 163, 122),
        (10, 89, 163, 201),
        (10, 8, 163, 279),
        (70, 243, 103, 43),
        (70, 166, 103, 122),
        (70, 88, 103, 201),
        (70, 8, 103, 280),
        (130, 243, 43, 48),
        (130, 164, 43, 123),
        (130, 86, 43, 199),
        (130, 8, 43, 277),
    ]

    coordinates = []
    numbers_dict = {}
    dragged = False  # Flag to track if a drag action was performed

    for idx, (highlight_margin_top, highlight_margin_right, highlight_margin_bottom, highlight_margin_left) in enumerate(highlight_areas):
        # Calculate the coordinates for the highlighted area
        highlight_left = highlight_margin_left
        highlight_top = highlight_margin_top
        highlight_right = cropped_image.width - highlight_margin_right
        highlight_bottom = cropped_image.height - highlight_margin_bottom

        # Draw a rectangle around the highlighted area
        draw = ImageDraw.Draw(cropped_image)
        draw.rectangle(
            [(highlight_left, highlight_top), (highlight_right, highlight_bottom)],
            outline="red", width=1
        )

        # Extract the highlighted area and save it as a separate image
        highlighted_area = cropped_image.crop((highlight_left, highlight_top, highlight_right, highlight_bottom))
        highlighted_area_path = os.path.join(os.getcwd(), f"highlighted_area_{idx + 1}.png")
        highlighted_area.save(highlighted_area_path)

        # Perform OCR on the highlighted area
        numbers = perform_ocr(cv2.imread(highlighted_area_path))
        coordinates.append((highlight_left, highlight_top, highlight_right, highlight_bottom))

        for number in numbers:
            last_digit = number[-1]  # Extract the last digit
            if last_digit in numbers_dict:
                numbers_dict[last_digit].append((idx + 1, number))
            else:
                numbers_dict[last_digit] = [(idx + 1, number)]

    # Check for identical last digits and perform the drag action
    for last_digit, areas in numbers_dict.items():
        # Only connect areas if one of the numbers has a single digit
        filtered_areas = [area for area in areas if len(area[1]) == 1]
        if len(filtered_areas) >= 1 and len(areas) >= 2:
            # Ensure one of the areas has a single digit number
            first_area = filtered_areas[0][0] - 1
            second_area = [area for area in areas if area[0] != filtered_areas[0][0]][0][0] - 1

            start_x = bbox[0] + crop_left + coordinates[first_area][0] + (coordinates[first_area][2] - coordinates[first_area][0]) / 2
            start_y = bbox[1] + crop_top + coordinates[first_area][1] + (coordinates[first_area][3] - coordinates[first_area][1]) / 2

            end_x = bbox[0] + crop_left + coordinates[second_area][0] + (coordinates[second_area][2] - coordinates[second_area][0]) / 2
            end_y = bbox[1] + crop_top + coordinates[second_area][1] + (coordinates[second_area][3] - coordinates[second_area][1]) / 2

            # Perform the drag action
            mouse_controller.position = (start_x, start_y)
            mouse_controller.press(Button.left)
            mouse_controller.position = (end_x, end_y)
            mouse_controller.release(Button.left)
            print(f"Dragged from area {first_area + 1} to area {second_area + 1} based on last digit: {last_digit}")
            dragged = True  # Set the flag to True indicating a drag action was performed
            break  # Assuming only one drag action is needed

    # Save the cropped and highlighted image in the root directory
    cropped_image_path = os.path.join(os.getcwd(), "cropped_highlighted_image.png")
    cropped_image.save(cropped_image_path)

def main():
    bbox = get_telegram_window_bbox()
    if bbox is None:
        print("Telegram window not found.")
        return

    # Activate the Telegram window
    window = gw.getWindowsWithTitle('Telegram')[0]
    window.activate()

    while True:
        # Wait for the pause/resume state if paused
        while pause_clicking:
            pyautogui.sleep(0.1)

        # Process the image and perform actions
        process_image(bbox)


if __name__ == "__main__":
    main()

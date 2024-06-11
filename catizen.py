import pygetwindow as gw
import pyautogui
from PIL import Image, ImageDraw
import os
import cv2
import pytesseract
import re


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


def main():
    bbox = get_telegram_window_bbox()
    if bbox is None:
        print("Telegram window not found.")
        return

    # Activate the Telegram window
    window = gw.getWindowsWithTitle('Telegram')[0]
    window.activate()

    # Delay to ensure the window is activated
    pyautogui.sleep(1)

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
    # top, right77, bottom, left79
    highlight_areas = [
        (10, 243, 163, 43),
        (10, 166, 163, 122),
        (10, 89, 163, 201),
        (10, 8, 163, 279),
        (70, 243, 103, 43),
        (70, 166, 103, 122),
        (70, 89, 103, 201),
        (70, 8, 103, 279),
        (130, 243, 43, 43),
        (130, 166, 43, 122),
        (130, 89, 43, 201),
        (130, 8, 43, 279),
    ]

    for idx, (
    highlight_margin_top, highlight_margin_right, highlight_margin_bottom, highlight_margin_left) in enumerate(
            highlight_areas):
        # Calculate the coordinates for the highlighted area
        highlight_left = highlight_margin_left
        highlight_top = highlight_margin_top
        highlight_right = cropped_image.width - highlight_margin_right
        highlight_bottom = cropped_image.height - highlight_margin_bottom

        # Print the coordinates of the highlighted area
        print(
            f"\nArea {idx + 1}\nLeft: {highlight_left}\nTop: {highlight_top}\nRight: {highlight_right}\nBottom: {highlight_bottom}")

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

        # Print OCR results
        print(f"Number: {numbers}")

        # Calculate the center of the highlighted area
        center_x = bbox[0] + crop_left + highlight_left + (highlight_right - highlight_left) / 2
        center_y = bbox[1] + crop_top + highlight_top + (highlight_bottom - highlight_top) / 2

        # Move the cursor to the center of the highlighted area
        pyautogui.moveTo(center_x, center_y)

    # Save the cropped and highlighted image in the root directory
    cropped_image_path = os.path.join(os.getcwd(), "cropped_highlighted_image.png")
    cropped_image.save(cropped_image_path)


if __name__ == "__main__":
    main()

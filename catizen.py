import pygetwindow as gw
import pyautogui
from PIL import Image, ImageDraw, ImageChops
import os
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import threading

mouse_controller = Controller()
pause_clicking = True  # The algorithm will be paused at startup
exit_program = threading.Event()  # Event to signal exit

def get_telegram_window_bbox():
    windows = gw.getWindowsWithTitle('Telegram')
    if windows:
        window = windows[0]
        return (window.left, window.top, window.width, window.height)
    return None


def on_click(x, y, button, pressed):
    global pause_clicking
    if button == Button.right and pressed:
        pause_clicking = not pause_clicking
        if pause_clicking:
            print("\n[⌛]Clicking paused.\n[🌱] THE CYCLE WILL END AFTER CHECKING THE LAST POSITION")
        else:
            print("[⌛]Clicking resumed.")
        return True

# Add mouse listener
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()


# Function to handle keyboard events
def on_press(key):
    if key == keyboard.Key.space:
        print("\n[😸] EXIT THE PROGRAM AFTER THE CYCLE IS COMPLETED")
        exit_program.set()  # Signal the exit event
        return False

# Add keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

def capture_screenshot(bbox):
    margin_left, margin_top, width, height = bbox
    cropped_bbox = (margin_left + 100, margin_top + 500, width - 100, height - 200)  # Adjusted to include margins
    screenshot_path = "telegram_screenshot.png"
    screenshot = pyautogui.screenshot(region=cropped_bbox)  # Capture the screenshot within the adjusted region
    screenshot.save(screenshot_path)
    return screenshot_path


def find_blue_area(image):
    blue_color = (19, 199, 255)  # RGB value for the blue color code #13C7FF
    width, height = image.size
    image_data = image.load()

    for y in range(height):
        for x in range(width):
            if image_data[x, y][:3] == blue_color:
                return (x, y)

    return None


def process_image(bbox):
    screenshot_path = capture_screenshot(bbox)
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

    for idx, (highlight_margin_top, highlight_margin_right, highlight_margin_bottom, highlight_margin_left) in enumerate(highlight_areas):
        highlight_left = highlight_margin_left
        highlight_top = highlight_margin_top
        highlight_right = cropped_image.width - highlight_margin_right
        highlight_bottom = cropped_image.height - highlight_margin_bottom

        draw = ImageDraw.Draw(cropped_image)
        draw.rectangle(
            [(highlight_left, highlight_top), (highlight_right, highlight_bottom)],
            outline="red", width=1
        )

        coordinates.append((highlight_left, highlight_top, highlight_right, highlight_bottom))

    cropped_image_path = os.path.join(os.getcwd(), "cropped_highlighted_image.png")
    cropped_image.save(cropped_image_path)

    def drag_to_blue_area(start_idx):
        start_x = bbox[0] + crop_left + coordinates[start_idx][0] + (coordinates[start_idx][2] - coordinates[start_idx][0]) / 2
        start_y = bbox[1] + crop_top + coordinates[start_idx][1] + (coordinates[start_idx][3] - coordinates[start_idx][1]) / 2

        mouse_controller.position = (start_x, start_y)
        pyautogui.sleep(0.3)
        mouse_controller.press(Button.left)
        pyautogui.sleep(0.3)

        # Capture a screenshot after pressing the mouse button down
        intermediate_screenshot_path = capture_screenshot(bbox)
        intermediate_image = Image.open(intermediate_screenshot_path)

        # Find the area with the blue background
        blue_area_coords = find_blue_area(intermediate_image)
        if blue_area_coords:
            end_x = bbox[0] + crop_left + blue_area_coords[0]
            end_y = bbox[1] + crop_top + blue_area_coords[1]

            mouse_controller.position = (end_x, end_y)
            pyautogui.sleep(0.1)
            mouse_controller.release(Button.left)
            pyautogui.sleep(0.1)

            new_screenshot_path = capture_screenshot(bbox)
            new_image = Image.open(new_screenshot_path)

            if not images_are_equal(cropped_image, new_image):
                print(f"[✅] Success!")
                return True
            else:
                return False
        else:
            mouse_controller.release(Button.left)
            return False

    def images_are_equal(img1, img2):
        return ImageChops.difference(img1, img2).getbbox() is None

    for i in range(len(coordinates)):
        retries = 1
        while retries > 0:
            if drag_to_blue_area(i):
                break
            retries -= 1
    return True  # Return True after processing all coordinates


def process_loop(bbox):
    global pause_clicking
    while not exit_program.is_set():
        if pause_clicking:
            pyautogui.sleep(0.1)
            continue

        if not process_image(bbox):
            break


def main():

    print("[💲] PROGRAM STARTED!\n[😺] Press the right mouse to START \n[😺] Press the right mouse to PAUSE\n[😺] "
          "Press SpaceBar to EXIT the program")
    bbox = get_telegram_window_bbox()
    if bbox is None:
        print("[😿] Telegram window not found.")
        return

    window = gw.getWindowsWithTitle('Telegram')[0]
    window.activate()

    process_thread = threading.Thread(target=process_loop, args=(bbox,))
    process_thread.start()

    keyboard_listener.join()
    exit_program.set()  # Signal the exit event for the process loop
    process_thread.join()
    mouse_listener.stop()
    print("[🗿] Program exited.")


if __name__ == "__main__":
    main()

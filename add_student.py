import cv2
import pandas as pd
import os

# Directory to save student images
image_dir = "student_images"
os.makedirs(image_dir, exist_ok=True)

# CSV file to store student details
csv_file = "students.csv"


# Function to capture a student's image
def capture_image(roll_number, name):
    cap = cv2.VideoCapture(0)
    image_path = None  # Initialize image_path

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        cv2.imshow("Capture Image - Press 'c' to capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Save the image with a unique filename
            image_path = os.path.join(image_dir, f"{roll_number}_{name}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved at {image_path}")
            break

    cap.release()
    cv2.destroyAllWindows()
    return image_path


# Function to register a student's details
def register_student():
    roll_number = input("Enter roll number: ")
    name = input("Enter name: ")

    choice = input("Would you like to (1) Capture a new image or (2) Provide an existing image path? Enter 1 or 2: ")

    if choice == '1':
        # Capture and save the student's image
        image_path = capture_image(roll_number, name)
        if image_path is None:
            print("Image capture failed. Registration aborted.")
            return
    elif choice == '2':
        image_path = input("Enter the full path of the existing image: ")
        # Validate the provided image path
        if not os.path.isfile(image_path):
            print("Invalid image path. Please try again.")
            return
        # Copy the image to the student_images directory
        new_image_path = os.path.join(image_dir, f"{roll_number}_{name}{os.path.splitext(image_path)[1]}")
        os.rename(image_path, new_image_path)
        image_path = new_image_path
        print(f"Image copied to {image_path}")
    else:
        print("Invalid choice. Please try again.")
        return

    # Create or update the CSV file with the student's details
    student_data = {"Roll Number": [roll_number], "Name": [name], "Image Path": [image_path]}
    df = pd.DataFrame(student_data)

    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False)

    print(f"Student {name} registered successfully.")


# Run the registration function
register_student()

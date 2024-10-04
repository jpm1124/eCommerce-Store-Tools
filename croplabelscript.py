import os
from PyPDF2 import PdfReader, PdfWriter

# Paths to the input and output folders
# Make sure the folder paths are correct based on your setup
input_folder = r"Replace with file path of uncropped labels folder"  # Folder containing the original uncropped labels
output_folder = r"Replace with file path of cropped labels folder"  # Folder where cropped labels will be saved

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # Creates the output folder if it doesn't already exist

def crop_pdf_to_label(input_pdf, output_pdf):
    """
    Crops a single PDF file to fit the dimensions of a 4x6 label.

    Parameters:
    input_pdf (str): Path to the input PDF file to be cropped.
    output_pdf (str): Path where the cropped output PDF will be saved.
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        # Get the original dimensions of the PDF page
        orig_width = float(page.mediabox.upper_right[0])  # Original page width in points
        orig_height = float(page.mediabox.upper_right[1])  # Original page height in points

        # Define the start positions and dimensions for cropping the label
        label_x_start = 100      # X-coordinate where the cropping starts (adjusted to fit label content)
        label_y_start = 450      # Y-coordinate where the cropping starts (adjusted to fit label content)
        label_width = 432        # Width of the label in points (6 inches in landscape mode)
        label_height = 288       # Height of the label in points (4 inches in landscape mode)

        # Calculate the coordinates for the lower-left and upper-right corners of the crop box
        lower_left_x = label_x_start
        lower_left_y = label_y_start
        upper_right_x = label_x_start + label_width
        upper_right_y = label_y_start + label_height

        # Apply the calculated crop box dimensions to the page
        page.cropbox.lower_left = (lower_left_x, lower_left_y)
        page.cropbox.upper_right = (upper_right_x, upper_right_y)

        # Add the cropped page to the writer object
        writer.add_page(page)

    # Write the modified pages to a new output PDF file
    with open(output_pdf, "wb") as out_file:
        writer.write(out_file)  # Save the cropped PDF to the specified output path

# Iterate through each PDF file in the input folder and apply cropping
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):  # Process only PDF files
        input_path = os.path.join(input_folder, filename)  # Full path to the input file
        output_path = os.path.join(output_folder, f"cropped_{filename}")  # Full path to the output file

        # Perform the cropping operation on the PDF
        crop_pdf_to_label(input_path, output_path)
        print(f"Cropped {filename} and saved as {output_path}")  # Print status message for each processed file

print("All labels have been processed and saved in the output folder.")

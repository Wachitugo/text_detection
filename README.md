# README

## Orientation Detection and Number Recognition in Images

This Python script processes a folder of images to detect and extract numerical information from the top portion of each image. The primary functionality includes detecting if the image is upside down, rotating it if necessary, extracting the region of interest (ROI) for number detection, and using OCR (Optical Character Recognition) to read the detected numbers. 

### Features
1. **Orientation Detection**  
   - Determines if the image is upside down by analyzing pixel density in the top and bottom halves.
   - Automatically rotates the image by 180° if necessary.

2. **Region of Interest (ROI) Detection**  
   - Focuses on the top half of the image for number extraction.
   - Resizes and enhances the contrast of the ROI to improve OCR accuracy.

3. **OCR (Optical Character Recognition)**  
   - Uses `pytesseract` to extract numerical information from the processed ROI.
   - Configured to detect numbers only and ignore other characters.

4. **Number Filtering and Deduplication**  
   - Ensures extracted numbers are at least 6 digits long.
   - Filters out numbers similar to already detected ones, based on a specified tolerance for differences.

### How It Works
1. The script iterates over all images in a specified folder (`images`).
2. Each image is checked for orientation and corrected if needed.
3. The top half of the image is extracted, resized, and preprocessed to enhance OCR results.
4. OCR is performed using multiple configurations to maximize recognition accuracy.
5. The detected numbers are validated and stored if they are unique and sufficiently different from previously detected numbers.

### Technologies and Libraries Used
- **Python**: The programming language used for implementation.
- **OpenCV**: For image processing tasks such as grayscale conversion, resizing, thresholding, and morphological operations.
- **NumPy**: To handle numerical operations on image data efficiently.
- **Tesseract OCR**: An open-source OCR engine used via the `pytesseract` Python wrapper to extract textual information.
- **OS**: For handling file system operations, such as reading images from the folder.
- **Image Preprocessing Techniques**:
  - **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: To enhance image contrast.
  - **Thresholding**: For binarizing images.
  - **Morphological Operations**: To clean up noise in the binarized images.

### Setup and Usage
1. **Prerequisites**:
   - Python 3.6 or later.
   - Installed dependencies: `opencv-python`, `numpy`, `pytesseract`.
   - Tesseract OCR installed on your system.

2. **Installation**:
   - Clone or download the repository.
   - Install the dependencies by running:
     ```bash
     pip install opencv-python-headless numpy pytesseract
     ```
   - Ensure Tesseract OCR is properly installed and added to your system PATH.

3. **Input Folder**:
   - Place your images in a folder named `images` in the root directory (or modify the `input_folder` path in the script).

4. **Run the Script**:
   - Execute the script:
     ```bash
     python script.py
     ```

5. **Output**:
   - The detected numbers are printed to the console, along with their corresponding image filenames.
   - Unique and valid numbers are stored in the `numeros_detectados` list.

### Customization
- **Tolerance for Similar Numbers**:
  Adjust the `tolerancia` parameter in the `son_similares` function to fine-tune how similar two numbers can be before being considered duplicates.
  
- **ROI Selection**:
  Modify the ROI height in the `detect_number_roi` function to focus on different parts of the image.

- **OCR Configurations**:
  Add or modify configurations in the `configs` list for `pytesseract` to test different OCR modes.

### Limitations
- The script assumes that the numbers to be detected are located in the top half of the image.
- It is optimized for numerical data only; it will not detect or process text or other types of data.

### Potential Applications
- Automatic number extraction from scanned documents or forms.
- Preprocessing for datasets requiring OCR of numerical fields.
- Data validation in scenarios where unique numerical identifiers are essential.


# Criminal Face Recognition

This program uses the face recognition module and a webcam to compare faces against an encoding bank of FBI's most wanted posters.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/josec40/CriminalFaceRecognition.git
   ```
2. Navigate to the project directory:
   ```bash
   cd CriminalFaceRecognition
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the program:
   ```bash
   python main.py
   ```

## Customaization
A database of images of criminals is able to be linked to the program. As long as the names of the file images is in 'first_name last_name' format, and the images are jpg, the program will be able to use the images. Import your own images into the 'MostWantedList' folder to expand the scope of the encoding bank.

## Notes
Tolerance for face encoding comparasion was altered from the default 0.6 to 0.55 as locally run tests performed better with the 0.55 tolerance.
Versions of the imported libraries and modules are sensitive when working with face_recognition libray. When working with other versions of, for example numpy, issues were encountered. Install the exact versions of the libraries from requirements.txt for best performace.

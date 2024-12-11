# ASL Video Scraper and Hand Tracking Project

This repository contains two Python scripts designed to support American Sign Language (ASL) research and development:

1. **scrape_signasl_org.py**: A web scraper for downloading ASL video resources from [SignASL.org].
2. **watching_hands.py**: A tool to track hand movements in video files and perform spline-based interpolation for data analysis.

## Features

### scrape_signasl_org.py
- Downloads ASL videos for words starting with the letter 'A'.
- Saves videos locally in a specified directory.
- Extracts metadata (e.g., word, video URL, save path) and stores it in a CSV file.
- Implements multithreading for faster scraping and downloading.
- Handles HTTP errors gracefully and ensures existing files are not re-downloaded.

### watching_hands.py
- Processes videos to track hand landmarks using MediaPipe.
- Extracts x, y, z coordinates for the tip of the index finger.
- Interpolates missing data using splines for smoother trajectory analysis.
- Visualizes results through detailed plots of x, y, z coordinates over time.

## Prerequisites

- Python 3.7 or higher
- Required Python libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `opencv-python-headless`
  - `mediapipe`
  - `gdown`
  - `requests`
  - `beautifulsoup4`
- GPU support is recommended for `watching_hands.py` but not mandatory.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-repo>.git
   cd <your-repo>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### scrape_signasl_org.py

1. Prepare a text file containing the target words, one word per line. Ensure the words start with the letter 'A'.

2. Update the `input_file_path` in the script to point to your text file.

3. Run the script:
   ```bash
   python scrape_signasl_org.py
   ```

4. Check the `ASL_Videos` directory for downloaded videos and metadata CSV.

### watching_hands.py

1. Replace the placeholder Google Drive URL with your video file's link in the `file_url` variable.

2. Run the script:
   ```bash
   python watching_hands.py
   ```

3. View the interpolated and smoothed hand trajectories in the generated plots.

## Outputs

- **scrape_signasl_org.py**:
  - Downloaded ASL videos stored in the `ASL_Videos` directory.
  - Metadata stored in `metadata.csv`.
- **watching_hands.py**:
  - Interpolated hand trajectory plots.

## Contributing

If you have suggestions or improvements, feel free to create a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [SignASL.org] for providing ASL video resources.
- MediaPipe and its contributors for the hand-tracking framework.


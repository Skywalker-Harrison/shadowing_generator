# Shadow Reading Program

A powerful tool for language learners to practice shadow reading using video content with subtitles.

![Shadow Reading](https://img.shields.io/badge/Language%20Learning-Shadow%20Reading-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## What is Shadow Reading?

Shadow reading is a language learning technique where you repeat what you hear immediately after hearing it, like a "shadow" following the original speaker. This program enhances this technique by:

1. Breaking down videos into complete sentences (not arbitrary subtitle chunks)
2. Allowing you to repeat each sentence multiple times
3. Controlling when subtitles appear (e.g., only on the second repetition)
4. Creating a customized video for your practice sessions

## Features

- **Smart Sentence Detection**: Parses SRT subtitle files and intelligently splits content by complete sentences
- **Customizable Repetitions**: Set how many times each sentence repeats
- **Flexible Subtitle Display**: Choose which repetition shows subtitles (all, first, second, etc.)
- **Batch Processing**: Apply settings to all sentences or specific ranges
- **Dual Interface**: Use either the graphical interface or command line
- **Progress Tracking**: Visual progress bar during video generation

## Requirements

- Python 3.6 or higher
- Required Python packages:
  ```
  pysrt
  moviepy
  nltk
  ```

## Installation

1. Clone this repository or download the source code:
   ```bash
   git clone https://github.com/yourusername/shadow-reading.git
   cd shadow-reading
   ```

2. Install the required dependencies:
   ```bash
   pip install pysrt moviepy nltk
   ```

## Quick Start

### Using the GUI (Recommended for Beginners)

1. Run the program:
   ```bash
   python generate_video.py
   ```

2. In the interface:
   - Select your video file
   - Select your subtitle file (or first run `python parse_srt.py` to process it)
   - Set your preferences
   - Generate your shadow reading video

### Using the Command Line (For Advanced Users)

1. Process your subtitle file:
   ```bash
   python parse_srt.py --srt your_video.srt
   ```

2. Generate your shadow reading video:
   ```bash
   python generate_video.py --video your_video.mp4 --json sentences.json --output shadow_reading.mp4
   ```

## Detailed Usage Guide

### Step 1: Parse Subtitle File

First, process your SRT subtitle file to split it into complete sentences:

```bash
python parse_srt.py --srt your_video.srt --output sentences.srt --json sentences.json
```

Parameters:
- `--srt`: Path to your SRT subtitle file (required)
- `--output`: Path for the output SRT file (default: sentences.srt)
- `--json`: Path for the output JSON file (default: sentences.json)

Alternatively, use the test script with default values:
```bash
python test_parse_srt.py
```

This generates:
- `sentences.srt`: SRT file with content split by sentences
- `sentences.json`: JSON file with sentence information for video generation

### Step 2: Generate Shadow Reading Video

#### Using the Graphical Interface

Run:
```bash
python generate_video.py
```

The interface allows you to:
1. Select your original video file
2. Select the JSON file from Step 1
3. Specify where to save the output video
4. Edit sentence repetition settings:
   - Set which repetition displays subtitles (0=All, 1=First, 2=Second, etc.)
   - Apply settings to all sentences at once
   - Apply settings to specific sentence ranges
   - Set individual repetition counts for each sentence
5. Generate your custom shadow reading video

#### Using the Command Line

```bash
python generate_video.py --video your_video.mp4 --json sentences.json --output shadow_reading.mp4 --subtitle-display 2
```

Parameters:
- `--video`: Path to your original video file (required)
- `--json`: Path to the sentence information JSON file (required)
- `--output`: Path for the output video file (default: output.mp4)
- `--edit`: Open the editing interface to set repetition counts
- `--subtitle-display`: Which repetition shows subtitles (default: 2)

Example workflow:
```bash
# First, edit repetition settings
python generate_video.py --video your_video.mp4 --json sentences.json --edit

# Then generate the video with subtitles on the second repetition
python generate_video.py --video your_video.mp4 --json sentences.json --output shadow_reading.mp4 --subtitle-display 2
```

## File Structure

- `parse_srt.py`: Core script for parsing SRT files and splitting by sentences
- `test_parse_srt.py`: Helper script to test the parsing functionality
- `generate_video.py`: Main program for creating shadow reading videos
- `sentences.srt`: Generated SRT file with sentence-based subtitles
- `sentences.json`: Generated JSON file with sentence timing information
- `output.mp4`: Default name for the generated shadow reading video

## Tips for Effective Shadow Reading

1. **Start with shorter videos**: 2-5 minutes is ideal for beginners
2. **Choose appropriate content**: Select material slightly above your current level
3. **Repetition settings**:
   - Beginners: 3-4 repetitions with subtitles on all or most repetitions
   - Intermediate: 2-3 repetitions with subtitles on the second repetition
   - Advanced: 1-2 repetitions with minimal subtitle use
4. **Practice regularly**: 15-30 minutes daily is more effective than occasional longer sessions

## Troubleshooting

### Common Issues

- **Video processing is slow**: Processing large video files requires significant computing power. Try using shorter video clips.
- **Subtitle timing issues**: Ensure your SRT file is properly synchronized with your video.
- **Encoding problems**: Make sure your subtitle files use UTF-8 encoding.
- **Missing dependencies**: Verify all required packages are installed with `pip list`.

### Error Messages

- **"No module named 'pysrt'"**: Run `pip install pysrt` to install the missing package.
- **"Error processing SRT file"**: Check that your SRT file is valid and properly formatted.
- **"Error generating video"**: Ensure your video file is in a supported format (MP4 recommended).

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs**: Open an issue describing the bug and how to reproduce it
2. **Suggest features**: Open an issue describing your proposed feature
3. **Submit pull requests**: Fork the repository, make your changes, and submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the developers of pysrt, moviepy, and nltk
- Inspired by language learning techniques from polyglots and language teachers worldwide 
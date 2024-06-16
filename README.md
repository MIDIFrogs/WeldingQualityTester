# Welding Quality Tester
by [PerdoTeam [MIDIFrogs]](https://github.com/MIDIFrogs)

[![CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE.md)
[![Number of GitHub stars](https://img.shields.io/github/stars/MIDIFrogs/WeldingQualityTester?logo=github)](https://github.com/MIDIFrogs/WeldingQualityTester/stargazers)

![Demo GIF](Resources/demo.gif)

## Features
- ✅ Simple to setup and use
- 🧩 Extensible
- 🌬️ lightweight

### Prerequisites:
- Installed Python v3.10+
- [Ultralytics](https://github.com/ultralytics/ultralytics) library (can be downloaded from requirements)

## Quick start (Jupiter)
Open and run `example.ipynb` file to predict defects on custom images directory. <br/>
The detection results are stored in `out/submission.csv` file.

## Getting started
1. Open the terminal in repo directory
2. Run `pip install -r requirements.txt`

### CSV dataset processing
3. Run `python csvRunner.py`
4. Input path to the dataset directory
5. After processing you'll get `submission.csv` file with all the processing results.

### Telegram bot host (recommended for skilled users)
3. Setup your Telegram bot and get the token
4. Add your bot token to the `startup.config` file by key `Token`
5. Run `python weldingBot.py`
6. Feel free to use your bot!

## Code overview
The whole project contain the following scripts:
1. [weldingBot](weldingBot.py) - The bot client configurable using `startup.config` file.
2. [csvRunner](csvRunner.py) - Dataset validation script for performance testing purposes.

Also there are two utilitary scripts:
1. [drawBox](drawBox.py) is a tool needed for image outline.
2. [vizualizer](vizualizer.py) is a helper script for dataset image highlighting.

The training code is in [weldingtrain](weldingtrain.ipynb) Jupyter notebook configured for Kaggle training.

## Need help?
Write me in [Telegram](https://t.me/ioexcept10n) or open an [issue](https://github.com/MIDIFrogs/WeldingQualityTester/issues/new/choose). Feel free to ask any questions!

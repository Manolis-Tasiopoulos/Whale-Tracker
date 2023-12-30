# Whale-Tracker

## Description
This repo is a project focused on tracking and analyzing data, related to cryptocurrency transcactions, with an integration of a Telegram bot for sending notifications or updates.
The target audience for this project are individuals or entities interested in financial tracking, market analysis, or automated data processing.

## Installation
Before running the script, make sure you have the following:

- Python 3.x installed on your system.

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/kyratzakos/Whale-Tracker.git
   ```
   or
   ```bash
   git clone https://github.com/Manolis-Tasiopoulos/Whale-Tracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Whale-Tracker
   ```

3. Install the required Python libraries from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

This will install the necessary libraries, including:

-`requests` for making HTTP requests.

-`blockcypher`: A Python library for interacting with BlockCypher's API, which provides tools for working with blockchain data and networks like Bitcoin.

-`yfinance`: A Python library used for downloading historical market data from Yahoo Finance, including cryptocurrency prices and split data.

-`python_telegram_bot`: A library for building Telegram bots in Python.

-`telegram`: A Python interface for the Telegram Bot API.

-`pandas`: A powerful data analysis and manipulation library for Python, widely used for data preprocessing, cleaning, analysis, and visualization in tabular form.

## Usage
1. Open the `tracker.py` file and fill out the following placeholders with appropriate values:

   - `address`: Replace `'1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ'` with the actual address you want to get updates for any buy/sell moves in the future.

2. Create a `.env` file based on `.env.example` and fill out the following placeholders with appropriate values:

   ```bash
   BlockCypher_token = "your_token_here"
   Telegram_token = "your_api_key_here"
   ```
3. Run the script:

   ```bash
   python telegramBOT.py
   ```
    and follow the instructions on the terminal.

## Contributing

If you'd like to contribute to this project, please follow the standard GitHub workflow:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear and concise messages.
4. Push your branch to your fork.
5. Create a pull request to merge your changes into the main repository.

## Issues
If you encounter any issues or have suggestions for improvements, please open an issue on the [Issues](https://github.com/kyratzakos/Whale-Tracker/issues) page.

Have fun!

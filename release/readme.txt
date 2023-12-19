================================================================================
CSV Email Validator Application
================================================================================

Description:
------------
The CSV Email Validator Application provides a graphical interface for users to upload a CSV file containing names and email addresses. The application will process the data, validate email addresses, and allow users to save the cleaned data to a new CSV file. The output format is in the order: "Email", "First Name", "Last Name".

Requirements:
-------------
- Python (version 3.x recommended)
- pandas library
- tkinter library

Installation:
-------------
1. Ensure Python is installed on your machine.
2. Install the required libraries using pip:
	pip install pandas

Usage:
------
1. Run the application:
	Command Prompt: python main.py
2. Click on "Browse" on the GUI to upload a CSV file.
3. The application will auto-detect the column names; however, you can choose the desired columns for "First Name", "Last Name", and "Email" from the dropdown boxes.
4. Click on "Process CSV" to process the data.
5. After processing, the application will prompt you to save the cleaned data to a new CSV file. You can choose to save or view the cleaned data directly in the application.
6. The feedback section displays the cleaned data and provides information about the number of valid entries processed and any invalid email addresses found.

Limitations:
------------
- The application assumes that the CSV contains columns related to "First Name", "Last Name", and "Email". If any of these columns are absent in the CSV, an error will be displayed.
- The email validation is based on a simple regular expression pattern. Some edge cases might not be handled.

Support:
--------
For any issues or queries, please contact uncommondll@gmail.com.

License:
--------
This software is provided "as-is" without any warranties. Users are free to use and distribute with attribution.

Copyright 2023 UncommonDLL, LLC

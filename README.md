>**Note**: Please **fork** this Udacity repository so you have a **remote** repository in **your** GitHub account. Then you can clone the remote repository to your local machine. Later, as a part of the project, you will push your changes to the remote repository in your GitHub account.

# Bikeshare Project

This project explores data from bikeshare systems in several major U.S. cities.  
The goal is to use Python to perform data analysis and extract meaningful statistics from shared bicycle usage data.


## 📄 Project Overview

The project includes:
- a single Python script (`bikeshare-starter.py`) that handles user interaction, data loading, and calculations
- one or more `.csv` files containing anonymized bikeshare trip data

The program guides the user through selecting:
- a city to analyze
- an optional month filter
- an optional day-of-week filter


## What the Program Does
- Loads bikeshare data for a selected city  
- Allows filtering by month and day  
- Calculates statistics such as:
  - Most common travel times  
  - Popular stations and routes  
  - Total and average trip duration  
  - User demographics (when available)

## How to Run
Run the script in your terminal:

```bash
python bikeshare-starter.py



## Known Issues
Currently, the bikeshare data files contain a few inconsistencies in timestamps.  
These do not break the program but may slightly affect time‑based statistics.

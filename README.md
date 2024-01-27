# Git Profile Manager

This Python script allows users to manage their Git profiles easily. It enables the addition and deletion of both global and local Git profiles. The script is designed to work on systems with Python installed and is intended for users who work with multiple Git configurations.

## Features

- **Add Git Profiles**: Add new global or local Git profiles.
- **Delete Git Profiles**: Remove existing global or local Git profiles.
- **List Git Profiles**: Display all global and local Git profiles in a specified directory.

## Prerequisites

- Python 3.x
- Git

## Installation

1. Clone the repository or download the script to your local machine.
2. Run the script using Python.

   ```bash
   python manage_git_profiles.py
   ```

## Usage

When you run the script, it will provide the following options:

- **Add a new profile**: Add a new global or local Git profile by specifying a username and email. For local profiles, you will also need to specify the path of the local repository.
- **Delete an existing profile**: Choose to delete either a global or local profile. For local profiles, the script will show the associated repository.
- **Exit**: Exit the script.

## Adding a New Profile

1. Choose add when prompted.
2. Enter the username and email for the new profile.
3. Specify whether the profile is global or local. If local, enter the path to the local repository.

## Deleting a Profile
1. Choose delete when prompted.
2. Select global or local.
3. Choose the profile to delete from the listed profiles.

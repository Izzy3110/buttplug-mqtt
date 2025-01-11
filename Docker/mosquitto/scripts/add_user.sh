#!/bin/bash

# Default paths and variables
PASSWORD_FILE="/path/to/mosquitto_passwd_file"
PASSWORD_INPUT_FILE=""
USERNAME=""

# Function to display usage
usage() {
    echo "Usage: $0 --user <username> --password-file <file>"
    echo ""
    echo "  --user            The username to add."
    echo "  --password-file   File containing the password in plain text."
    exit 1
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --user)
            USERNAME="$2"
            shift 2
            ;;
        --password-file)
            PASSWORD_INPUT_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
done

# Validate inputs
if [[ -z "$USERNAME" || -z "$PASSWORD_INPUT_FILE" ]]; then
    echo "Error: Both --user and --password-file are required."
    usage
fi

if [[ ! -f "$PASSWORD_INPUT_FILE" ]]; then
    echo "Error: Password file '$PASSWORD_INPUT_FILE' does not exist."
    exit 1
fi

# Read the password from the file
PASSWORD=$(cat "$PASSWORD_INPUT_FILE")

# Add the user to the Mosquitto password file
if mosquitto_passwd -b "$PASSWORD_FILE" "$USERNAME" "$PASSWORD"; then
    echo "User '$USERNAME' added successfully to the password file."
else
    echo "Failed to add user '$USERNAME'."
    exit 1
fi

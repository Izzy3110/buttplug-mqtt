"""
This module provides functionality to generate
random passwords using a customizable set of characters.

Functions:
    generate_password(chars_list=string.printable, length=12):
        Generates a random password using the specified characters and length.
"""
import os
import random
import string
import argparse
import shutil
from datetime import datetime


def str_to_file(output_string: str, filename=".current_password.temp", filemode="w"):
    with open(filename, filemode) as target_file:
        target_file.write(output_string)


def generate_password(chars_list=string.printable, length=12):
    """
    Generate a random password using the given string of characters and specified length.

    Args:
        chars_list (str, optional): A string of characters to use for generating the password.
                                    Defaults to all printable characters, including whitespace.
        length (int, optional): The desired length of the password. Defaults to 12.

    Raises:
        ValueError: If `length` is not a positive integer.

    Returns:
        str: The generated password.
    """
    chars_list = chars_list.strip()
    if length <= 0:
        raise ValueError("length must be a positive integer.")

    return ''.join(random.choice(chars_list) for _ in range(length))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a random password.")
    parser.add_argument(
        'length',
        type=int,
        nargs='?',
        default=12,
        help="Length of the generated password (default: 12)."
    )
    parser.add_argument(
        '-l', '--length-flag',
        type=int,
        help="Length of the generated password (overrides positional length)."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Determine the length, giving priority to the flag
    password_length = args.length_flag if args.length_flag is not None else args.length

    # Generate and print the password
    GENERATED_PASSWORD = generate_password(length=password_length)
    dir_content: list = os.listdir(os.path.abspath(os.getcwd()))

    if ".current_password.temp" in dir_content:
        print("file exists")
        if ".last_password.temp" in dir_content:
            current_datestring = datetime.now().strftime("%Y%m%d-%H%M%S")
            shutil.copyfile(
                src=os.path.abspath(os.path.join(os.path.abspath(os.getcwd()), ".last_password.temp")),
                dst=os.path.join(os.getcwd(), f".last_password-{current_datestring}.temp"))
            str_to_file(GENERATED_PASSWORD)
        else:
            shutil.copyfile(
                src=os.path.abspath(os.path.join(os.path.abspath(os.getcwd()), ".current_password.temp")),
                dst=os.path.join(os.getcwd(), ".last_password.temp"))
            str_to_file(GENERATED_PASSWORD)
    else:
        str_to_file(GENERATED_PASSWORD, filename="passwd.clr")

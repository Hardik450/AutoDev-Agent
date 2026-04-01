import requests
import json
import os

API_URL = "https://official-joke-api.appspot.com/random_joke"
OUTPUT_FILE = "jokes.txt"

def get_random_joke():
    """Fetches a random joke from the API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        joke_data = response.json()

        setup = joke_data.get("setup")
        punchline = joke_data.get("punchline")

        if setup and punchline:
            return f"Setup: {setup}\nPunchline: {punchline}"
        else:
            return "Error: Could not retrieve complete joke (missing setup or punchline)."

    except requests.exceptions.RequestException as e:
        return f"Error fetching joke from API: {e}"
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON response from API."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def save_joke_to_file(joke_content, filename):
    """Appends the joke content to the specified file."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(joke_content + "\n---\n") # Add a separator for readability
        print(f"Joke successfully saved to '{filename}'.")
    except IOError as e:
        print(f"Error saving joke to file '{filename}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving file: {e}")

if __name__ == "__main__":
    print("Attempting to fetch a random joke...")
    joke = get_random_joke()

    if joke.startswith("Error"):
        print(joke) # Print the error message directly
    else:
        print("\n--- Retrieved Joke ---")
        print(joke)
        print("----------------------\n")
        save_joke_to_file(joke, OUTPUT_FILE)
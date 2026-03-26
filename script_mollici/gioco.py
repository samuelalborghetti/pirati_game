from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def load_image(file_name):
    return pygame.image.load(BASE_DIR / file_name)


def spostamento_pos_to_pos(...):
    # Your code here
    pass  # Replace with actual implementation


# Example of loading an image
image = load_image('assets/image.png')
# Continue with other image loading calls accordingly
def another_function(...):
    # Refer to load_image for any asset
    image = load_image('assets/another_image.png')

    # Continue with the function as required

    # Remember to remove all conflicting markers
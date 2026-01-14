import os

folders = [
    "data/raw",
    "data/processed",
    "data/external",
    "notebooks",
    "src",
    "tests",
    "models",
    "reports/figures",
    "images"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Optional placeholder files
open("README.md", "a").close()
open("requirements.txt", "a").close()
open("src/__init__.py", "a").close()
open("notebooks/01_data_exploration.ipynb", "a").close()

print("Project structure created!")

# Recipe Manager (Basic Version)

A simple command-line recipe manager that allows you to:
- Create recipes with structured ingredients (name, quantity, unit)
- View all recipes
- Search recipes by ingredient
- Save recipes to a JSON file for persistence

## Features
- **Add Recipe**: Interactive recipe creation with ingredients and instructions
- **View Recipes**: List all recipes with their ingredient counts
- **Search by Ingredient**: Find recipes that contain a specific ingredient
- **Persistent Storage**: Recipes are saved to `recipes.json` and loaded on start

## Installation
No dependencies required! Just Python 3.6+.

## Usage
1. Run the program:
    ```bash
   python recipe_manager.py
   

2. Choose from the menu:

    1: View all recipes

    2: Add new recipe

    3: Search recipes by ingredient

    4: Exit

Example Workflow
1. Add a recipe with structured ingredients:
    Recipe: Pancakes
    Ingredients:
      - 1.5 cups flour
      - 2 tbsp sugar
      - 1 cup milk
2. Search for recipes containing "milk"
3. View your recipe collection
   
   File Structure
recipe_manager.py: Main program

recipes.json: Data file (automatically created)

README.md: This documentation

    Future Enhancements
This is the basic version. Planned features include:
    Edit/delete recipes
    Recipe categories/tags
    Search by multiple criteria
    Recipe scaling
    Export/import

Developer: Kirubel Seifu
import json
import os

# File Path For Persistent Storage
RECIPE_FILE = "recipes.json"

def load_recipes():
    """Load All Recipes From The Json File."""
    if not os.path.exists(RECIPE_FILE):
        return []
    try:
        with open(RECIPE_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Error Loading Recipes. Starting With Empty List.")
        return []

def save_recipes(recipes):
    """Save All The Recipes To The JSON File."""
    try: 
        with open(RECIPE_FILE, 'w') as file:
            json.dump(recipes, file, indent=2)
    except Exception as e:
        print(f"❌ Error saving recipes: {e}")
        
def search_by_ingredient(recipes, ingredient_name):
    """Search For Recipes Containing A Specific Ingredient."""
    ingredient_name = ingredient_name.lower()
    found_recipes = []
    
    for recipe in recipes: 
        # Check Each Ingredient In This Recipe
        for ing in recipe['ingredients']:
            if ingredient_name in ing['name'].lower():
                found_recipes.append(recipe)
                break
    return found_recipes       

def create_recipe():
    """Interactively Create A New Recipe With Structured Ingredients."""
    print("\n--- Create New Recipe ---")
    name = input("Recipe name: ")
    
    # Collect Ingredients
    ingredients = []
    print("\n Add Ingredients (Leave Name Empty When Done): ")
    while True:
        ing_name = input("Ingredient Name: ").strip()
        if not ing_name:
            break
        
        try:
            quantity = float(input(f"Quantity Of {ing_name}: "))
            unit = input(f"Unit (cup, tbsp, piece, etc.): ").strip()
            
            ingredients.append({
                "name": ing_name.lower(),
                "quantity": quantity,
                "unit": unit
            })  
            print(f"✅ Added {quantity} {unit} of {ing_name}")
        except ValueError:
            print ("❌ Quantity Must Be A Number. Try Again.")
            
    # Collect Instructions
    instructions = []
    print("\n Add Instructions (Leave Empty When Done.): ")
    while True:
        step = input(f"Step {len(instructions) + 1}: ").strip()
        if not step:
            break
        instructions.append(step)
    
    # Build The Complete Recipe Dictionary
    recipe = {
        "name": name,
        "ingredients": ingredients,
        "instructions": instructions,
        "tags": []
    } 
    
    return recipe   

def display_recipe(recipe):
    """Display A Single Recipe In A Readable Format."""
    print(f"\n 📖 {recipe['name']}")
    print("=" * 40)
    
    print("Ingredients: ")
    for ing in recipe['ingredients']:
        print(f" •{ing['quantity']} {ing['unit']} {ing['name']}")
    
    print("\n Instructions:")
    for i, step in enumerate(recipe['instructions'], 1):
        print(f" {i}.{step}")
        
    if recipe.get('tags'):
        print(f"\n Tags: {', '.join(recipe['tags'])} ")

def main():
    """Main program loop"""
    recipes = load_recipes()
    print(f"📚 Recipe Manager - {len(recipes)}) recipes loaded")
    
    while True:
        print("\n" + "=" * 40)
        print("1. View All Recipes")
        print("2. Add New Recipe")
        print("3. Search Recipe")
        print("4. Exit")
        
        choice = input("\n Your Choice (1-4): ")
        
        if choice == "1":
            print(f"\n📚 All Recipes ({len(recipes)} total): ")
            for i, recipe in enumerate(recipes, 1):
                print(f"{i}.{recipe['name']}) ({len(recipe['ingredients'])} ingredients)")
                
        elif choice == "2":
            new_recipe = create_recipe()
            recipes.append(new_recipe)
            save_recipes(recipes)
            print(f"\n ✅'{new_recipe['name']}' Saved Successfully!")
        elif choice == "3":
            search_term = input("Search For Ingredient: ").strip()
            if search_term:
                results = search_by_ingredient(recipes, search_term)
                print(f"\n🔍 Found {len(results)} recipes with '{search_term}': ")
                for recipe in results:
                    print(f" • {recipe['name']}")
        elif choice == "4":
            save_recipes(recipes)
            print("\n 👋 Recipes Saved. GoodBye!")
            break
        else:
            print("❌ Invalid Choice. Please Enter 1-4.")
            
if __name__ == "__main__":
    main()
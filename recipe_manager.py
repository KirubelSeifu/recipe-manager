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
        
def search_by_ingredient(recipes, ingredient_name, exact_match=False):
    """Search For Recipes Containing A Specific Ingredient."""
    ingredient_name = ingredient_name.lower()
    found_recipes = []
    
    for recipe in recipes: 
        for ing in recipe['ingredients']:
            if exact_match:
                if ingredient_name == ing['name'].lower():
                    found_recipes.append(recipe)
                    break
            else:
                if ingredient_name in ing['name'].lower():
                    found_recipes.append(recipe)
                    break
    return found_recipes

def search_by_name(recipes, name_query):
    """Search Recipes By Name (Supports Partial Matching)."""
    name_query = name_query.lower()
    return [recipe for recipe in recipes 
            if name_query in recipe['name'].lower()]

def search_by_tag(recipes, tag_query):
    """Search Recipes By Tags."""
    tag_query = tag_query.lower()
    found_recipes = []
    
    for recipe in recipes:
        tags = recipe.get('tags', [])
        for tag in tags:
            if tag_query in tag.lower():
                found_recipes.append(recipe)
                break
    return found_recipes

def search_by_cooking_time(recipes, max_time=None, min_time=None):
    """Search recipes by estimated cooking time."""
    found_recipes = []
    
    for recipe in recipes:
        # Check if recipe has cooking_time field
        cooking_time = recipe.get('cooking_time')
        if cooking_time is None:
            continue
            
        try:
            time_minutes = int(cooking_time)
            match = True
            
            if max_time is not None and time_minutes > max_time:
                match = False
            if min_time is not None and time_minutes < min_time:
                match = False
                
            if match:
                found_recipes.append(recipe)
        except (ValueError, TypeError):
            continue
            
    return found_recipes

def search_by_difficulty(recipes, difficulty_level):
    """Search recipes by difficulty level (Easy, Medium, Hard)."""
    difficulty_level = difficulty_level.lower()
    found_recipes = []
    
    for recipe in recipes:
        recipe_difficulty = recipe.get('difficulty', '').lower()
        if recipe_difficulty == difficulty_level:
            found_recipes.append(recipe)
            
    return found_recipes

def advanced_search(recipes):
    """Perform Advanced Search With Multiple Criteria."""
    print("\n" + "=" * 50)
    print("🔍 ADVANCED SEARCH")
    print("=" * 50)
    
    # Collect Search Criteria
    criteria = {}
    
    # Search By Name
    name_query = input("Recipe Name Contains (Leave Empty To Skip): ").strip()
    if name_query:
        criteria['name'] = name_query
    
    # Search By Ingredient
    ingredient_query = input("Ingredient Contains (Leave Empty To Skip): ").strip()
    if ingredient_query:
        exact_match = input("Exact Match? (y/n): ").strip().lower() == 'y'
        criteria['ingredient'] = ingredient_query
        criteria['exact_match'] = exact_match
    
    # Search By Tag
    tag_query = input("Tag Contains (Leave Empty To Skip): ").strip()
    if tag_query:
        criteria['tag'] = tag_query
    
    # Search By Cooking Time
    time_query = input("Maximum Cooking Time In Minutes (Enter 0 to Skip): ").strip()
    if time_query and time_query.isdigit():
        criteria['max_time'] = int(time_query)
    
    # Search By Ingredient Count
    max_ingredients = input("Maximum Number Of Ingredients (Enter 0 to Skip): ").strip()
    if max_ingredients and max_ingredients.isdigit():
        criteria['max_ingredients'] = int(max_ingredients)
    
    # Search By Difficulty
    difficulty_query = input("Difficulty (Easy/Medium/Hard, Leave Empty To Skip): ").strip()
    if difficulty_query:
        criteria['difficulty'] = difficulty_query
    
    # Apply All Criteria
    results = recipes.copy()
    
    if 'name' in criteria:
        results = search_by_name(results, criteria['name'])
    
    if 'ingredient' in criteria:
        results = search_by_ingredient(results, criteria['ingredient'], 
                                      criteria.get('exact_match', False))
    
    if 'tag' in criteria:
        results = search_by_tag(results, criteria['tag'])
    
    if 'max_time' in criteria:
        results = search_by_cooking_time(results, max_time=criteria['max_time'])
    
    if 'max_ingredients' in criteria:
        results = search_by_ingredient_count(results, max_count=criteria['max_ingredients'])
    
    if 'difficulty' in criteria:
        results = search_by_difficulty(results, criteria['difficulty'])
    
    return results

def display_search_results(results, search_description=""):
    """Display Search Results In A Formatted Way."""
    if not results:
        print(f"\n🔍 No recipes found {search_description}")
        return []
    
    print(f"\n🔍 Found {len(results)} recipes {search_description}:")
    print("-" * 50)
    
    for i, recipe in enumerate(results, 1):
        # Get Additional Info If Available
        info_parts = []
        
        if recipe.get('cooking_time'):
            info_parts.append(f"⏱️ {recipe['cooking_time']}min")
        
        if recipe.get('difficulty'):
            difficulty_icon = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
            icon = difficulty_icon.get(recipe['difficulty'].lower(), "")
            info_parts.append(f"{icon}{recipe['difficulty']}")
        
        tags = recipe.get('tags', [])
        if tags:
            info_parts.append(f"🏷️ {', '.join(tags[:2])}")
        
        info_str = f" ({', '.join(info_parts)})" if info_parts else ""
        
        print(f"{i}. {recipe['name']} ({len(recipe['ingredients'])} ingredients){info_str}")
    
    return results

def search_recipes_menu(recipes):
    """Main Search Menu With Multiple Options."""
    while True:
        print("\n" + "=" * 50)
        print("🔍 SEARCH RECIPES")
        print("=" * 50)
        print("1. Search By Ingredient")
        print("2. Search By Recipe Name")
        print("3. Search By Tag")
        print("4. Search By Cooking Time")
        print("5. Search By Ingredient Count")
        print("6. Search By Difficulty")
        print("7. Advanced Search (Multiple Criteria)")
        print("8. Back to Main Menu")
        
        choice = input("\nChoose search option (1-8): ").strip()
        
        if choice == "1":
            search_term = input("Enter Ingredient To Search For: ").strip()
            if search_term:
                exact_match = input("Exact Match? (y/n): ").strip().lower() == 'y'
                results = search_by_ingredient(recipes, search_term, exact_match)
                display_search_results(results, f"Containing '{search_term}'")
        
        elif choice == "2":
            search_term = input("Enter Recipe Name To Search For: ").strip()
            if search_term:
                results = search_by_name(recipes, search_term)
                display_search_results(results, f"Named '{search_term}'")
        
        elif choice == "3":
            search_term = input("Enter Tag To Search For: ").strip()
            if search_term:
                results = search_by_tag(recipes, search_term)
                display_search_results(results, f"Tagged '{search_term}'")
        
        elif choice == "4":
            print("\nSearch By Cooking Time:")
            max_time = input("Maximum Cooking Time In Minutes (0 For no Limit): ").strip()
            if max_time and max_time.isdigit():
                max_time = int(max_time) if int(max_time) > 0 else None
                results = search_by_cooking_time(recipes, max_time=max_time)
                time_desc = f"Under {max_time} Minutes" if max_time else "With Cooking Time"
                display_search_results(results, time_desc)
        
        elif choice == "5":
            print("\nSearch By Ingredient Count:")
            max_count = input("Maximum Number Of Ingredients (0 For No Limit): ").strip()
            if max_count and max_count.isdigit():
                max_count = int(max_count) if int(max_count) > 0 else None
                results = search_by_ingredient_count(recipes, max_count=max_count)
                count_desc = f"with {max_count} or fewer ingredients" if max_count else "by ingredient count"
                display_search_results(results, count_desc)
        
        elif choice == "6":
            print("\nSearch By Difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            diff_choice = input("Choose Difficulty (1-3): ").strip()
            difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
            if diff_choice in difficulty_map:
                results = search_by_difficulty(recipes, difficulty_map[diff_choice])
                display_search_results(results, f"With {difficulty_map[diff_choice]} difficulty")
        
        elif choice == "7":
            results = advanced_search(recipes)
            display_search_results(results, "Matching All Criteria")
        
        elif choice == "8":
            break
        
        else:
            print("❌ Invalid Choice. Please Enter 1-8.")
        
        # Option To View A Recipe From Results
        if results:
            view_choice = input("\nEnter Recipe Number To View, Or 's' To Search Again, Or 'Enter' To Continue: ").strip()
            if view_choice.isdigit():
                idx = int(view_choice) - 1
                if 0 <= idx < len(results):
                    display_recipe(results[idx])
            elif view_choice.lower() == 's':
                continue
            elif not view_choice:
                break

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
            print(f"✅ Added {quantity} {unit} Of {ing_name}")
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
    
     # Collect additional information
    print("\n --- Additional Information (Optional) ---")
    
    # Cooking time
    cooking_time = input("Estimated cooking time in minutes (press Enter to skip): ").strip()
    if cooking_time and cooking_time.isdigit():
        cooking_time = int(cooking_time)
    else:
        cooking_time = None
    
    # Difficulty level
    print("\nDifficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    diff_choice = input("Choose (1-3, or Enter to skip): ").strip()
    difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
    difficulty = difficulty_map.get(diff_choice)
    
    # Tags
    tags = []
    print("\nAdd Tags (Comma-Separated, Or 'Enter' To skip): ")
    tags_input = input("Tags: ").strip()
    if tags_input:
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    
    # Build The Complete Recipe Dictionary
    recipe = {
        "name": name,
        "ingredients": ingredients,
        "instructions": instructions,
        "tags": tags
    }
    
    # Add optional fields if provided
    if cooking_time:
        recipe['cooking_time'] = cooking_time
    if difficulty:
        recipe['difficulty'] = difficulty
    
    return recipe  

def display_recipe(recipe):
    """Display A Single Recipe In A Readable Format."""
    print(f"\n 📖 {recipe['name']}")
    print("=" * 50)
    
    # Display metadata if available
    metadata = []
    if recipe.get('cooking_time'):
        metadata.append(f"⏱️ Cooking Time: {recipe['cooking_time']} minutes")
    if recipe.get('difficulty'):
        metadata.append(f"📊 Difficulty: {recipe['difficulty']}")
    
    if metadata:
        print(" | ".join(metadata))
        print("-" * 50)
    
    print("📝 Ingredients:")
    for ing in recipe['ingredients']:
        print(f"  • {ing['quantity']} {ing['unit']} {ing['name']}")
    
    print("\n👨‍🍳 Instructions:")
    for i, step in enumerate(recipe['instructions'], 1):
        print(f"  {i}. {step}")
    
    if recipe.get('tags'):
        print(f"\n🏷️ Tags: {', '.join(recipe['tags'])}")
        
def main():
    """Main program loop"""
    recipes = load_recipes()
    print(f"📚 Recipe Manager - {len(recipes)} recipes loaded")
    
    while True:
        print("\n" + "=" * 50)
        print("🍽️  RECIPE MANAGER")
        print("=" * 50)
        print("1. View All Recipes")
        print("2. Add New Recipe")
        print("3. Search Recipes")
        print("4. Exit")
        
        choice = input("\nYour Choice (1-4): ")
        
        if choice == "1":
            print(f"\n📚 All Recipes ({len(recipes)} total): ")
            for i, recipe in enumerate(recipes, 1):
                # Show additional info if available
                info_parts = []
                if recipe.get('cooking_time'):
                    info_parts.append(f"{recipe['cooking_time']}min")
                if recipe.get('difficulty'):
                    info_parts.append(recipe['difficulty'])
                
                info_str = f" [{', '.join(info_parts)}]" if info_parts else ""
                print(f"{i}. {recipe['name']} ({len(recipe['ingredients'])} ingredients){info_str}")
            
            # Option to view a recipe
            view_choice = input("\nEnter recipe number to view, or press Enter to continue: ")
            if view_choice.isdigit():
                idx = int(view_choice) - 1
                if 0 <= idx < len(recipes):
                    display_recipe(recipes[idx])
                
        elif choice == "2":
            new_recipe = create_recipe()
            recipes.append(new_recipe)
            save_recipes(recipes)
            print(f"\n ✅'{new_recipe['name']}' Saved Successfully!")
            
        elif choice == "3":
            search_recipes_menu(recipes)
            
        elif choice == "4":
            save_recipes(recipes)
            print("\n 👋 Recipes Saved. Goodbye!")
            break
            
        else:
            print("❌ Invalid Choice. Please Enter 1-4.")
            
if __name__ == "__main__":
    main()
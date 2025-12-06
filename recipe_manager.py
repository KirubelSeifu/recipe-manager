import json
import os
import re
from typing import List, Dict, Any, Optional

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPE_FILE = os.path.join(SCRIPT_DIR, "recipes.json")

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

def select_recipe(recipes, prompt="Select a recipe:"):
    """Display list of recipes and let user select one."""
    if not recipes:
        print("❌ No recipes available.")
        return None
    
    print(f"\n{prompt}")
    print("-" * 40)
    
    for i, recipe in enumerate(recipes, 1):
        # Show additional info if available
        info_parts = []
        if recipe.get('cooking_time'):
            info_parts.append(f"{recipe['cooking_time']}min")
        if recipe.get('difficulty'):
            info_parts.append(recipe['difficulty'])
        
        info_str = f" [{', '.join(info_parts)}]" if info_parts else ""
        print(f"{i}. {recipe['name']} ({len(recipe['ingredients'])} ingredients){info_str}")
    
    try:
        choice = input("\nEnter recipe number (or 0 to cancel): ").strip()
        if choice == '0':
            return None
        
        idx = int(choice) - 1
        if 0 <= idx < len(recipes):
            return recipes[idx], idx
        else:
            print("❌ Invalid selection.")
            return None
    except ValueError:
        print("❌ Please enter a valid number.")
        return None

def edit_recipe_name(recipe):
    """Edit the name of a recipe."""
    current_name = recipe['name']
    print(f"\nCurrent name: {current_name}")
    new_name = input("New name (press Enter to keep current): ").strip()
    
    if new_name:
        recipe['name'] = new_name
        print(f"✅ Name changed to: {new_name}")
        return True
    return False

def edit_recipe_ingredients(recipe):
    """Edit the ingredients of a recipe."""
    print("\n📝 Current Ingredients:")
    for i, ing in enumerate(recipe['ingredients'], 1):
        print(f"  {i}. {ing['quantity']} {ing['unit']} {ing['name']}")
    
    print("\nOptions:")
    print("1. Add new ingredient")
    print("2. Edit existing ingredient")
    print("3. Remove ingredient")
    print("4. Clear all ingredients")
    print("5. Keep current ingredients")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice == "1":
        # Add new ingredient
        print("\n--- Add New Ingredient ---")
        while True:
            ing_name = input("Ingredient Name (leave empty to finish): ").strip()
            if not ing_name:
                break
            
            try:
                quantity = float(input(f"Quantity of {ing_name}: "))
                unit = input(f"Unit (cup, tbsp, piece, etc.): ").strip()
                
                recipe['ingredients'].append({
                    "name": ing_name.lower(),
                    "quantity": quantity,
                    "unit": unit
                })
                print(f"✅ Added {quantity} {unit} of {ing_name}")
            except ValueError:
                print("❌ Quantity must be a number.")
        
        return True
    
    elif choice == "2":
        # Edit existing ingredient
        if not recipe['ingredients']:
            print("❌ No ingredients to edit.")
            return False
        
        try:
            ing_num = int(input(f"Enter ingredient number to edit (1-{len(recipe['ingredients'])}): "))
            if 1 <= ing_num <= len(recipe['ingredients']):
                ingredient = recipe['ingredients'][ing_num - 1]
                print(f"\nEditing: {ingredient['quantity']} {ingredient['unit']} {ingredient['name']}")
                
                # Edit name
                new_name = input(f"New name ({ingredient['name']}): ").strip()
                if new_name:
                    ingredient['name'] = new_name.lower()
                
                # Edit quantity
                new_qty = input(f"New quantity ({ingredient['quantity']}): ").strip()
                if new_qty:
                    try:
                        ingredient['quantity'] = float(new_qty)
                    except ValueError:
                        print("❌ Quantity must be a number. Keeping current value.")
                
                # Edit unit
                new_unit = input(f"New unit ({ingredient['unit']}): ").strip()
                if new_unit:
                    ingredient['unit'] = new_unit
                
                print("✅ Ingredient updated.")
                return True
            else:
                print("❌ Invalid ingredient number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    elif choice == "3":
        # Remove ingredient
        if not recipe['ingredients']:
            print("❌ No ingredients to remove.")
            return False
        
        try:
            ing_num = int(input(f"Enter ingredient number to remove (1-{len(recipe['ingredients'])}): "))
            if 1 <= ing_num <= len(recipe['ingredients']):
                removed = recipe['ingredients'].pop(ing_num - 1)
                print(f"✅ Removed: {removed['quantity']} {removed['unit']} {removed['name']}")
                return True
            else:
                print("❌ Invalid ingredient number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    elif choice == "4":
        # Clear all ingredients
        confirm = input("⚠️  Are you sure you want to clear ALL ingredients? (y/n): ").strip().lower()
        if confirm == 'y':
            recipe['ingredients'] = []
            print("✅ All ingredients cleared.")
            return True
    
    return False

def edit_recipe_instructions(recipe):
    """Edit the instructions of a recipe."""
    print("\n👨‍🍳 Current Instructions:")
    for i, step in enumerate(recipe['instructions'], 1):
        print(f"  {i}. {step}")
    
    print("\nOptions:")
    print("1. Add new step")
    print("2. Edit existing step")
    print("3. Remove step")
    print("4. Clear all instructions")
    print("5. Keep current instructions")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice == "1":
        # Add new step
        print("\n--- Add New Steps (leave empty to finish) ---")
        while True:
            step = input(f"Step {len(recipe['instructions']) + 1}: ").strip()
            if not step:
                break
            recipe['instructions'].append(step)
            print(f"✅ Step added.")
        return True
    
    elif choice == "2":
        # Edit existing step
        if not recipe['instructions']:
            print("❌ No instructions to edit.")
            return False
        
        try:
            step_num = int(input(f"Enter step number to edit (1-{len(recipe['instructions'])}): "))
            if 1 <= step_num <= len(recipe['instructions']):
                new_step = input(f"New text for step {step_num}: ").strip()
                if new_step:
                    recipe['instructions'][step_num - 1] = new_step
                    print("✅ Step updated.")
                    return True
            else:
                print("❌ Invalid step number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    elif choice == "3":
        # Remove step
        if not recipe['instructions']:
            print("❌ No steps to remove.")
            return False
        
        try:
            step_num = int(input(f"Enter step number to remove (1-{len(recipe['instructions'])}): "))
            if 1 <= step_num <= len(recipe['instructions']):
                removed = recipe['instructions'].pop(step_num - 1)
                print(f"✅ Removed step {step_num}: {removed}")
                return True
            else:
                print("❌ Invalid step number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    elif choice == "4":
        # Clear all instructions
        confirm = input("⚠️  Are you sure you want to clear ALL instructions? (y/n): ").strip().lower()
        if confirm == 'y':
            recipe['instructions'] = []
            print("✅ All instructions cleared.")
            return True
    
    return False

def edit_recipe_metadata(recipe):
    """Edit recipe metadata (tags, cooking time, difficulty)."""
    print("\n📊 Current Metadata:")
    
    # Display current values
    print(f"  Tags: {', '.join(recipe.get('tags', [])) or 'None'}")
    print(f"  Cooking Time: {recipe.get('cooking_time', 'Not set')} minutes")
    print(f"  Difficulty: {recipe.get('difficulty', 'Not set')}")
    
    print("\nWhat would you like to edit?")
    print("1. Tags")
    print("2. Cooking Time")
    print("3. Difficulty")
    print("4. Keep current metadata")
    
    choice = input("\nChoose option (1-4): ").strip()
    
    if choice == "1":
        # Edit tags
        current_tags = recipe.get('tags', [])
        print(f"\nCurrent tags: {', '.join(current_tags) if current_tags else 'None'}")
        
        print("\nOptions:")
        print("1. Replace all tags")
        print("2. Add tags")
        print("3. Remove tags")
        
        tag_choice = input("Choose option (1-3): ").strip()
        
        if tag_choice == "1":
            new_tags = input("Enter new tags (comma-separated): ").strip()
            if new_tags:
                recipe['tags'] = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
                print("✅ Tags updated.")
            else:
                recipe['tags'] = []
                print("✅ Tags cleared.")
        
        elif tag_choice == "2":
            tags_to_add = input("Enter tags to add (comma-separated): ").strip()
            if tags_to_add:
                new_tags = [tag.strip() for tag in tags_to_add.split(',') if tag.strip()]
                # Ensure we don't add duplicates
                current_tags = recipe.get('tags', [])
                for tag in new_tags:
                    if tag not in current_tags:
                        current_tags.append(tag)
                recipe['tags'] = current_tags
                print(f"✅ Added {len(new_tags)} tag(s).")
        
        elif tag_choice == "3":
            if not recipe.get('tags'):
                print("❌ No tags to remove.")
            else:
                print(f"Current tags: {', '.join(recipe['tags'])}")
                tags_to_remove = input("Enter tags to remove (comma-separated): ").strip()
                if tags_to_remove:
                    remove_list = [tag.strip() for tag in tags_to_remove.split(',') if tag.strip()]
                    recipe['tags'] = [tag for tag in recipe['tags'] if tag not in remove_list]
                    print(f"✅ Removed {len(remove_list)} tag(s).")
        
        return True
    
    elif choice == "2":
        # Edit cooking time
        current_time = recipe.get('cooking_time')
        new_time = input(f"New cooking time in minutes ({current_time}): ").strip()
        if new_time:
            if new_time.isdigit():
                recipe['cooking_time'] = int(new_time)
                print(f"✅ Cooking time set to {new_time} minutes.")
            else:
                print("❌ Cooking time must be a number.")
        elif new_time == "" and current_time is not None:
            # User wants to clear cooking time
            recipe.pop('cooking_time', None)
            print("✅ Cooking time cleared.")
        
        return True
    
    elif choice == "3":
        # Edit difficulty
        current_diff = recipe.get('difficulty')
        print(f"\nCurrent difficulty: {current_diff or 'Not set'}")
        print("\n1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Clear difficulty")
        
        diff_choice = input("Choose difficulty (1-4): ").strip()
        difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
        
        if diff_choice in difficulty_map:
            recipe['difficulty'] = difficulty_map[diff_choice]
            print(f"✅ Difficulty set to {difficulty_map[diff_choice]}.")
        elif diff_choice == "4":
            recipe.pop('difficulty', None)
            print("✅ Difficulty cleared.")
        
        return True
    
    return False

def edit_recipe_menu(recipes):
    """Main menu for editing a recipe."""
    print("\n" + "=" * 50)
    print("✏️  EDIT RECIPE")
    print("=" * 50)
    
    result = select_recipe(recipes, "Select a recipe to edit:")
    if not result:
        return
    
    recipe, idx = result
    
    # Display the recipe first
    display_recipe(recipe)
    
    changed = False
    
    while True:
        print("\n" + "-" * 40)
        print("What would you like to edit?")
        print("1. Name")
        print("2. Ingredients")
        print("3. Instructions")
        print("4. Metadata (Tags, Cooking Time, Difficulty)")
        print("5. View current recipe")
        print("6. Save changes and exit")
        print("7. Cancel without saving")
        
        choice = input("\nChoose option (1-7): ").strip()
        
        if choice == "1":
            if edit_recipe_name(recipe):
                changed = True
        
        elif choice == "2":
            if edit_recipe_ingredients(recipe):
                changed = True
        
        elif choice == "3":
            if edit_recipe_instructions(recipe):
                changed = True
        
        elif choice == "4":
            if edit_recipe_metadata(recipe):
                changed = True
        
        elif choice == "5":
            display_recipe(recipe)
        
        elif choice == "6":
            if changed:
                save_recipes(recipes)
                print(f"\n✅ '{recipe['name']}' updated successfully!")
            else:
                print("\nℹ️  No changes were made.")
            break
        
        elif choice == "7":
            confirm = input("⚠️  Discard all changes? (y/n): ").strip().lower()
            if confirm == 'y':
                # Reload recipes to discard changes
                recipes = load_recipes()
                print("❌ Edit cancelled.")
                break
        else:
            print("❌ Invalid option. Please choose 1-7.")

def delete_recipe_menu(recipes):
    """Delete a recipe with confirmation."""
    print("\n" + "=" * 50)
    print("🗑️  DELETE RECIPE")
    print("=" * 50)
    
    result = select_recipe(recipes, "Select a recipe to delete:")
    if not result:
        return
    
    recipe, idx = result
    
    # Show recipe details before deletion
    print("\n" + "=" * 50)
    print("⚠️  RECIPE TO DELETE:")
    print("=" * 50)
    display_recipe(recipe)
    
    # Double confirmation
    confirm1 = input(f"\n❌ Are you SURE you want to delete '{recipe['name']}'? (y/n): ").strip().lower()
    if confirm1 != 'y':
        print("❌ Deletion cancelled.")
        return
    
    confirm2 = input("⚠️  This action cannot be undone. Type 'DELETE' to confirm: ").strip()
    if confirm2 != 'DELETE':
        print("❌ Deletion cancelled.")
        return
    
    # Delete the recipe
    deleted_recipe = recipes.pop(idx)
    save_recipes(recipes)
    
    print(f"\n✅ '{deleted_recipe['name']}' has been permanently deleted.")
    print(f"📊 Remaining recipes: {len(recipes)}")

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
    """Search recipes by name (supports partial matching)."""
    name_query = name_query.lower()
    return [recipe for recipe in recipes 
            if name_query in recipe['name'].lower()]

def search_by_tag(recipes, tag_query):
    """Search recipes by tags."""
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

def search_by_ingredient_count(recipes, max_count=None, min_count=None):
    """Search recipes by number of ingredients."""
    found_recipes = []
    
    for recipe in recipes:
        ingredient_count = len(recipe['ingredients'])
        match = True
        
        if max_count is not None and ingredient_count > max_count:
            match = False
        if min_count is not None and ingredient_count < min_count:
            match = False
            
        if match:
            found_recipes.append(recipe)
            
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
    """Perform advanced search with multiple criteria."""
    print("\n" + "=" * 50)
    print("🔍 ADVANCED SEARCH")
    print("=" * 50)
    
    criteria = {}
    
    name_query = input("Recipe name contains (leave empty to skip): ").strip()
    if name_query:
        criteria['name'] = name_query
    
    ingredient_query = input("Ingredient contains (leave empty to skip): ").strip()
    if ingredient_query:
        exact_match = input("Exact match? (y/n): ").strip().lower() == 'y'
        criteria['ingredient'] = ingredient_query
        criteria['exact_match'] = exact_match
    
    tag_query = input("Tag contains (leave empty to skip): ").strip()
    if tag_query:
        criteria['tag'] = tag_query
    
    time_query = input("Maximum cooking time in minutes (0 to skip): ").strip()
    if time_query and time_query.isdigit():
        criteria['max_time'] = int(time_query)
    
    max_ingredients = input("Maximum number of ingredients (0 to skip): ").strip()
    if max_ingredients and max_ingredients.isdigit():
        criteria['max_ingredients'] = int(max_ingredients)
    
    difficulty_query = input("Difficulty (Easy/Medium/Hard, leave empty to skip): ").strip()
    if difficulty_query:
        criteria['difficulty'] = difficulty_query
    
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
    """Display search results in a formatted way."""
    if not results:
        print(f"\n🔍 No recipes found {search_description}")
        return []
    
    print(f"\n🔍 Found {len(results)} recipes {search_description}:")
    print("-" * 50)
    
    for i, recipe in enumerate(results, 1):
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
    """Main search menu with multiple options."""
    while True:
        print("\n" + "=" * 50)
        print("🔍 SEARCH RECIPES")
        print("=" * 50)
        print("1. Search by Ingredient")
        print("2. Search by Recipe Name")
        print("3. Search by Tag")
        print("4. Search by Cooking Time")
        print("5. Search by Ingredient Count")
        print("6. Search by Difficulty")
        print("7. Advanced Search (Multiple Criteria)")
        print("8. Back to Main Menu")
        
        choice = input("\nChoose search option (1-8): ").strip()
        
        if choice == "1":
            search_term = input("Enter ingredient to search for: ").strip()
            if search_term:
                exact_match = input("Exact match? (y/n): ").strip().lower() == 'y'
                results = search_by_ingredient(recipes, search_term, exact_match)
                results = display_search_results(results, f"containing '{search_term}'")
        
        elif choice == "2":
            search_term = input("Enter recipe name to search for: ").strip()
            if search_term:
                results = search_by_name(recipes, search_term)
                results = display_search_results(results, f"named '{search_term}'")
        
        elif choice == "3":
            search_term = input("Enter tag to search for: ").strip()
            if search_term:
                results = search_by_tag(recipes, search_term)
                results = display_search_results(results, f"tagged '{search_term}'")
        
        elif choice == "4":
            print("\nSearch by cooking time:")
            max_time = input("Maximum cooking time in minutes (0 for no limit): ").strip()
            if max_time and max_time.isdigit():
                max_time = int(max_time) if int(max_time) > 0 else None
                results = search_by_cooking_time(recipes, max_time=max_time)
                time_desc = f"under {max_time} minutes" if max_time else "with cooking time"
                results = display_search_results(results, time_desc)
        
        elif choice == "5":
            print("\nSearch by ingredient count:")
            max_count = input("Maximum number of ingredients (0 for no limit): ").strip()
            if max_count and max_count.isdigit():
                max_count = int(max_count) if int(max_count) > 0 else None
                results = search_by_ingredient_count(recipes, max_count=max_count)
                count_desc = f"with {max_count} or fewer ingredients" if max_count else "by ingredient count"
                results = display_search_results(results, count_desc)
        
        elif choice == "6":
            print("\nSearch by difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            diff_choice = input("Choose difficulty (1-3): ").strip()
            difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
            if diff_choice in difficulty_map:
                results = search_by_difficulty(recipes, difficulty_map[diff_choice])
                results = display_search_results(results, f"with {difficulty_map[diff_choice]} difficulty")
        
        elif choice == "7":
            results = advanced_search(recipes)
            results = display_search_results(results, "matching all criteria")
        
        elif choice == "8":
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-8.")
        
        # Option to view, edit, or delete a recipe from results
        if results:
            print("\nOptions for selected recipe:")
            print("  [number] - View recipe")
            print("  e[number] - Edit recipe")
            print("  d[number] - Delete recipe")
            print("  s - Search again")
            print("  Enter - Back to search menu")
            
            action = input("\nEnter your choice: ").strip().lower()
            
            if action.isdigit():
                idx = int(action) - 1
                if 0 <= idx < len(results):
                    display_recipe(results[idx])
            elif action.startswith('e') and action[1:].isdigit():
                idx = int(action[1:]) - 1
                if 0 <= idx < len(results):
                    # Find the actual index in the main recipes list
                    recipe_name = results[idx]['name']
                    for i, recipe in enumerate(recipes):
                        if recipe['name'] == recipe_name:
                            edit_recipe_menu(recipes)
                            break
            elif action.startswith('d') and action[1:].isdigit():
                idx = int(action[1:]) - 1
                if 0 <= idx < len(results):
                    # Find the actual index in the main recipes list
                    recipe_name = results[idx]['name']
                    for i, recipe in enumerate(recipes):
                        if recipe['name'] == recipe_name:
                            recipes_copy = recipes.copy()
                            delete_recipe_menu(recipes_copy)
                            break
            elif action == 's':
                continue
            elif not action:
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
    print("\nAdd tags (comma-separated, or Enter to skip): ")
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
        print("4. Edit Recipe")
        print("5. Delete Recipe")
        print("6. Exit")
        
        choice = input("\nYour Choice (1-6): ")
        
        if choice == "1":
            print(f"\n📚 All Recipes ({len(recipes)} total): ")
            for i, recipe in enumerate(recipes, 1):
                info_parts = []
                if recipe.get('cooking_time'):
                    info_parts.append(f"{recipe['cooking_time']}min")
                if recipe.get('difficulty'):
                    info_parts.append(recipe['difficulty'])
                
                info_str = f" [{', '.join(info_parts)}]" if info_parts else ""
                print(f"{i}. {recipe['name']} ({len(recipe['ingredients'])} ingredients){info_str}")
            
            # Enhanced options when viewing recipes
            print("\nOptions:")
            print("  [number] - View recipe")
            print("  e[number] - Edit recipe")
            print("  d[number] - Delete recipe")
            print("  Enter - Back to main menu")
            
            action = input("\nEnter your choice: ").strip().lower()
            
            if action.isdigit():
                idx = int(action) - 1
                if 0 <= idx < len(recipes):
                    display_recipe(recipes[idx])
            elif action.startswith('e') and action[1:].isdigit():
                idx = int(action[1:]) - 1
                if 0 <= idx < len(recipes):
                    edit_recipe_menu(recipes)
            elif action.startswith('d') and action[1:].isdigit():
                idx = int(action[1:]) - 1
                if 0 <= idx < len(recipes):
                    delete_recipe_menu(recipes)
                
        elif choice == "2":
            new_recipe = create_recipe()
            recipes.append(new_recipe)
            save_recipes(recipes)
            print(f"\n ✅'{new_recipe['name']}' Saved Successfully!")
            
        elif choice == "3":
            search_recipes_menu(recipes)
            
        elif choice == "4":
            edit_recipe_menu(recipes)
            
        elif choice == "5":
            delete_recipe_menu(recipes)
            
        elif choice == "6":
            save_recipes(recipes)
            print("\n 👋 Recipes Saved. Goodbye!")
            break
            
        else:
            print("❌ Invalid Choice. Please Enter 1-6.")
            
if __name__ == "__main__":
    main()
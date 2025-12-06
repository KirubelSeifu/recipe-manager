# Recipe Manager CLI (Enhanced)

A comprehensive command-line recipe manager with advanced search capabilities. Built with Python for efficient recipe management, organization, and intelligent searching.

## ✨ Features

### 🔍 **Advanced Search System**
- **Multiple Search Criteria**: Search by ingredient, name, tags, cooking time, difficulty, and ingredient count
- **Advanced Search**: Combine multiple filters for precise results
- **Flexible Matching**: Exact or partial matching options
- **Real-time Filtering**: Interactive search with immediate results

### 📝 **Enhanced Recipe Structure**
- **Structured Ingredients**: Name, quantity, unit for precise measurements
- **Optional Metadata**: Cooking time, difficulty level (Easy/Medium/Hard)
- **Tag System**: Add descriptive tags for better organization
- **Step-by-step Instructions**: Detailed cooking directions

### 💾 **Data Management**
- **JSON Storage**: Human-readable data persistence
- **Automatic Saving**: Changes saved automatically
- **Error Handling**: Graceful recovery from file issues
- **Clean Data Structure**: Consistent, well-organized recipe format

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/KirubelSeifu/recipe-manager.git
cd recipe-manager

# Run the recipe manager
python recipe_manager.py

📋 Usage
Main Menu Options:
1. View All Recipes - Browse your complete collection
2. Add New Recipe - Interactive recipe creation wizard
3. Search Recipes - Advanced search with multiple criteria

4. Exit - Save and quit

Search Features:
-By Ingredient: Find recipes containing specific ingredients

-By Name: Search recipe titles

-By Tag: Filter by descriptive tags

-By Cooking Time: Find quick meals or elaborate dishes

-By Difficulty: Easy, Medium, or Hard recipes

-By Ingredient Count: Simple or complex recipes

-Advanced Search: Combine all criteria for precise filtering

🎯 Example Workflow
# 1. Add a recipe
> Add New Recipe
Recipe: Chicken Alfredo
Ingredients: chicken, pasta, cream, parmesan
Cooking Time: 30 minutes
Difficulty: Medium
Tags: italian, dinner, pasta

# 2. Search for recipes
> Search Recipes
> Advanced Search
- Name contains: "chicken"
- Max cooking time: 30
- Difficulty: Medium

# 3. View results
Found 3 recipes matching all criteria

📁 Project Structure
recipe-manager/
├── recipe_manager.py    # Main application (enhanced version)
├── recipes.json         # Recipe database (auto-generated)
├── README.md           # This documentation
├── requirements.txt    # Python requirements
└── .gitignore         # Ignore unnecessary files

🔧 Technical Details
- Python Version: 3.6+

- Dependencies: None (pure Python)

- Storage: JSON format for easy reading/modification

- Search Algorithm: Linear scan with early termination

🌟 Key Enhancements
1. Intelligent Search: Multi-criteria filtering system

2. Rich Metadata: Cooking time, difficulty, tags

3. User-Friendly Interface: Visual indicators and clear menus

4.Interactive Results: View recipes directly from search results

Data Integrity: Consistent structure and validation

📈 Future Roadmap
Recipe editing and deletion

Batch operations (add tags to multiple recipes)

Recipe scaling (adjust portions)

Export to PDF/CSV

Nutritional information tracking

Meal planning features

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Tags: python recipe-manager cli search cooking productivity data-management

Created by: Kirubel Seifu
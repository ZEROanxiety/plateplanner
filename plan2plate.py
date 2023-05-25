import pandas as pd
import numpy as np
import streamlit as st

file = st.file_uploader(label="Upload your CSV file", type="csv")

df = pd.read_csv(file)

try:
  df = pd.read_csv(file)
except:
  st.error("Please upload a valid CSV file")

# Check if the dataframe has the required columns
required_columns = ["Name", "Category", "Applicable Meals", "Price", "Health Rating (1-10)"]
if not all(col in df.columns for col in required_columns):
  st.error("The CSV file is missing some required columns")

# Check if the dataframe has the required values for the Category column
required_values = ["Fast Food", "Homemade", "Quick", "LEFTOVERS"]
if not all(val in df["Category"].unique() for val in required_values):
  st.error("The CSV file is missing some required values for the Category column")

st.sidebar.title("Meal Plan Settings")

# Create a slider widget to get the number of days
days = st.sidebar.slider(label="Number of days", min_value=1, max_value=14, value=7)

# Create a number input widget to get the budget
budget = st.sidebar.number_input(label="Budget ($)", min_value=0.0, value=100.0)

# Create a number input widget to get the calorie limit
calorie_limit = st.sidebar.number_input(label="Calorie limit (kcal)", min_value=0, value=2000)

def generate_meal_plan(df, days, budget, calorie_limit):
  # Write the code for generating the meal plan here
  return meal_plan

def generate_meal_plan(df, days, budget, calorie_limit):
  # Create an empty list to store the meal plan data
  meal_plan = []

  # Loop through the number of days
  for day in range(days):
    # Create a sublist for each day
    day_list = []

    # Loop through the number of meals (3)
    for meal in range(3):
      # Randomly select a meal option from the dataframe that matches the applicable meal slot
      if meal == 0:
        # Breakfast slot
        meal_option = df[df["Applicable Meals"] == "Breakfast"].sample()
      elif meal == 1:
        # Lunch slot
        # Check if the previous dinner was homemade and fill with leftovers if so
        if day > 0 and meal_plan[day-1][2][0] == "Homemade":
          meal_option = df[df["Name"] == "LEFTOVERS"]
        else:
          # Otherwise select a random lunch option
          meal_option = df[df["Applicable Meals"].str.contains("Lunch")].sample()
      else:
        # Dinner slot
        meal_option = df[df["Applicable Meals"] == "Dinner"].sample()

      # Check if the selected meal option satisfies the constraints for the category, cost and calories
      # If not, select another meal option until it does
      while True:
        # Get the category, cost and calories of the selected meal option
        category = meal_option["Category"].item()
        cost = meal_option["Price"].item()
        calories = int(meal_option["Health Rating (1-10)"].item()) * 100

        # Check if the category is evenly blended with previous meals
        # Count the number of occurrences of each category in the previous meals
        category_count = {"Fast Food": 0, "Homemade": 0, "Quick": 0}
        for previous_day in meal_plan:
          for previous_meal in previous_day:
            previous_category = previous_meal[0]
            category_count[previous_category] += 1
        
        # Calculate the expected number of occurrences of each category based on an even blend
        expected_count = (day * 3 + meal + 1) / 3

        # If the selected category has more occurrences than expected, select another meal option
        if category_count[category] > expected_count:
          if meal == 0:
            # Breakfast slot
            meal_option = df[df["Applicable Meals"] == "Breakfast"].sample()
          elif meal == 1:
            # Lunch slot
            # Check if the previous dinner was homemade and fill with leftovers if so
            if day > 0 and meal_plan[day-1][2][0] == "Homemade":
              meal_option = df[df["Name"] == "LEFTOVERS"]
            else:
              # Otherwise select a random lunch option
              meal_option = df[df["Applicable Meals"].str.contains("Lunch")].sample()
          else:
            # Dinner slot
            meal_option = df[df["Applicable Meals"] == "Dinner"].sample()
          
          # Update the category, cost and calories of the selected meal option
          category = meal_option["Category"].item()
          cost = meal_option["Price"].item()
          calories = int(meal_option["Health Rating (1-10)"].item()) * 100
        
        else:
          # The selected category is evenly blended with previous meals
          break
      
      # Check if there are two consecutive fast food meals and select another meal option if so
      if category == "Fast Food":
        # Check if the previous meal was also fast food
        if day_list and day_list[-1][0] == "Fast Food":
          # Select another non-fast food meal option that matches the applicable meal slot
          if meal == 0:
            # Breakfast slot
            meal_option = df[(df["Applicable Meals"] == "Breakfast") & (df["Category"] != "Fast Food")].sample()
          elif meal == 1:
            # Lunch slot
            # Check if the previous dinner was homemade and fill with leftovers if so
            if day > 0 and meal_plan[day-1][2][0] == "Homemade":
              meal_option = df[df["Name"] == "LEFTOVERS"]
            else:
              # Otherwise select a random non-fast food lunch option
              meal_option = df[(df["Applicable Meals"].str.contains("Lunch")) & (df["Category"] != "Fast Food")].sample()
          else:
            # Dinner slot
            meal_option = df[(df["Applicable Meals"] == "Dinner") & (df["Category"] != "Fast Food")].sample()

          # Update the category, cost and calories of the selected meal option
          category = meal_option["Category"].item()
          cost = meal_option["Price"].item()
          calories = int(meal_option["Health Rating (1-10)"].item()) * 100
      
      # Check if the first lunch of the week is leftovers and select another non-leftover lunch option if so
      if day == 0 and meal == 1 and category == "LEFTOVERS":
        # Select a random non-leftover lunch option
        meal_option = df[(df["Applicable Meals"].str.contains("Lunch")) & (df["Name"] != "LEFTOVERS")].sample()

        # Update the category, cost and calories of the selected meal option
        category = meal_option["Category"].item()
        cost = meal_option["Price"].item()
        calories = int(meal_option["Health Rating (1-10)").item()) * 100

      # Add the selected meal option to the sublist along with its cost and calories
      day_list.append([category, cost, calories])

    # Add the sublist to the main list 
    meal_plan.append(day_list)

    # Calculate the total cost and calories for each day 
    total_cost = sum([meal[1] for meal in day_list])
    total_calories = sum([meal[2] for meal in day_list])

    # Add the total cost and calories to the sublist 
    day_list.append([total_cost, total_calories])

  # Calculate the total cost and calories for each week 
  total_week_cost = sum([day[-1][0] for day in meal_plan])
  total_week_calories = sum([day[-1][1] for day in meal_plan])

    # Add the total cost and calories for each week to the main list
  meal_plan.append([total_week_cost, total_week_calories])

  # Return the meal plan data
  return meal_plan

# Convert the meal plan data into a dataframe
df = pd.DataFrame(meal_plan)

# Add column names and index names to the dataframe
df.columns = ["Category", "Cost ($)", "Calories (kcal)"]
df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Total"]

# Display the dataframe as a table using streamlit's data_frame widget
st.data_frame(df)

# Display the cost and calories summary using streamlit's markdown widget
st.markdown(f"The total cost for the week is ${meal_plan[-1][0]}")
st.markdown(f"The total calories for the week are {meal_plan[-1][1]} kcal")


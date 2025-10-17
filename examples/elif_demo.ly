def main() {
    print("=== Elif Conditional Syntax Demo ===")
    
    # Example 1: Simple if/elif/else chain
    print("\n1. Simple if/elif/else chain:")
    int score = 85
    
    if score >= 90:
        print("  Grade: A - Excellent!")
    elif score >= 80:
        print("  Grade: B - Good!")
    elif score >= 70:
        print("  Grade: C - Average")
    elif score >= 60:
        print("  Grade: D - Below average")
    else:
        print("  Grade: F - Failing")
    end
    
    # Example 2: String conditions
    print("\n2. String conditions:")
    str day = "Wednesday"
    
    if day == "Monday":
        print("  Start of the work week")
    elif day == "Tuesday":
        print("  Second day of the week")
    elif day == "Wednesday":
        print("  Mid-week hump day")
    elif day == "Thursday":
        print("  Almost Friday")
    elif day == "Friday":
        print("  TGIF - Friday!")
    elif day == "Saturday" or day == "Sunday":
        print("  Weekend!")
    else:
        print("  Invalid day")
    end
    
    # Example 3: Complex conditions with and/or
    print("\n3. Complex conditions:")
    int age = 25
    god is_student = true
    god has_job = false
    
    if age < 18:
        print("  Category: Minor")
    elif age >= 18 and age < 65:
        print("  Category: Adult")
    elif age >= 65:
        print("  Category: Senior")
    end
    
    if is_student and age >= 18:
        print("  Status: Adult student")
    elif is_student and age < 18:
        print("  Status: Minor student")
    elif not is_student and has_job:
        print("  Status: Working adult")
    elif not is_student and not has_job:
        print("  Status: Unemployed adult")
    end
    
    # Example 4: Nested conditionals
    print("\n4. Nested conditionals:")
    int temperature = 75
    str weather = "sunny"
    
    if temperature > 80:
        print("  Hot weather")
        if weather == "sunny":
            print("    Perfect beach weather!")
        elif weather == "cloudy":
            print("    Hot but cloudy")
        else:
            print("    Hot with other weather")
        end
    elif temperature > 60:
        print("  Mild weather")
        if weather == "sunny":
            print("    Pleasant day")
        elif weather == "rainy":
            print("    Light jacket weather")
        else:
            print("    Mild with other weather")
        end
    else:
        print("  Cold weather")
        if weather == "sunny":
            print("    Cold but sunny")
        elif weather == "snowy":
            print("    Winter wonderland")
        else:
            print("    Cold with other weather")
        end
    end
    
    # Example 5: Multiple elif clauses
    print("\n5. Multiple elif clauses:")
    int month = 3
    
    if month == 1:
        print("  January - New Year")
    elif month == 2:
        print("  February - Valentine's Day")
    elif month == 3:
        print("  March - Spring begins")
    elif month == 4:
        print("  April - April showers")
    elif month == 5:
        print("  May - May flowers")
    elif month == 6:
        print("  June - Summer solstice")
    elif month == 7:
        print("  July - Independence Day")
    elif month == 8:
        print("  August - Dog days of summer")
    elif month == 9:
        print("  September - Back to school")
    elif month == 10:
        print("  October - Halloween")
    elif month == 11:
        print("  November - Thanksgiving")
    elif month == 12:
        print("  December - Christmas")
    else:
        print("  Invalid month")
    end
    
    print("\n=== Elif Demo Complete ===")
}

def main() {
    print("=== Logical Operators and Boolean Literals Demo ===")
    
    # Example 1: Boolean literals
    print("\n1. Boolean literals:")
    god flag1 = true
    god flag2 = false
    print("  flag1 =", flag1)
    print("  flag2 =", flag2)
    
    # Example 2: Simple logical operations
    print("\n2. Simple logical operations:")
    god result1 = true and false
    god result2 = true or false
    god result3 = not true
    god result4 = not false
    
    print("  true and false =", result1)
    print("  true or false =", result2)
    print("  not true =", result3)
    print("  not false =", result4)
    
    # Example 3: Complex expressions with precedence
    print("\n3. Complex expressions with precedence:")
    god result5 = true and true or false
    god result6 = false or true and false
    god result7 = not (true and false)
    god result8 = not true and not false
    
    print("  true and true or false =", result5)
    print("  false or true and false =", result6)
    print("  not (true and false) =", result7)
    print("  not true and not false =", result8)
    
    # Example 4: Mixed expressions with numbers
    print("\n4. Mixed expressions with numbers:")
    int x = 5
    int y = 3
    god result9 = x > 3 and y < 5
    god result10 = x < 10 or y > 5
    god result11 = not (x == 0)
    god result12 = (x > 0) and (x < 10) and (y > 0)
    
    print("  x > 3 and y < 5 =", result9)
    print("  x < 10 or y > 5 =", result10)
    print("  not (x == 0) =", result11)
    print("  (x > 0) and (x < 10) and (y > 0) =", result12)
    
    # Example 5: Short-circuit evaluation demonstration
    print("\n5. Short-circuit evaluation:")
    god result13 = false and print("This should not print")
    print("  false and (print) =", result13)
    
    god result14 = true or print("This should not print")
    print("  true or (print) =", result14)
    
    # Example 6: Nested expressions
    print("\n6. Nested expressions:")
    god a = true
    god b = false
    god c = true
    
    god result15 = (a and b) or (c and not b)
    god result16 = not (a and b) or (not c)
    god result17 = (a or b) and (c or not a)
    god result18 = not ((a and b) or (c and not a))
    
    print("  (a and b) or (c and not b) =", result15)
    print("  not (a and b) or (not c) =", result16)
    print("  (a or b) and (c or not a) =", result17)
    print("  not ((a and b) or (c and not a)) =", result18)
    
    # Example 7: Real-world scenario
    print("\n7. Real-world scenario:")
    int age = 25
    god has_license = true
    god has_insurance = false
    god is_employed = true
    god has_good_credit = true
    
    # Complex eligibility checks
    god can_drive = age >= 18 and has_license
    god needs_insurance = can_drive and not has_insurance
    god is_eligible_for_loan = age >= 18 and is_employed and (has_license or not needs_insurance)
    god is_eligible_for_premium = is_eligible_for_loan and has_good_credit and has_insurance
    
    print("  Age:", age)
    print("  Has license:", has_license)
    print("  Has insurance:", has_insurance)
    print("  Is employed:", is_employed)
    print("  Has good credit:", has_good_credit)
    print("  Can drive:", can_drive)
    print("  Needs insurance:", needs_insurance)
    print("  Eligible for loan:", is_eligible_for_loan)
    print("  Eligible for premium:", is_eligible_for_premium)
    
    # Example 8: Conditional statements with logical operators
    print("\n8. Conditional statements:")
    if age >= 18 and has_license:
        print("  Can drive legally")
    end
    
    if (age >= 21 and is_employed) or has_good_credit:
        print("  Eligible for premium services")
    end
    
    if not has_insurance and can_drive:
        print("  Warning: Driving without insurance")
    end
    
    if age < 18 or not has_license:
        print("  Cannot drive legally")
    end
    
    print("\n=== Logical Operators Demo Complete ===")
}

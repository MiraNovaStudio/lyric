from lyric.parser import parse

# Test the if statement issue
source1 = '''
class Test:
    def test() {
        if self.balance >= amount {
            return True
        }
    }
+++'''

try:
    ast1 = parse(source1)
    print("If statement: Success")
except Exception as e:
    print("If statement error:", e)

# Test the for loop issue  
source2 = '''
class Test:
    def test() {
        for item in self.items {
            print(item)
        }
    }
+++'''

try:
    ast2 = parse(source2)
    print("For loop: Success")
except Exception as e:
    print("For loop error:", e)

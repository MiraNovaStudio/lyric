
def main() {

# string conversions
    print str(123)
    print str(3.14)
    print str(true)

# numeric conversions
    print int("42")
    print int(3.7)

    print flt("3.14")
    print flt(5)

# invalid conversions
    try:
        print int("hello")
    catch Error:
        print "caught error"
    fade
    
    try:
        print flt("abc")
    catch Error:
        print "caught error"
    fade

# concatenation behavior
    print "hello" + " world"

    try:
        print "hello" + 5   # should error
    catch Error:
        print "caught error"
    fade

}

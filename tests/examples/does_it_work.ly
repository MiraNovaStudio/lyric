def main() {
    var count = 0
    god keep_going = true

    given keep_going:
        print("Count:", count)
        count = count + 1
	print("count assignment: ", count)
        if count >= 3:
	    print("count: ", count)
            keep_going = false
	    print("keep_going: ", keep_going)
        end
    done

    print("Final count:", count)
}

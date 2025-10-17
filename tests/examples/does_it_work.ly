def main() {
    var count = 0
    god keep_going = true
    
    given keep_going:
        print("Count:", count)
        count = count + 1
        if count >= 3:
            keep_going = false
        end
    done
    
    print("Final count:", count)
}

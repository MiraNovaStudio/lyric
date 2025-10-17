# Lyric Loop Demonstration
# Shows basic loops, nested loops, and control flow modifiers: break and continue

def main() {
  print("=== Loop Examples in Lyric ===")

  # Simple loop — counts from 0 to 4
  given i in range(5):
    print("Outer loop iteration:", i)
  done

  # Loop with conditional skip
  print("\nLoop with 'continue' to skip even numbers:")
  given n in range(6):
    if n % 2 == 0:
      continue   # Skip even numbers
    end
    print("Odd number:", n)
  done

  # Loop with early break
  print("\nLoop with 'break' to stop when number reaches 3:")
  given x in range(10):
    if x == 3:
      print("Breaking at:", x)
      break
    end
    print("Counting:", x)
  done

  # Nested loop example — prints pairs, skips duplicates
  print("\nNested loop demonstration:")
  given a in range(3):
    given b in range(3):
      if a == b:
        continue   # Skip when both indexes are the same
      end
      print("Pair:", a, b)
    done
  done

  print("\nAll loops complete.")
}

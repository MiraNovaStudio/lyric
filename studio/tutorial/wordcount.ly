class WordCounter
    def init(str text) {
        self.text = text
        self.counts = {}
    }

    def count_words() {
        #rex word_pattern = regex("/\w+/")
        #arr words = word_pattern.findall(self.text.lower())
        arr words = self.text.split()
        str word

        for word in words
            if word in self.counts
                self.counts[word] += 1
            else
                self.counts[word] = 1
            end
        done
    }

    def top_words(int n) {
        arr result = []
        arr all_words = self.counts.keys()
        int i
        str word

        # Simple selection sort for top N
        for i in range(n)
            if all_words.len() == 0
                break
            end

            var best_word = all_words[0]
            int best_count = self.counts[all_words[0]]

            for word in all_words
                if self.counts[word] > best_count
                    best_count = self.counts[word]
                    best_word = word
                end
            done

            result.append([best_word, best_count])
            all_words.remove(best_word)
        done

        return result
    }
+++

def main() {
    var filename = getopts("f:", "file:")
    god verbose  = getopts("v", "verbose")

    if filename == False
        print("Usage: lyric wordcount.ly --file=text.txt [--verbose]")
        exit(1)
    end

    dsk f = disk(filename)
    if not f.exists()
        print("Error: file not found:", filename)
        exit(1)
    end

    str text = f.read()
    f.close()

    if verbose
        print("File size:", f.size(), "bytes")
    end

    obj wc = WordCounter(text)
    wc.count_words()

    print("Unique words:", wc.counts.len())

    print("\nTop 5 words:")
    arr top = wc.top_words(5)
    arr entry

    for entry in top
        print(" ", entry[0], ":", entry[1])
    done
}

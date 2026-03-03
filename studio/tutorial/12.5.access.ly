class User:
    public str name = ""
    private str password = ""

    def User(str n, str p) {
        self.name = n
        self.password = p
    }

    public def check_password(str attempt) {
        return attempt == self.password
    }
+++

def main() {
    obj user = User("Alice", "secret123")

    print("Name:", user.name)                          # works — name is public
    print("Password correct:", user.check_password("secret123"))  # works — method is public
    # print(user.password)                             # would fail — password is private
}

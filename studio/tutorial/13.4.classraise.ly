class Wallet:
    private flt balance = 0.0

    public def deposit(flt amount) {
        if amount <= 0
            raise ValueErrorLyric
        end
        self.balance += amount
        print("Deposited", amount, "— balance is now", self.balance)
    }

    public def withdraw(flt amount) {
        if amount > self.balance
            raise RuntimeErrorLyric
        end
        self.balance -= amount
        print("Withdrew", amount, "— balance is now", self.balance)
    }
+++

def main() {
    obj w = Wallet()
    w.deposit(50.0)

    try:
        w.deposit(-10.0)
    catch:
        print("Deposit rejected: amount must be positive")
    fade

    try:
        w.withdraw(100.0)
    catch:
        print("Withdrawal rejected: not enough funds")
    fade

    w.withdraw(20.0)
}

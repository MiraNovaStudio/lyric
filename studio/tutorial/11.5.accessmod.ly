class BankAccount:
    balance = 0.0

    public def deposit(flt amount) {
        self.balance = self.balance + amount
    }

    public def get_balance() {
        return self.balance
    }

    private def apply_fee() {
        self.balance = self.balance + 5.0
    }
+++

def main() {
    var account = BankAccount()
    account.deposit(100.0)
    print(account.get_balance())   # 100.0
}

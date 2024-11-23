def get_usage_cost():
    cost = get_gas_cost() + get_oil_cost() + get_tire_cost()
    return cost

def get_gas_cost():
    cost = int(input("Cost of gas: "))
    return cost

def get_oil_cost():
    cost = int(input("Cost of oil: "))
    return cost

def get_tire_cost():
    cost = int(input("Cost of tires: "))
    return cost

def get_fixed_cost():
    cost = get_devaluation() + get_insurance()
    return cost

def get_devaluation():
    # Unsure if this was supposed to be depreciation rate or depreciation total
    current_value = int(input("Current market value of car: "))
    original_value = int(input("Price of car at original purchase: "))
    cost = original_value - current_value
    return cost

def get_insurance():
    cost = int(input("Cost of insurance: "))
    return cost

def display_cost(cost):
    print(cost)

def main():
    cost = get_fixed_cost() + get_usage_cost()
    display_cost(cost)

if __name__ == "main":
    main()
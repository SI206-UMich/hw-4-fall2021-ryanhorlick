#HW4.py
#Ryan Horlick
#UM ID -- 6990 0824
#worked with Anders Lundin
import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self, deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet -= amount
        cashier.receive_payment(stall, amount)


    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."

    def extra_credit(self):
        pass


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:

    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings


    def process_order(self, name, quantity):
        if self.has_item(name, quantity):
            self.inventory[name] -= quantity
        else:
            print ("Sorry we do not have enough" + str(self.name) + "to complete your order.")


    def has_item(self, name, quantity):
        if name not in self.inventory.keys():
            return False
        if self.inventory[name] >= quantity:
            return True
        else:
            return False

    def stock_up(self, name, quantity):
        if name in self.inventory:
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity

    def compute_cost(self, quantity):
        total = self.cost * quantity
        return total

    def __str__(self):
        print("Hello, we are " + self.name + ". This is the current menu " + self.inventory.keys() + ".")
        print("We charge $" + self.cost + " per item. We have $" + self.earnings + " in total.")

    # def extra_credit(self):
    #     for name in list.randrange(0, 10):
    #         if name == 10:
    #                 pass
    # unsure, needs more practice / thought

            
class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_customer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_customer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)


	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases


        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertNotEqual(self.s1.has_item("Popsicle", 5), True)
        
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(self.s1.has_item("Burger", 50))

        
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s1.has_item("Burger", 5))


	# Test validate order
    def test_validate_order(self):
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.assertEqual(self.f1.validate_order(self.c1, self.s1, "Burger", 30), None)

		# case 2: test if the stall doesn't have enough food left in stock
        self.assertEqual(self.f1.validate_order(self.c1, self.s1, "Burger", 200), None)

		# case 3: check if the cashier can order item from that stall
        self.assertEqual(self.f1.validate_order(self.c2, self.s3, "Burger", 30), None)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        self.f2.reload_money(50)
        self.assertEqual(self.f2.wallet, 200)


### Write main function
def main():
    #Create different objects
    inventory1 = {'Burger':40, 'French Fries':40, 'Hot Dog':40}
    inventory2 = {'Ham Sandwich':40, 'Bolognese Sandwich':40, 'Yogurt':40, 'Ice Cream':50}
    inventory3 = {'Lollipop': 30}
    customer1 = Customer("Jeremiah", 100)
    customer2 = Customer("Yolanda", 50)
    customer3 = Customer("Julius", 272)
    stall1 = Stall("Chipotle", inventory1, cost = 11)
    stall2 = Stall("Joe's Pizza", inventory2, cost = 7)
    stall3 = Stall("Bopjib", inventory3, cost = 8)
    cashier1 = Cashier("North")
    cashier2 = Cashier("South")

    for c in [cashier1, cashier2]:
            for s in [stall1, stall2]:
                c.add_stall(s)

    


    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall
    customer1.validate_order(cashier1, stall3, "Burger", 9)
    customer2.validate_order(cashier2, stall3, "Ham Sandwich", 5)
    customer3.validate_order(cashier2, stall3, "Yogurt", 4)
    
    #case 2: the cashier has the stall, but not enough ordered food or the ordered food item
    customer1.validate_order(cashier1, stall1, "Yogurt", 41)
    customer2.validate_order(cashier2, stall2, "Burger", 41)
    customer3.validate_order(cashier2, stall2, "Hot Dog", 41)
    
    #case 3: the customer does not have enough money to pay for the order:
    customer1.validate_order(cashier1, stall1, "Burger", 39)
    customer2.validate_order(cashier2, stall2, "Ham Sandwich", 39)
    customer3.validate_order(cashier2, stall2, "Ham Sandwich", 39)
    
    #case 4: the customer successfully places an order
    customer1.validate_order(cashier1, stall1, "French Fries", 1)
    customer2.validate_order(cashier2, stall2, "Bolognese Sandwich", 1)
    customer3.validate_order(cashier2, stall2, "Ice Cream", 1)


if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)

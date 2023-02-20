def calculate (total_amount):
    total_amount = float(total_amount)
    eighteen = total_amount * 0.18
    total_with_eighteen = total_amount + eighteen
    
    twenty = total_amount * 0.2
    total_with_twenty = total_amount + twenty
    
    twenty_two = total_amount * 0.22
    total_with_twenty_two = total_amount + twenty_two
    
    print("18%: " + str(total_with_eighteen) + "\n20%: " + str(total_with_twenty) + "\n22%: " + str(total_with_twenty_two))

total_amount = input("Amount to calculate: ")
calculate (total_amount)    
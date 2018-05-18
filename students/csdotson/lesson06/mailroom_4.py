#!/usr/bin/env python3
# Lesson 6 - Mailroom_4 (Unit testing)

<<<<<<< HEAD
### Function Definitions ###
# def test_func():
#     return True

def prompt(prompt, menu):
    # Create menu based on arguments
=======
def prompt(prompt, menu):
    """ Create menu based on arguments """
>>>>>>> lesson06-mailroom-unit-testing
    while True:
        response = input(prompt)
        try:
            if menu[response]() == "quit":
                break
        except KeyError:
            print('Please enter a valid selection!')


def send_thank_you():
<<<<<<< HEAD
    # Create sub_prompt for creating thank you's and adding new donors/donations
    prompt(thank_you_prompt, thank_you_menu)


def add_donation():
    # Append donation to existing donor, or add donor/donation to existing list
    try:
        donor_name = input("\nPlease enter a donor name: ")
        new_donation = float(input(f"Please enter a donation amount for {donor_name}: "))
    except ValueError:
        print("Please enter a numeric value for 'donation'!")
        add_donation()
    else:
        if donor_name not in donations:
            donations[donor_name] = [new_donation]
        else:
            donations[donor_name].append(new_donation)
        print_email(donor_name, new_donation)


def write_letters():
    # For all donors, generate a thank you letter, and write it to disk as a text file
    for donor in donations:
        file_name = '_'.join(donor.split()) + ".txt"
        with open(file_name, 'w') as f:
            f.write(f"""Dear {donor},

            Thank you very much for your generosity! Your most recent gift of ${(donations[donor][-1])} will be put to great use. So far, you've donated a total of ${sum(donations[donor])}!

            Sincerely,
            The Team""")

            print(f"\nCreated letter for {donor}!")


def print_email(donor, amount):
    # Print formatted email thanking donor
    letter_details = {'name': donor, 'donation_amount': amount}
    letter = "\nDear {name},\n\nThank you so very much for your kind donation of ${donation_amount}. We can assure you that it will be put to great use.\n\nBest,\nChris".format(**letter_details)
    print(letter)


def create_report():
    # Print formatted report showing donors and donation stats
    header = '{:20}|{:^15}|{:^15}|{:>15}'.format("Donor Name", "Total Given", "Num Gifts", "Average Gift")
    print()
    print(header)
    print("-" * len(header))

=======
    """ Create sub_prompt """
    prompt(thank_you_prompt, thank_you_menu)


def prompt_for_donation():
    """ Prompt user for new donor/donation """
    try:
        donor = input("\nPlease enter a donor name: ")
        donation = float(input(f"Please enter a donation amount for {donor}: "))
    except ValueError:
        print("Please enter a numeric value for 'donation'!")
        prompt_for_donation()
    add_donation(donor, donation, donations)
    print_email(donor, donation)


def add_donation(donor, donation, donations):
    """ Add donor/donation data to current donations """
    if donor not in donations:
        donations[donor] = [donation]
    else:
        donations[donor].append(donation)


def write_letters():
    """ Generate thank you's to all donors and write files to disk """
    for donor in donations:
        file_name = '_'.join(donor.split()) + ".txt"
        with open(file_name, 'w') as f:
            f.write(compose_letter(donor, donations))
            print(f"\nCreated letter for {donor}!")


def compose_letter(donor, donations):
        return (f"""Dear {donor},

        Thank you very much for your generosity! Your most recent gift of ${(donations[donor][-1])} will be put to great use. So far, you've donated a total of ${sum(donations[donor])}!

        Sincerely,
        The Team""")


def create_report_header():
    """ Generate formatted header for report """
    header = '{:20}|{:^15}|{:^15}|{:>15}'.format("Donor Name", "Total Given", "Num Gifts", "Average Gift")
    header += '\n'
    header += ("-" * len(header))
    return header


def create_report_data(donations):
    """ Generate data needed for report """
    data = []
>>>>>>> lesson06-mailroom-unit-testing
    for donor, donor_data in donations.items():
        total_given = sum(donor_data)
        num_gifts = len(donor_data)
        avg_gift = total_given / num_gifts
<<<<<<< HEAD
        print('{:21}{:>15.2f}{:>16}{:>16.2f}'.format(donor, total_given, num_gifts, avg_gift))
    print()


def list_donors():
    # Formatted print of donor names
    print("\nList of donors:")
    for donor in donations:
        print(donor)
    print()


def quit_menu():
    # Quit current menu
    return("quit")
=======
        data.append([donor, total_given, num_gifts, avg_gift])
    return data


def create_report_rows(data):
    """ Create formatted data rows for report """
    rows = ''
    for donor, total_given, num_gifts, avg_gift in data:
        rows += '{:21}{:>15.2f}{:>16}{:>16.2f}'.format(donor, total_given, num_gifts, avg_gift) + '\n'
    return rows


def print_report():
    print(create_report_header())
    data = create_report_data(donations)
    print(create_report_rows(data))


def create_email(donor, donation):
    """ Create formatted email thanking donor """
    letter_details = {'name': donor, 'donation_amount': donation}
    letter = "\nDear {name},\n\nThank you so very much for your kind donation of ${donation_amount}. We can assure you that it will be put to great use.\n\nBest,\nChris".format(**letter_details)
    return letter


def print_email(donor, donation):
    print(create_email(donor, donation))


def list_donors(donations):
    """ Create formatted list of donor names """
    donor_names = "\nList of donors:\n"
    for donor in donations:
        donor_names += (donor) + "\n"
    return donor_names


def print_donors():
    print(list_donors(donations))


def quit_menu():
    """ Quit current menu """
    return "quit"
>>>>>>> lesson06-mailroom-unit-testing


### Parameters ###
donations = {"Bill Gates": [10.50, 123.45, 1111.11],
             "Jeff Bezos": [7.65, 1000.00],
             "Paul Allen": [145.90],
             "John Nordstrom": [45.67, 6519.65],
             "Mark Zuck": [789.12]}

# Dictionaries for menu control flow
main_menu = {
    "1": send_thank_you,
<<<<<<< HEAD
    "2": create_report,
=======
    "2": print_report,
>>>>>>> lesson06-mailroom-unit-testing
    "3": write_letters,
    "q": quit_menu,
}

thank_you_menu = {
<<<<<<< HEAD
    "1": add_donation,
    "2": list_donors,
=======
    "1": prompt_for_donation,
    "2": print_donors,
>>>>>>> lesson06-mailroom-unit-testing
    "q": quit_menu,
}

# Prompts used
main_prompt = ("\nWelcome to the Main Menu! What would you like to do?\n1 - Send a Thank You\n2 - Create a Report\n3 - Send letters to everyone\nq - Quit and exit\n--> ")

thank_you_prompt = ("\nPlease choose one of the following:\n1 - Add a donation and send thank you message\n2 - Display list of current donors\nq - Return to main menu\n--> ")


## Execution of file if run as a script ###
if __name__ == "__main__":
    prompt(main_prompt, main_menu)

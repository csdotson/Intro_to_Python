import os
import sys

donor_names = ["John Smith", "Jane Doe", "Alan Smithee", "Tom D.A. Harry", "Joe Shmoe"]
donation_amounts = [[18774.48, 8264.47, 7558.71], [281918.99, 8242.13], [181.97, 955.16], [67.10, 500.98], [200.01]]

donor_db = {name: donation for name, donation in zip(donor_names, donation_amounts)}


def thank_you():
    """Module with three functions:
    1) Append donation to record (if existing donor) or create a new record in database (if not an existing donor.
    2) Print thank you letter after updating database record.
    3) List all current donors in database."""
    user_input = input('Enter a donor\'s full name, or type \'list\' for a full list. ' +
                       'Type \'e\' to exit and return to the main menu.\n> ').title()
    if user_input.lower() == 'list':
        print(list_donors())
        thank_you()
    elif user_input.lower() == 'e':
        mailroom()
    else:
        try:
            donation = float(input("Please enter a donation amount: "))
        except ValueError:
            print("Error: donations can only be entered as numbers and decimals.")
            print("Returning to previous menu...")
            thank_you()
        for k in donor_db:
            if user_input in list_donors() and k != user_input:
                continue
            if user_input in list_donors() and k == user_input:
                donor_db[k].append(donation)
                print("Existing donor found.")
                print("Appending the amount of {0} to {1}'s file...".format(donation, user_input))
                print("Printing thank you email...")
                print("---------------------------")
                print(create_letter(0, user_input, donation))
                print("---------------------------")
                print("Returning to thank you letter menu...")
                thank_you()
            else:
                donor_db[user_input] = [donation]
                print("New donor detected. Creating record for {0}...".format(user_input))
                print("Printing thank you email...")
                print("---------------------------")
                print(create_letter(1, user_input, donation))
                print("---------------------------")
                print("Returning to thank you letter menu...")
                thank_you()


def list_donors():
    """List all donors by name. Called by thank_you() menu."""
    donor_list = [k for k in donor_db]
    return donor_list


def report_printing():
    """Print some user-friendly text and call report_generation() function below."""
    while True:
        print('Donor Name' + ' ' * 16 + '| Total Given | Num Gifts | Average Gift')
        print('-' * 66)
        print(report_generation(donor_db))
        print('Returning to main menu...\n')
        return


def report_generation(database):
    """Generate and return report based on donor_db."""
    report = ""
    for k in database:
        num_gifts = len(database[k])
        total_given = sum(database[k])
        average_gifts = total_given / num_gifts
        report = report + f'{k: <26}| ${total_given:>10.2f} |{num_gifts:^11}| ${average_gifts:>11.2f}\n'
    return report


def filter_report_generation(database):
    """New version of above for filter(). Excludes average, as donors may have 0 values when filtered."""
    report = ""
    for k in database:
        num_gifts = len(database[k])
        total_given = sum(database[k])
        report = report + f'{k: <26}| ${total_given:>10.2f} |{num_gifts:^11}\n'
    return report


def quit_program():
    """Quit Mailroom program."""
    print("Exiting...")
    sys.exit()


def create_letter(donor_status, donor_name, donation_amt):
    """Return formatted letters, depending on options selected. Not intended to be used by itself."""
    if donor_status == 0:
        letter_text = '''
        Dear {0},
    
            Thank you for your very kind donation of ${1}, and for your continuing support.
    
            Your generous contribution will be put to very good use.
    
                           Sincerely,
                              -The Team
                              '''.format(donor_name, donation_amt)
        return letter_text
    elif donor_status == 1:
        letter_text = '''
        Dear {0},

            Thank you for your very kind donation of ${1}.

            Your generous contribution will be put to very good use.

                           Sincerely,
                              -The Team
                              '''.format(donor_name, donation_amt)
        return letter_text
    elif donor_status == 2:
        return('''
        Dear {0},

            Thank you for your very kind contribution(s) totaling ${1}.

            We would like you to know that your generous donation(s) will be put to very good use.

                           Sincerely,
                              -The Team
                              '''.format(donor_name, donation_amt))


def thank_all():
    """Print some user-friendly text and calls create_txt_files() function."""
    current_dir = os.getcwd()
    print("Saving letters to {0}...".format(current_dir))
    create_txt_files()
    print("---------------------------")
    print("Letters saved to text files in directory. Returning to main menu...")
    mailroom()


def create_txt_files():
    """Write letters generated by create_letter to text files, saving them to same directory as script."""
    for k, v in donor_db.items():
        letter = create_letter(2, k, sum(v))
        with open('{:s}.txt'.format(k), 'w') as f:
            f.write(letter)


def challenge_menu():
    """Generate challenge menu text and get user input."""
    user_input1 = input('Enter a multiplier (float or integer) to create a matching challenge for existing donations.' +
                        ' Type \'e\' to exit and return to the main menu.\n> ')
    if user_input1.lower() == 'e':
        mailroom()
    else:
        user_input2 = input('Would you like to enter a minimum and maximum?\n> ')
        if user_input2.lower() == 'yes' or user_input2.lower() == 'y':
            user_input3 = input('Please enter the minimum (numbers only!):\n>')
            user_input4 = input('Please enter the maximum (numbers only!):\n>')
            try:
                challenge(float(user_input1), min_donation=float(user_input3), max_donation=float(user_input4))
                print('Returning to challenge menu...\n')
                challenge_menu()
            except ValueError:
                print("Invalid value. Please enter a number and try again.")
                pass
        else:
            try:
                challenge(float(user_input1))
                print('Returning to challenge menu...\n')
                challenge_menu()
            except ValueError:
                print("Invalid value. Please enter a number and try again.")
                pass


def challenge(factor, **min_max):
    """Create challenge database + report using multiplier, map(), and existing database."""
    challenge_db = dict(list((key, list(map(lambda i: i * factor, value))) for key, value in donor_db.items()))
    if min_max:
        challenge_db = dict(list((key, list(filter(lambda x: min_max['min_donation'] <= x <= min_max['max_donation'],
                                            value))) for key, value in donor_db.items()))
        print('Showing list of donation matching challenge values based on selected multiplier of: {0}x,'
              'as well as selected filters: min ({1}) and max ({2}).'.
              format(factor, min_max['min_donation'], min_max['max_donation']))
        print('Donor Name' + ' ' * 16 + '| Total Given | Num Gifts')
        print('-' * 66)
        print(filter_report_generation(challenge_db))
    else:
        print('Showing list of donation matching challenge values based on selected multiplier of: {0}x.'.
              format(factor))
        print('Donor Name' + ' ' * 16 + '| Total Given | Num Gifts | Average Gift')
        print('-' * 66)
        print(report_generation(challenge_db))


def projection_under():
    less_than = float(input("Donations under which value should be filtered out? (Enter integer or float).\n> "))
    factor = float(input("Enter a multiplier for donations.\n> "))
    matching_db = dict(list((key, list(filter(lambda x: x >= less_than, value))) for key, value in donor_db.items()))
    matching_db = dict(list((key, list(map(lambda x: x * factor, value))) for key, value in matching_db.items()))
    for k in matching_db:
        print("Projected total matching donation for {0} if excluding donations that are less than ${1} "
              "and multiplying by {2}: {3}.\n".format(k, less_than, factor, sum(matching_db[k])))
    projection_menu()


def projection_over():
    more_than = float(input("Donations over which value should be filtered out? (Enter integer or float).\n> "))
    factor = float(input("Enter a multiplier for donations.\n> "))
    matching_db = dict(list((key, list(filter(lambda x: x <= more_than, value))) for key, value in donor_db.items()))
    matching_db = dict(list((key, list(map(lambda x: x * factor, value))) for key, value in matching_db.items()))
    for k in matching_db:
        print("Projected total matching donation for {0} if excluding donations that are more than ${1} "
              "and multiplying by {2}: {3}.\n".format(k, more_than, factor, sum(matching_db[k])))
    projection_menu()


def projection_menu():
    while True:
        selection = input('Donor Projections Menu\n------------------------\n' +
                          'Choose an option:\n1) Donation matching (under)\n2) Donation matching (over)\n' +
                          '3) Quit\n> ')
        menu_dict = {'1': projection_under, '2': projection_over, '3': mailroom}
        try:
            menu_dict.get(selection)()
        except TypeError:
            print("Invalid value. Enter a number from 1-3.")
            pass


def mailroom():
    """Generate main menu options and activate other functions."""
    while True:
        selection = input('MAILROOM v0.4.1: Functional Programming Branch\n------------------------\n' +
                          'Choose an option:\n1) Send a thank you\n2) Create a report\n3) Send letters to everyone' +
                          '\n4) Donation matching challenge\n5) Run projections\n6) Quit\n> ')
        menu_dict = {'1': thank_you, '2': report_printing, '3': thank_all, '4': challenge_menu,
                     '5': projection_menu, '6': quit_program}
        try:
            menu_dict.get(selection)()
        except TypeError:
            print("Invalid value. Enter a number from 1-6.")
            pass


if __name__ == "__main__":
    mailroom()

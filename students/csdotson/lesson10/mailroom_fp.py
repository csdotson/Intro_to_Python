#!/usr/bin/env python3
# Lesson 10 - Functional Programming Mailroom

class Donor:
    """ Create Donor class representing a donor and all donations """
    def __init__(self, name, donations=[]):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("Name should be a string value")
        self.donations = donations

    @property
    def total_donation(self):
        return sum(self.donations)

    @property
    def number_of_donations(self):
        return len(self.donations)

    @property
    def average_donation(self):
        return self.total_donation / self.number_of_donations

    def __contains__(self, name):
        if name in self.name:
            return True

    def add_donation(self, donation):
        if donation < 0:
            raise ValueError("Donation can't be negative")
        self.donations.append(donation)

    def create_email(self):
        """ Create formatted email thanking donor """
        letter_details = {
            'name': self.name,
            'donation_amount': self.donations[-1]
            }
        letter = "\nDear {name},\n\nThank you so very much for your kind donation of ${donation_amount}. We can assure you that it will be put to great use.\n\nBest,\nChris".format(**letter_details)
        return letter

    def compose_letter(self):
            return (f"""Dear {self.name},

            Thank you very much for your generosity! Your most recent gift of ${self.donations[-1]} will be put to great use. So far, you've donated a total of ${self.total_donation}!

            Sincerely,
            The Team""")

    def __repr__(self):
        return "Donor({},{})".format(self.name, repr(self.donations))

    def __str__(self):
        return "Donor: {}, Donations: {}".format(self.name, self.donations)


class DonorCollection():
    """ Create container object to hold multiple donors """
    def __init__(self, donors=[]):
        self.donors = donors
        self.index = 0

    def add_new_donor(self, donor):
        self.donors.append(donor)

    def __len__(self):
        return len(self.donors)

    def __getitem__(self, index):
        return self.donors[index]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self):
            raise StopIteration
        else:
            self.index += 1
            return self.donors[self.index - 1]

    def __contains__(self, item):
        if item in self.donors:
            return True

    def find_donor(self, name):
        current_donor = None
        for donor in self.donors:
            if name in donor:
                current_donor = donor
        return current_donor

    def list_donors(self):
        """ Create formatted list of donor names """
        donor_names = "\nList of donors:\n"
        for donor in self.donors:
            donor_names += donor.name + '\n'
        return donor_names

    def create_report_header(self):
        """ Generate formatted header for report """
        header = '{:20}|{:^15}|{:^15}|{:>15}'.format("Donor Name", "Total Given", "Num Gifts", "Average Gift") + '\n'
        header += ("-" * len(header))
        return header

    def generate_report(self):
        """ Create formatted data for report """
        rows = ''
        for donor in self.donors:
            rows += '{:21}{:>15.2f}{:>16}{:>16.2f}'.format(
                donor.name,
                donor.total_donation,
                donor.number_of_donations,
                donor.average_donation) + '\n'
        return rows

    def write_letters(self):
        """ Generate thank you's to all donors and write files to disk """
        for donor in self.donors:
            file_name = '_'.join(donor.name.split()) + ".txt"
            with open(file_name, 'w') as f:
                f.write(donor.compose_letter())
                print(f"\nCreated letter for {donor.name}!")

    def challenge(self, factor):
        """ Multiply all donations by a given factor """
        challenge_donors = DonorCollection([])
        for donor in self.donors:
            donations = list(map(lambda donation: donation * factor, donor.donations))
            challenge_donors.add_new_donor(Donor(donor.name, donations))
        return challenge_donors

    def donation_filter(self):
        pass

    def __repr__(self):
        return "DonorCollection({})".format(repr(self.donors))

    def __str__(self):
        return "Donor collection with: {}".format(self.donors)

# d1 = Donor("Bill Gates", [100.00, 20.00, 35.00])
# d2 = Donor("Jeff Bezos", [1.34, 5.67])
# d3 = Donor("Paul Allen", [167.00])
# donors = DonorCollection([d1, d2, d3])

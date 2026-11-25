
import time
import json


print("Project Name: Smart Washing Machine")
print("Made by: Priya Kumari")
print("-" * 40)
print("    WELCOME TO WASHING MACHINE")
print("-" * 40)


class WashingMachine:

    def __init__(self):
        self.power = False
        self.weight = 0
        self.water_level = "Not Selected"
        self.program = "Not Selected"
        self.duration = 0
        self.water = False
        self.detergent = False
        self.stage = "Standby"

        self.history = self.load_history()

    # Load previous washing history from JSON file
    def load_history(self):
        try:
            with open("washing_history.json", "r") as file:
                history = json.load(file)

                if isinstance(history, list):
                    return history
                return []

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("History file is empty or damaged.")
            return []

    # Save washing history in JSON file
    def save_history(self):
        with open("washing_history.json", "w") as file:
            json.dump(self.history, file, indent=4)

    # Display all previous washing records
    def show_history(self):
        print("\n--------- WASHING HISTORY ---------")

        if not self.history:
            print("No washing history available.")

        else:
            for index, record in enumerate(self.history, start=1):
                print("\nWash Number:", index)
                print("Weight:", record.get("weight", "N/A"), "kg")
                print("Water Level:", record.get("water_level", "N/A"))
                print("Program:", record.get("program", "N/A"))
                print("Duration:", record.get("duration", "N/A"), "minutes")
                print("Starting Time:", record.get("starting_time", "N/A"))
                print("Completed Time:", record.get("completed_time", "N/A"))

        print("-----------------------------------")

    # Timer function
    def run_timer(self, seconds):
        for remaining in range(seconds, 0, -1):
            minutes = remaining // 60
            secs = remaining % 60

            print(
                f"Time Remaining: {minutes:02d}:{secs:02d}",
                end="\r",
                flush=True
            )
            time.sleep(1)

        print("Time Remaining: 00:00")

    # Turn ON the machine
    def power_on(self):
        self.power = True
        self.stage = "Ready"

        print("\nMachine is now ON!")
        print("Starting Time:", time.strftime("%I:%M:%S %p"))

    # Turn OFF the machine
    def power_off(self):
        self.power = False
        self.stage = "Standby"

        print("\nMachine is now OFF!")

    # Select clothes weight
    def select_weight(self):
        while True:
            try:
                weight = float(input("\nEnter clothes weight (1-7 kg): "))

                if 1 <= weight <= 7:
                    self.weight = weight

                    if weight <= 2:
                        self.water_level = "Low"
                    elif weight <= 4:
                        self.water_level = "Medium"
                    else:
                        self.water_level = "High"

                    print("Water Level:", self.water_level)
                    break

                else:
                    print("Enter weight between 1 and 7 kg.")

            except ValueError:
                print("Please enter a valid number.")

    # Select washing program
    def select_program(self):
        print("\n1. Quick Wash - 1 minute")
        print("2. Normal Wash - 3 minutes")
        print("3. Heavy Wash - 4 minutes")
        print("4. Soft Wash - 2 minutes")

        programs = {
            "1": ("Quick Wash", 1),
            "2": ("Normal Wash", 3),
            "3": ("Heavy Wash", 4),
            "4": ("Soft Wash", 2)
        }

        while True:
            choice = input("Select wash program: ").strip()

            if choice in programs:
                self.program, self.duration = programs[choice]

                print("Selected Program:", self.program)
                print("Wash Time:", self.duration, "minutes")
                break

            else:
                print("Please select 1, 2, 3 or 4.")

    # Check water supply
    def check_water(self):
        while True:
            choice = input(
                "\nIs water available? (yes/no): "
            ).lower().strip()

            if choice == "yes":
                self.water = True
                print("Water supply is available.")
                break

            elif choice == "no":
                print("Please arrange water first.")

            else:
                print("Enter yes or no.")

    # Check detergent
    def add_detergent(self):
        while True:
            choice = input(
                "Have you added detergent? (yes/no): "
            ).lower().strip()

            if choice == "yes":
                self.detergent = True
                print("Detergent check complete.")
                break

            elif choice == "no":
                print("Please add detergent first.")

            else:
                print("Enter yes or no.")

    # Check machine lid
    def close_lid(self):
        while True:
            choice = input(
                "Is the machine lid closed? (yes/no): "
            ).lower().strip()

            if choice == "yes":
                print("Lid is closed.")
                return True

            elif choice == "no":
                print("Please close the lid.")

            else:
                print("Enter yes or no.")

    # Start washing process
    def start_wash(self):
        if not self.power:
            print("Machine is OFF!")
            return False

        if not self.water or not self.detergent:
            print("Please check water and detergent.")
            return False

        if not self.close_lid():
            return False

        total_seconds = self.duration * 60
        start_time = time.strftime("%I:%M:%S %p")

        print("\nWASHING STARTED!")
        print("Program:", self.program)
        print("Total Wash Time:", self.duration, "minutes")
        print("Starting Time:", start_time)

        current_stage = ""

        for remaining in range(total_seconds, 0, -1):
            elapsed = total_seconds - remaining
            progress = elapsed / total_seconds

            if progress < 0.10:
                stage = "Filling Water"
                message = "Water is filling into the drum."

            elif progress < 0.60:
                stage = "Washing Clothes"
                message = "Washing clothes..."

            elif progress < 0.80:
                stage = "Rinsing Clothes"
                message = "Rinsing clothes with clean water..."

            else:
                stage = "Draining Water"
                message = "Draining dirty water..."

            if stage != current_stage:
                current_stage = stage
                self.stage = stage
                print("\n" + message)

            minutes = remaining // 60
            seconds = remaining % 60

            print(
                f"Time Remaining: {minutes:02d}:{seconds:02d}",
                end="\r",
                flush=True
            )

            time.sleep(1)

        print("Time Remaining: 00:00")

        self.stage = "Wash Complete"

        completed_time = time.strftime("%I:%M:%S %p")

        print("\nWASHING COMPLETED!")
        print("Starting Time:", start_time)
        print("Completed Time:", completed_time)

        # Create a record of the completed wash
        wash_record = {
            "weight": self.weight,
            "water_level": self.water_level,
            "program": self.program,
            "duration": self.duration,
            "starting_time": start_time,
            "completed_time": completed_time
        }

        # Add record to history and save it
        self.history.append(wash_record)
        self.save_history()

        print("Washing history saved successfully!")

        return True

    # Spin dry clothes
    def spin_dry(self):
        if not self.power:
            print("Machine is OFF!")
            return False

        if not self.close_lid():
            return False

        while True:
            try:
                duration = int(
                    input("Enter spin-dry time (1-10 minutes): ")
                )

                if 1 <= duration <= 10:
                    break

                else:
                    print("Enter time between 1 and 10 minutes.")

            except ValueError:
                print("Enter a valid number.")

        start_time = time.strftime("%I:%M:%S %p")

        self.stage = "Spinning Clothes"

        print("\nSPIN DRY STARTED!")
        print("Drying Time:", duration, "minutes")
        print("Starting Time:", start_time)

        self.run_timer(duration * 60)

        self.stage = "Drying Complete"

        completed_time = time.strftime("%I:%M:%S %p")

        print("\nRemoving extra water from clothes...")
        print("SPIN DRY COMPLETED!")
        print("Starting Time:", start_time)
        print("Completed Time:", completed_time)
        print("Clothes may still be slightly damp.")

        return True

    # Display current machine status
    def show_status(self):
        print("\n--------- MACHINE STATUS ---------")

        print("Power:", "ON" if self.power else "OFF")
        print("Weight:", self.weight, "kg")
        print("Water Level:", self.water_level)
        print("Wash Program:", self.program)
        print("Wash Duration:", self.duration, "minutes")

        print(
            "Water Supply:",
            "Available" if self.water else "Unavailable"
        )

        print(
            "Detergent:",
            "Added" if self.detergent else "Not Added"
        )

        print("Current Stage:", self.stage)
        print("Current Time:", time.strftime("%I:%M:%S %p"))
        print("----------------------------------")


# Main program
machine = WashingMachine()


# Main menu
while True:
    print("\n--------- SMART WASHING MACHINE ---------")
    print("1. Start Washing Machine")
    print("2. View Washing History")
    print("3. Exit")
    print("-----------------------------------------")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        machine.power_on()
        break

    elif choice == "2":
        machine.show_history()

    elif choice == "3":
        print("\nThank you for using Washing Machine!")
        raise SystemExit

    else:
        print("Please select 1, 2 or 3.")


# Washing machine main loop
while machine.power:

    machine.select_weight()
    machine.select_program()
    machine.check_water()
    machine.add_detergent()

    wash_success = machine.start_wash()

    if not wash_success:
        print("Washing could not be completed.")
        machine.power_off()
        break

    dry_success = machine.spin_dry()

    if not dry_success:
        print("Spin drying could not be completed.")
        machine.power_off()
        break

    machine.show_status()

    choice = input(
        "\nDo you want to wash more clothes? (yes/no): "
    ).lower().strip()

    if choice == "yes":

        machine.weight = 0
        machine.water_level = "Not Selected"
        machine.program = "Not Selected"
        machine.duration = 0
        machine.water = False
        machine.detergent = False
        machine.stage = "Ready"

        print("\nReady for the next load!")

    elif choice == "no":

        machine.power_off()

        print("\nThank you for using Smart Washing Machine!")
        print("Have a nice day!")
        break

    else:

        print("Invalid choice. Machine will now turn OFF.")

        machine.power_off()

        print("Thank you for using Washing Machine!")
        break

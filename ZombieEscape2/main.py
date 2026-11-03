import guitk as ui
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import random
import time


class ZombieEscape(ui.Window):
    def config(self):
        self.title = "Zombie Escape"

        with ui.VLayout():
            ui.Label("", image="ClassroomI.png", key="image")
            with ui.HStack(halign="center"):
                ui.Button(text="text!", key="a")
                ui.Button(text="text!", key="b")
                ui.Button(text="text!", key="c")
                ui.Button(text="text!", key="d")

    def update_image(self, filename: str):
        try:
            image = tk.PhotoImage(file=filename)
            self["image"].widget.configure(image=image)
            self["image"].widget.image = image
        except Exception:
            # Safe fallback if images are missing locally during development
            print(f"Image notice: '{filename}' asset could not load.")

    def setup_room(self, image: str, button_a: str, button_b: str, button_c: str, button_d: str):
        self.room = image
        self.update_image(image)

        self["a"].widget.configure(text=button_a or "")
        self["a"].disabled = button_a is None

        self["b"].widget.configure(text=button_b or "")
        self["b"].disabled = button_b is None

        self["c"].widget.configure(text=button_c or "")
        self["c"].disabled = button_c is None

        self["d"].widget.configure(text=button_d or "")
        self["d"].disabled = button_d is None

    def setup(self):
        self.setup_room("menu.png", None, "Run", "Incident Logs", None)

    @ui.on("a")
    def on_button_a(self):
        if self.room == "menu.png":
            pass
        elif self.room in ["Lockers.png", "CanteenI.png", "ClassroomI.png", "StaffroomI.png"]:
            self.move()
        elif self.room in ["CanteenO.png", "ClassroomO.png", "StaffroomO.png"]:
            pass
        elif self.room == "Bag":
            self.tracker()
        elif self.room == "Corridor.png":
            self.forward()

    @ui.on("b")
    def on_button_b(self):
        if self.room == "menu.png":
            self.beginning()
        elif self.room in ["Lockers.png", "CanteenI.png", "ClassroomI.png", "StaffroomI.png"]:
            self.search()
        elif self.room in ["CanteenO.png", "ClassroomO.png", "StaffroomO.png"]:
            self.yes()
        elif self.room == "Bag":
            self.medkit()
        elif self.room == "Corridor.png":
            self.left()

    @ui.on("c")
    def on_button_c(self):
        if self.room == "menu.png":
            self.logs()
        elif self.room in ["Lockers.png", "CanteenI.png", "ClassroomI.png", "StaffroomI.png"]:
            self.use()
        elif self.room in ["CanteenO.png", "ClassroomO.png", "StaffroomO.png"]:
            self.move()
        elif self.room == "Bag":
            self.antiz()
        elif self.room == "Corridor.png":
            self.right()

    @ui.on("d")
    def on_button_d(self):
        if self.room == "menu.png":
            pass
        elif self.room in ["Lockers.png", "CanteenI.png", "ClassroomI.png", "StaffroomI.png"]:
            self.hide()
        elif self.room in ["CanteenO.png", "ClassroomO.png", "StaffroomO.png"]:
            pass
        elif self.room == "Bag":
            self.placeholder()
        elif self.room == "Corridor.png":
            self.backwards()

    def beginning(self):
        self.noises1 = False
        self.noises2 = False
        self.keycard = False
        self.override = False
        self.medkit = False
        self.antiz = False
        self.health = 100
        self.infection = 0
        self.tracker = False

        self.setup_room("ClassroomI.png", "Move", "Search", "Use", "Hide")
        self.name = None
        while self.name is None or len(self.name.strip()) == 0:
            self.name = sd.askstring("Zombie Escape", "Please enter your name.")
        mb.showinfo("Zombie Escape", f"Your username is {self.name}.")

        mb.showinfo("Opening", "It is 4:10pm. The emergency shutters have started closing.\n"
                               "You are in a classroom, with no recollection of how you got here.... Or where here is really.\n"
                               "But you know you need to escape, but the exits are locked down.\n"
                               "Something is telling you that you will either need a keycard or an override code to get through the exit when you can find it")

        maybe = random.randint(1, 1000)
        if maybe >= 900:
            mb.showinfo("Outcome", "You start with 1 Medkit")
            self.medkit = True
        elif maybe >= 800:
            mb.showinfo("Outcome", "You start with 1 AntiZ")
            self.antiz = True
        else:
            mb.showinfo("Outcome", "You start with no items of use")

    def logs(self):
        try:
            with open("Incident Report Logs.txt", "r") as file:
                content = file.read()
                mb.showinfo("Recovered Incident Report Logs", f"{content}")
        except FileNotFoundError:
            mb.showinfo("Recovered Incident Report Logs", "No incident logs have been recorded yet.")

    def log_failure(self, complication_text):
        """Helper method to clean up redundant log writing code."""
        with open("Incident Report Logs.txt", "a") as file:
            file.write(f"\nIncident report:\n"
                       f"{self.name} - Ran the Simulation\n"
                       f"Escape - Failure\n"
                       f"Complications - {complication_text}\n"
                       f"Health left - {self.health}\n"
                       f"Infection Percentage - {self.infection}%\n")
        self.setup()  # Return player safely to the main menu screen

    def move(self):
        if self.noises1 == True:
            mb.showinfo("GROANER", "The groaner found you and attacks until it is bored")
            self.health = self.health - 10
            self.infection = self.infection + 25
            mb.showinfo("ATTACKED", "You take 10 health and gain 25 infection")
            self.noises1 = False

            if self.health <= 0:
                mb.showinfo("Game over!", "You ran out of health.")
                self.log_failure("Eaten by a Groaner")
                return
            elif self.infection >= 100:
                mb.showinfo("Game over!", "You became fully infected.")
                self.log_failure("Fully Infected by a Groaner")
                return
            else:
                mb.showinfo("Moving on", "You carry on and find yourself in a corridor")
                self.corridor()
                return

        elif self.noises2 == True:
            mb.showinfo("CLICKER", "The clicker found you and attacks until it is bored")
            self.health = self.health - 25
            self.infection = self.infection + 10
            mb.showinfo("Attacked", "You take 25 health and gain 10 infection")
            self.noises2 = False

            if self.health <= 0:
                mb.showinfo("Game over!", "You ran out of health.")
                self.log_failure("Eaten by a Clicker")
                return
            elif self.infection >= 100:
                mb.showinfo("Game over!", "You became fully infected.")
                self.log_failure("Fully Infected by a Clicker")
                return
            else:
                mb.showinfo("Moving on", "You carry on and find yourself in a corridor")
                self.corridor()
                return

        else:
            # Safe default fallback path if there are no noises
            mb.showinfo("Moving on", "You slip away safely into the corridor.")
            self.corridor()

    def corridor(self):
        self.setup_room("Corridor.png", "Forward", "Left", "Right", "Backwards")

    def forward(self):
        mb.showinfo("Action", "You move forward.")
        poi=random.randint(1,25)
        if poi<=5:
            self.lockers()
        elif poi<=10:
            self.classroomO()
        elif poi<=15:
            self.canteenO()
        elif poi<=20:
            self.staffroomO()
        else:
            self.move()

    def left(self):
        mb.showinfo("Action", "You turn left.")
        poi = random.randint(1, 25)
        if poi <= 5:
            self.lockers()
        elif poi <= 10:
            self.classroomO()
        elif poi <= 15:
            self.canteenO()
        elif poi <= 20:
            self.staffroomO()
        else:
            self.move()

    def right(self):
        mb.showinfo("Action", "You turn right.")
        poi = random.randint(1, 25)
        if poi <= 5:
            self.lockers()
        elif poi <= 10:
            self.classroomO()
        elif poi <= 15:
            self.canteenO()
        elif poi <= 20:
            self.staffroomO()
        else:
            self.move()

    def backwards(self):
        mb.showinfo("Action", "You back up.")
        poi = random.randint(1, 25)
        if poi <= 5:
            self.lockers()
        elif poi <= 10:
            self.classroomO()
        elif poi <= 15:
            self.canteenO()
        elif poi <= 20:
            self.staffroomO()
        else:
            self.move()

    def yes(self):
        mb.showinfo("Action", "You confirm.")
        if self.room==self.canteenO:
            self.canteenI()
        elif self.room==self.staffroomO:
            self.staffroomI()
        elif self.room==self.canteenO:
            self.canteenI()
        else:
            pass

    def no(self):
        self.corridor()

    def search(self):
        if self.noises1 == True:
            mb.showinfo("GROANER", "The groaner found you and attacks until it is bored")
            self.health = self.health - 10
            self.infection = self.infection + 25
            mb.showinfo("ATTACKED", "You take 10 health and gain 25 infection")
            self.noises1 = False

            if self.health <= 0:
                mb.showinfo("Game over!", "You ran out of health.")
                self.log_failure("Eaten by a Groaner")
                return
            elif self.infection >= 100:
                mb.showinfo("Game over!", "You became fully infected.")
                self.log_failure("Fully Infected by a Groaner")
                return
            else:
                pass
        elif self.noises2 == True:
            mb.showinfo("CLICKER", "The clicker found you and attacks until it is bored")
            self.health = self.health - 25
            self.infection = self.infection + 10
            mb.showinfo("Attacked", "You take 25 health and gain 10 infection")
            self.noises2 = False

            if self.health <= 0:
                mb.showinfo("Game over!", "You ran out of health.")
                self.log_failure("Eaten by a Clicker")
                return
            elif self.infection >= 100:
                mb.showinfo("Game over!", "You became fully infected.")
                self.log_failure("Fully Infected by a Clicker")
                return
            else:
                pass
        mb.showinfo("Search", "You chose to search the area")
        found = random.randint(1, 100)
        if found <=5:
            mb.showinfo("Loot", "You have a found a Keycard")
            self.keycard = True
        elif found <= 10:
            mb.showinfo("Loot", "You have found an Override Code")
            self.override = True
        elif found <=15:
            mb.showinfo("Loot", "You have found a Medkit")
            self.medkit = True
        elif found <=20:
            mb.showinfo("Loot", "You have found AntiZ (It reduces infection amount)")
            self.antiz = True
        elif found <=25:
            mb.showinfo("Loot", "You have found a tracker. Maybe try using it")
            self.tracker = True
        else:
            mb.showinfo("Loot", "You couldn't find anything of use")

    def use(self):
        mb.showinfo("Action", "You try to use an item. Select which item you try to use")
        self.setup_room("Bag.jpg", "Medkit", "AntiZ", "Tracker", "Placeholder")
        if self.noises1 == True:
            mb.showinfo("GROANER", "But first, The groaner found you and attacks until it is bored")
            self.health = self.health - 10
            self.infection = self.infection + 25
            mb.showinfo("ATTACKED", "You take 10 health and gain 25 infection")
            self.noises1 = False

            if self.health <= 0:
                mb.showinfo("Game over!", "You ran out of health.")
                self.log_failure("Eaten by a Groaner")
                return
            elif self.infection >= 100:
                mb.showinfo("Game over!", "You became fully infected.")
                self.log_failure("Fully Infected by a Groaner")
                return
            else:
                mb.showinfo("Moving on", "You try to use an item anyway")
                self.corridor()
                return

        elif self.noises2 == True:
            mb.showinfo("CLICKER", "But first, The clicker found you and attacks until it is bored")
            self.health = self.health - 25
            self.infection = self.infection + 10
            mb.showinfo("Attacked", "You take 25 health and gain 10 infection")
            self.noises2 = False

            if self.health <= 0:
                mb.showinfo("Game over!", "You ran out of health.")
                self.log_failure("Eaten by a Clicker")
                return
            elif self.infection >= 100:
                mb.showinfo("Game over!", "You became fully infected.")
                self.log_failure("Fully Infected by a Clicker")
                return
            else:
                mb.showinfo("Moving on", "You Try to use an item anyway")

    def tracker(self):
        if self.tracker==True:
            mb.showinfo("The tracker is pointing you to an exit")
            decision = str(input("Do you follow it now (it is not single use)"))
            decision = decision.lower()
            if decision == "yes":
                exit()
            else:
                mb.showinfo("You put the tracker away for now")

    def medkit(self):
        if medkit == True and self.health != 100:
            self.health = self.health + 25
            if self.health > 100:
                self.health = 100
            else:
                self.health = self.health

    def antiz(self):
        if antiz == True and self.infection != 0:
            self.infection = self.infection - 15
            if self.infection < 0:
                self.infection = 0
            else:
                self.infection = self.infection

    def palceholder(self):
        if placeholder == True:
            pass
        else:
            pass

    def lockers(self):
        mb.showinfo("Location", "You find yourself at some lockers")
        self.setup_room("Lockers.png", "Move", "Search", "Use", "Hide")

    def hide(self):
        mb.showinfo("Hiding", "You find a spot to hide.\n"
"You dont move until the noises move away")
        self.noises1=False
        self.noises2=False

    def canteenO(self):
        mb.showinfo("Location", "You find yourself outside a canteen\n"
"Do you choose to enter")
        self.setup_room("CanteenO.png", None, "Yes", "No", None)

    def canteenI(self):
        mb.showinfo("Location", "You find yourself inside a canteen")
        self.setup_room("CanteenI.png", "Move", "Search", "Use", "Hide")

    def classroomO(self):
        mb.showinfo("Location", "You find yourself outside a classroom\n"
"Do you choose to enter")
        self.setup_room("ClassroomO.png", None, "Yes", "No", None)

    def classroomI(self):
        mb.showinfo("Location", "You find yourself inside a classroom")
        self.setup_room("ClassroomI.png", "Move", "Search", "Use", "Hide")

    def staffroomO(self):
        mb.showinfo("Location", "You find yourself outside a staffroom\n"
"Do you choose to enter")
        self.setup_room("StaffroomO.png", None, "Yes", "No", None)

    def staffroomI(self):
        mb.showinfo("Location", "You find yourself inside a staffroom")
        self.setup_room("StaffroomI.png", "Move", "Search", "Use", "Hide")

    def exit(self):
        self.setup_room("exitimg.jpg", None, None, None, None)
        mb.showinfo("It is time", "You find yourself at the exit but you hear groaning and clicking from different sources.\n"
"You know you have to escape now")
        if self.keycard == True:
            print("You use the keycard and escape before the Groaners and Clickers reach you\n"
"You Successfully escaped and Win!\n"
"(More to come in this section, WIP.)")
            with open("Incident Report Logs.txt", "a") as file:
                file.write(f"Incident report:\n"
f"{name} - Ran the Simulation\n"
f"Escape - Successful \n"
f"Complications - None\n"
f"Health left - {health}\n"
f"Infection Percentage - {infection}")
            file.close
        elif self.override == True:
            print(
                "You use the override code and escape but the Groaners and Clickers are chasing. You may have won but it is not over yet!\n"
"(This section is still a work in progress, so for the time being this counts as a victory.")
            print("You Successfully escaped and Win!")
            with open("Incident Report Logs.txt", "a") as file:
                file.write(f"Incident report:\n"
                           f"{name} - Ran the Simulation\n"
                           f"Escape - Successful \n"
                           f"Complications - Chased While Escaping\n"
                           f"Health left - {health}\n"
                           f"Infection Percentage - {infection}")
            file.close
        else:
            print(
                "You did not have a keycard or override code and as the Groaners and Clickers swarm you, you think to yourself. Why did i get overzealous and not prepare better?")
            print("You got swarmed at the exit and Lost!")
            with open("Incident Report Logs.txt", "a") as file:
                file.write(f"Incident report:\n"
                           f"{name} - Ran the Simulation\n"
                           f"Escape - Failure \n"
                           f"Complications - Swarmed While Trying to Escape\n"
                           f"Health left - {health}\n"
                           f"Infection Percentage - {infection}")
                #eventually add 2nd part that starts here
            file.close

if __name__ == "__main__":
    instance = ZombieEscape()
    instance.run()

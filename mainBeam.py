# myImports imports the neccesary libraries (matplotlib, os, numpy, tkinter, pickle)
from myImports import *
# settings import the global variables
from settings import *
# functions loads the functions which are described in the project
from functions import *


class BacteriaGrowth(tk.Tk):

    # __init__ initialises starting conditions such as dictionary of frames, the grid and starting frame.
    def __init__(self, *args, **kwargs):

        self.count = 0
        self.labels = {}

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Bacteria growth")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("1100x800")

        self.frames = {}

        for F in (StartPage, Info):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # show_frame moves selected frame to the top I.e. current showing frame.
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


# The main frame where the user inputs data
class StartPage(tk.Frame):

    # saveConfig prompts the user for a file name and saves the necessary configs to the file
    # Input: None, prompts user for input
    # Output: None, creates file
    def saveConfig(self):
        file_name = tk.simpledialog.askstring(
            "File name", "Pick a file name")
        with open(file_name, 'wb') as f:
            pickle.dump(variables, f)

    # loadConfig loads a file and changes the entry boxes
    # Input: None, prompts user for input
    # Output: None, Changes entry

    def loadConfig(self):
        files = askopenfile()
        if files:
            file_name = os.path.basename(files.name)
            pickle_in = open(file_name, "rb")
            variables = pickle.load(pickle_in)

            entryLength.delete(0, "end")
            entryLength.insert(0, str(variables[1]))

            beamDeflection(variables[0], variables[1],
                           variables[2], variables[3], variables[4])

    # addBox adds entry boxes for load position and load when the botton Add is pressed
    # Input: None
    # Output: None, creates entry boxes
    def addBox(self):
        self.num_rows += 1

        ent1 = Entry(self, width=5)
        ent1.grid(column=5, row=5+self.num_rows, sticky='WE')

        ent2 = Entry(self, width=5)
        ent2.grid(column=7, row=5+self.num_rows, sticky='WE')

        load_entries.append((ent1, ent2))

    # removeLoad removes all the created entries for loads
    # Input: None
    # Output: None, deletes entry boxes

    def removeLoad(self):
        iter_loads = iter(load_entries)
        next(iter_loads)

        for (ent1, ent2) in iter_loads:
            ent1.destroy()
            ent2.destroy()

    # showEntries loads the data from the entry boxes and calls the function beamPlot()
    # Input: None, reads global variables (entries)
    # Output: Calls beamPlot() which ultimately creates a plot
    def showEntries(self):

        global entryLength, options, entryPosition, x, y, variables

        # List which the forces will be appended to.
        forces = []

        # Appending forces to the list.
        for number, (ent1, ent2) in enumerate(load_entries):
            forces.append(int(ent1.get()))

        # List which the positions of the given forces will be appended to.
        forcePositions = []

        # Appending positions of forces to the list.
        for number, (ent1, ent2) in enumerate(load_entries):
            forcePositions.append(int(ent2.get()))

        # Seperating the users wanted positions for deflection by ',' and putting the integers in a list. This makes them accessable during computation,
        computePositions = [int(x) for x in (entryPosition.get()).split(',')]

        # This if statement determines which formula to use depending of the number of loads.

        # If there is multiple loads we use the beamSuperpostition function to compute deflection.
        if len(forces) > 1:
            variables.append(computePositions)
            variables.append(float(entryLength.get()))
            variables.append(forcePositions)
            variables.append(forces)
            variables.append(options.get())
            beamPlot(variables[1], variables[2], variables[3], variables[4])

        # If there is only one load we use the beamDeflection function to compute deflection.
        if len(forces) == 1:
            variables.append(computePositions)
            variables.append(float(entryLength.get()))
            variables.append(forcePositions[0])
            variables.append(forces[0])
            variables.append(options.get())
            beamDeflection(variables[0], variables[1],
                           variables[2], variables[3], variables[4])

            graphForces = forces
            graphPositions = forcePositions

            # If statement making shure the right plot is used depending on the number of loads (represented by the lenght of loadPosition).
            if variables[2] < variables[1] and int(variables[2]) > 0:
                beamPlot(variables[1], graphPositions,
                         graphForces, variables[4])

            if variables[2] > variables[1] or int(variables[2]) < 0:
                tk.messagebox.showinfo("Beware", str(
                    variables[2]) + " is outside of the length of the beam. Please change.")

        graphForces = forces
        graphPositions = forcePositions

        beamDeflection(variables[0], variables[1],
                       variables[2], variables[3], variables[4])

        # To be able to print the computed deflection. The list of deflections are saved in a variable making them accesable by index.
        deflectionList = beamDeflection(
            variables[0], variables[1], variables[2], variables[3], variables[4])

        # For loop that for every computed deflection prints a string, the position and the deflection at the given position.
        for i in range(len(variables[0])):
            print("The deflection for " +
                  str(variables[0][i]) + " is " + str(deflectionList[i]))

    # The main frame defines all the tkinter widgets and assigns them in a neat grid

    def __init__(self, parent, controller):
        self.num_rows = 1

        global entryLength, options, entryPosition, load_entries

        tk.Frame.__init__(self, parent)

        self.label_list = []

        title = ttk.Label(self, text="Beam deflection", font=(None, 44))

        position_label = ttk.Label(
            self, text="Insert positions where \nyou want deflection computed \n(seperated by \" , \")")
        entryPosition = Entry(self, width=5)

        length = ttk.Label(self, text="Length [m]: ")
        entryLength = Entry(self, width=5)
        entryLength.insert(0, 10)

        support_label = ttk.Label(self, text="Support: ")
        options = tk.StringVar(self)
        options.set("Both")
        supportList = ["Both", "Cantilever"]
        dropSupport = OptionMenu(self, options, "Both", "Cantilever")
        dropSupport.configure(width=5)

        load = ttk.Label(self, text="Load [N]: ")
        entryLoad = Entry(self, width=5)

        loadPos = ttk.Label(self, text="Load position [m]: ")
        entryLoadPos = Entry(self, width=5)

        add = ttk.Label(self, text="Add load: ")
        addBtn = ttk.Button(self, text="Add", width=5, command=self.addBox)

        deleteBtn = ttk.Button(self, text="Delete",
                               width=5, command=self.removeLoad)

        showButton = ttk.Button(
            self, text='Compute', command=self.showEntries)
        showButton.grid(column=5, row=6, pady=90)

        loadButton = ttk.Button(
            self, text='Load', command=self.loadConfig)
        loadButton.grid(column=0, row=0, pady=40, padx=(10, 0))
        saveButton = ttk.Button(
            self, text='Save', command=self.saveConfig)
        saveButton.grid(column=1, row=0, pady=40)

        title.grid(column=3, row=0, columnspan=4)
        position_label.grid(column=3, row=2,  columnspan=4, rowspan=2)
        entryPosition.grid(column=3, row=4, columnspan=4)
        length.grid(column=0, row=7, padx=(40, 0))
        entryLength.grid(column=1, row=7)
        support_label.grid(column=2, row=7, padx=(40, 0))
        dropSupport.grid(column=3, row=7)
        load.grid(column=4, row=7, padx=(40, 0))
        entryLoad.grid(column=5, row=7)
        loadPos.grid(column=6, row=7, padx=(40, 0))
        entryLoadPos.grid(column=7, row=7)
        add.grid(column=8, row=7, padx=(40, 0))
        addBtn.grid(column=9, row=7, padx=(0, 40))
        deleteBtn.grid(column=9, row=8, padx=(0, 40))

        load_entries.append((entryLoad, entryLoadPos))


class Info(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Info")
        label.pack(pady=20, padx=20)

        button = ttk.Button(self, text="Back to start",
                            command=lambda: controller.show_frame(StartPage))
        button.pack(pady=20, padx=20)


app = BacteriaGrowth()
app.mainloop()

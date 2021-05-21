from myImports import *
from settings import *


# beamDeflection computes the deflection of a beam with a single load.
def beamDeflection(positions, beamLength, loadPosition, loadForce, beamSupport):
    # E and I are contants for the stiffness of the beam.
    EI = 200*(10**9) * 0.001

    # Empty list that the computed deflections will be appended to.
    posDeflection = []

    # For loop iterating over the wanted positions and computing the deflection for these.
    for i in range(len(positions)):

        # If/else statement deciding which formula to use depending on the users input.
        if beamSupport == "Both":
            if positions[i] < loadPosition:
                y = ((loadForce*(beamLength - loadPosition)*positions[i]) / (6*EI*beamLength))*(
                    beamLength**2-positions[i]**2-(beamLength-loadPosition)**2)
                posDeflection.append(-y)

            else:
                y = ((loadForce*loadPosition*(beamLength - positions[i])) / (6*EI*beamLength))*(
                    beamLength**2-(beamLength-positions[i])**2-loadPosition**2)
                posDeflection.append(-y)

        elif beamSupport == "Cantilever":
            if positions[i] < loadPosition:
                y = ((loadForce*(positions[i]**2)) /
                     (6*EI)) * (3*loadPosition - positions[i])
                posDeflection.append(-y)

            else:
                y = ((loadForce*(loadPosition**2)) / (6*EI)) * \
                    (3*positions[i] - loadPosition)
                posDeflection.append(-y)

    return posDeflection


# Function for computing the deflection of a beam at given positions when it is affected by multiple loads at once.
def beamSuperposition(positions, beamLength, loadPosition, loadForce, beamSupport):

    # If statement that makes tests if either loadForce or loadPosition are empty.
    # If this is the case the function return a zero vector of same length as positions.
    if len(loadPosition) == 0 or len(loadForce) == 0:
        return np.zeros(len(positions))

    beamDef = []

    # For loop iterating over each load and its given position.
    # In the loop the beamDeflection function is called and the computed deflection is appended to beamDef.
    for i in range(len(loadForce)):
        deflection = beamDeflection(
            positions, beamLength, loadPosition[i], loadForce[i], beamSupport)
        beamDef.append(deflection)

    totalDeflection = []

    # For loop iterating over each position and sum up the deflections for each load.
    # The result is appended to totalDeflection.
    for j in range(len(positions)):
        positionDef = []
        for i in range(len(beamDef)):
            positionDef.append(beamDef[i][j])
        totalDeflection.append(sum(positionDef))

    # A list of the same length as the input is returned.
    return totalDeflection

# Function for plotting a beam with the given loads.


def beamPlot(beamLength, loadPosition, loadForce, beamSupport):

    global x, y

    # If/else statement differentiating between the beamsupport and the amount of loads.
    if len(loadPosition) == 1:

        if beamSupport == "Both":

            plt.title("Beam deflection")

            x = np.arange(beamLength+1)
            y = beamSuperposition(
                x, beamLength, loadPosition, loadForce, beamSupport)

            # Making sure only the interval of the beam is displayed using beamLength.
            plt.xlim(0, beamLength)
            # Using autoscale to make sure the whole graph is displayed.
            plt.autoscale(enable=True, axis='y')

            # A list of all the loads. Using markevery to display all loads on the graph.
            loads = [loadPosition]
            plt.plot(x, y, '-bD', markevery=loads)

            # A linear graph along the x-axis to display the beam under no load.
            linearX = [0, beamLength]
            linearY = [0, 0]
            # The '--' makes the line dotted and 'g' makes the graph green.
            plt.plot(linearX, linearY, '--g')

            print(variables)
            plt.show()

        elif beamSupport == "Cantilever":

            plt.title("Beam deflection")

            x = np.arange(beamLength+1)
            y = beamSuperposition(
                x, beamLength, loadPosition, loadForce, beamSupport)

            plt.xlim(0, beamLength)
            plt.autoscale(enable=True, axis='y')

            loads = [loadPosition]
            plt.plot(x, y, '-bD', markevery=loads)

            linearX = [0, beamLength]
            linearY = [0, 0]
            plt.plot(linearX, linearY, '--g')

            print(variables)
            plt.show()

    if len(loadPosition) > 1:

        if beamSupport == "Cantilever":

            plt.title("Beam deflection")

            x = np.arange(beamLength+1)
            y = beamSuperposition(
                x, beamLength, loadPosition, loadForce, beamSupport)

            plt.xlim(0, beamLength)
            plt.autoscale(enable=True, axis='y')

            loads = [loadPosition]
            plt.plot(x, y, '-bD', markevery=loads)

            linearX = [0, beamLength]
            linearY = [0, 0]
            plt.plot(linearX, linearY, '--g')

            print(variables)
            plt.show()

        elif beamSupport == "Both":

            plt.title("Beam deflection")

            x = np.arange(beamLength+1)
            y = beamSuperposition(
                x, beamLength, loadPosition, loadForce, beamSupport)

            plt.xlim(0, beamLength)
            plt.autoscale(enable=True, axis='y')

            loads = [loadPosition]
            plt.plot(x, y, '-bD', markevery=loads)

            linearX = [0, beamLength]
            linearY = [0, 0]
            plt.plot(linearX, linearY, '--g')

            print(variables)
            plt.show()

# Pythology 1.0.3 Documentation

## 1 - Introduction

Pythology is a scientific python package with the purpose of simplifying the implementation
of epidemiological compartmental models.

Using object-oriented concepts, users can build each compartment and each transfer rate between compartments
in a much more high-level way than implementing the model by hand, only needing to specify each of these elements' characteristics.

Thus, the package aims to eliminate the need for advanced mathematical 
knowledge and allow the user to focus more on the conceptual and biological aspect with freedom
to explore more model and parameter possibilities.

Please keep in mind Pythology is still in early development. There are still a lot of features
to implement and bugs to fix. Planned features can be found at the bottom of this document.

## 2 - Usage

This session's objective is to both explain the conceptual building of this package and to provide a simple quickstart application of the simplest form 
of compartmental models: the SIR (Susceptible, Infected and Recovered) model.

![SIR model][logo]

[logo]: sir.png "SIR model"

The package should first by installed by running `pip install pythology` on console. 
The dependencies are SciPy, NumPy and Matplotlib.

You also need to `from pythology.functions import *`.

Pythology revolves around three key concepts to construct the compartmental mode: Compartments, Flows and Models themselves.

### 2.1 - Compartments

Each compartment is one "box" of the model where one individual may be.
They are implemented through simple 1-character strings just to identify the model foundations.
Compartments should be initialized in form of a list to be fed to the model.

Example:

`compartmentlist = ['S', 'I', 'R']`

### 2.2 - Flows

**2.2.1 - Flow**

Flows are the relations between compartments that describe the dynamics of the transference of individuals from 
one compartment to another.
Flow implementation consists of the Flow class, which has the following attributes:

**origin:** The compartment from which the individuals are being transferred from.

**destiny:** The compartment to which the individuals are being transferred to.

**parameter_label:** The verbose name to be used to identify that relation inside the internal equations.
The most usual approach is to use greek letters or otherwise common variable names.

**rate:** The rate in which individuals are transferred from "origin" to "destiny". This
should be interpreted as a frequency type value. 
The easiest way to visualize this variable is to think about the inverse of how many time units the average
individual is expected to be in the origin compartment before it goes to the destiny (which is the period). 
For example: considering the infection lasts 14 days, in a Flow object describing individuals going from Infected to Recovered, the
transfer rate would be 1/14. 

**2.2.2 - MainFlow**

The MainFlow class, child of the Flow class, is designed to represent the relation between the Susceptible and Infected compartments that should exist in 
all compartmental models. This happens because the default Flow object assumes the transfer rate between compartments is only proportional
to the quantity of individuals in the origin compartment at any given moment. This is true for most relations, but the infection dynamic is different.

The speed in which individuals are infected is proportional to both the number of infected individuals and the number of infected individuals, so 
this relation should be handled specially by the MainFlow class, which automatically points to the S and I compartments that should always be present.

The MainFlow **contactrate** also has a special meaning. This parameter is known in the epidemiological modeling community as Beta.
Beta/contact rate means "The number of people that each infected person will infect per unit of time".

Usually, beta can be estimated through the basic reproduction number (R), which describes the average number of new infections generated from an initially infected individual, multiplied by Gamma, which is the inverse fraction of the average infection duration.



The flows should also be passed in the form of a list.

Initialization example:

`si = MainFlow(contactrate=1)`

 `ir = Flow(parameter_label='gamma', rate=0.5, origin='I', destiny='R')`

`flowlist = [si, ir]`

### 2.3 - CompartmentalModel

**2.3.1 - Initialization**

This class is the model itself. It's initialized by passing a list of compartments and a list of flows (compartment relations).

Model initialization example:

`mysirmodel = CompartmentalModel(compartments=compartmentlist, flows=flowlist)`

**2.3.2 - Simulation**

As of now, this class is ruled by the method build, which receives three arguments:

**population:** The number of individuals the user wishes to simulate

**initial:** The initial state of the model (How many individuals are in each compartment at time = 0). Expected to be a dictionary following the pattern "Compartment": Value. **IMPORTANT**: THE SUM OF THE INITIAL VALUES MUST BE EQUAL TO THE TOTAL POPULATION.

**time:** The time interval the user wishes to model.

It's extremely important that the units are consistent between these parameters and the units considered for the Flow rates.

The build method, given these arguments, will return one list for each of the compartments which describe the simulated number of individuals for each corresponding compartment in each unit of time.


Model initialization example:

`initial = {
    'S': 195,
    'I': 5,
    'R': 0
}`

`S, I, R = mysirmodel.build(population=200, initial=initial, time=365)`

This way, the variables S, I and R will be assigned one list each, containing 365 values (the number of individuals in that compartment each day) to be plotted and analyzed.

It's important to maintain consistent order when declaring compartments.

## 3- To be implemented

As said before, Pythology is in extremely early development stage. Some of the envisioned future features are:

* Method for plotting inside the package
* Support for contact rates varying through time
* Optimization
* Flexibilizing input structure
* Fixing bugs

Please feel free to contact me if you have any questions, suggestions or desire to help this project!


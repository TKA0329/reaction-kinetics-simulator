# Reaction Kinetics Simulator
This is a Python programme that calculates the concentrations of the reactant and product, saves the data in a CSV file, generates a table, and plots a graph of how the concentration of the reactant and product varies with time, using the given and calculated data.

## Why I built this
As an aspiring Chemical and Biomolecular Engineer, I am interested to see how the Chemistry concepts I learnt at school can be brought to life by building a programme that can handle repetitive inputs. As someone with no prior programming experience, I built this on my own from scratch, after about 3 weeks of learning Python intensively. It is not perfect, but I am proud of my progress, and I am eager to improve. This project is a work in progress. Moving forward, as I learn more about Python, I plan to incorporate more features into the programme, while trimming down some parts to avoid repetition and reduce the risks of potential bugs.

## Features
- calculates a rate constant using the Arrhenius equation
- supports zero-, first- and second-order reactions
- supports saving both the given data and the calculated data into a CSV file, while generating a table to document the relevant data.
- is capable of generating a graph in 3 formats: PDF, PNG and JPEG

## How to use this programme?
This programme assumes that the temperature is constant, and the units used are seconds and mol/L.
1. Input the relevant frequency factor, activation energy and temperature to calculate the rate constant.
If sys.argv[1] is empty, a default CSV file will be used.
2. Input the initial concentration of the reactant, the reaction order, as well as the number of times the user wants to calculate the reactant's concentration.
If the inputs are invalid, the user will be reprompted for a set of valid inputs.
3. Input the time values of the reaction. For instance, for a reaction with an interval of 200s, the times could be 0, 200, 400 and so on. If the inputs are invalid, the user will be prompted again until a valid input is received.
4. Once the calculations are done, a sentence regarding the half-life of the reaction will be stated, alongside a table with the headings: time(s), concentration of reactant(mol/L), and concentration of product(mol/L).
5. The user will then be prompted for the title for which they want to name the graph, as well as the file's name and the file's format, which only accepts PDF, png and JPEG. With that, a properly labelled graph is generated and the data are saved.

Some samples of the graphs generated: (https://drive.google.com/drive/folders/1Vhe8V8c9KmGvfA_JP0MLKLOfKnfmXZSh?usp=drive_link)

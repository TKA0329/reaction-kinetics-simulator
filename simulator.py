import math
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import csv
import sys
import re

#Find the rate constant(k)
def temperature():
    while True:
        try:
            A = float(input("A (frequency factor): "))
            Ea = float(input("Activation energy in J/mol: "))
            R = 8.31
            T = float(input("Temperature in Kelvin: "))
            #making sure the user enters a valid value
            while True:
                if A <= 0 or Ea <= 0 or T <= 0:
                    print("A, Ea, k and T cannot be a negative value! Please try again.")
                else:
                    k = A*math.exp(-Ea/(R*T))
                    print(f"for T = {T}K, k = {k:.6f}")
                    return k
                break
        except ValueError:
            print("Invalid. Please try again.")

def main():
    k = temperature()
    #asking for the initial concentration, order of reaction and number of times
    while True:
        if len(sys.argv) < 2:
            print("No output filename given. Using default: Output.csv")
            sys.argv.append("Output.csv")
        if not sys.argv[1].endswith(".csv"):
            sys.argv[1] += ".csv"

        else:
            try:
                A0 = float(input("Initial concentration (mol/L): "))
                order_list = {"zero", "first", "second"}
                order = input("Order of reaction (zero, first, or second): ").lower().strip()
                n = int(input("Number of times to calculate concentration: "))
                #making sure the user enters a valid value
                if order not in order_list:
                    print("Please choose from: zero, first, or second.")
                    continue
                if A0 <= 0 or n <= 0:
                    print("A0 and n cannot be a negative value!")
                    continue
                break
            except ValueError:
                print("Please enter a valid value.")
    graph(k, A0, order, n)
    file_format_name()

def graph(k, A0, order, n):
    #writing the header for the CSV file
    fieldnames=["time(s)", "concentration of reactant(mol/L)", "concentration of product(mol/L)"]
    with open(sys.argv[1], "w") as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
    #calculating the concentrations based on what was given above
    Reactant_concentration = []
    Product_concentration = []
    time = []
    if order == "second":
        for _ in range(n):
            while True:
                try:
                    t = float(input("Time: "))
                    if t < 0:
                        print("Time cannot be less than 0! Please try again!")
                    else:
                        break
                except ValueError:
                    print("Invalid! Please enter a number.")
                    continue
            time.append(t)
            inverse_R = 1/A0 + k*t
            R_concentration = 1/inverse_R
            Reactant_concentration.append(round(R_concentration, 3))
            P_concentration = A0 - R_concentration
            Product_concentration.append(round(P_concentration, 3))
            print(f'[A] = {R_concentration:.3f}mol/L')
            print(f'[B] = {P_concentration:.3f}mol/L')
            #incorporating the values calculated into the CSV file
            with open(sys.argv[1], "a") as file:
                writer = csv.DictWriter(file, fieldnames)
                writer.writerow({"time(s)": t, "concentration of reactant(mol/L)": round(R_concentration, 3), "concentration of product(mol/L)": round(P_concentration, 3)})
        print("The half-life of second order reactions increases as the reactant's concentration decreases.")

    elif order == "first":
        for _ in range(n):
            while True:
                try:
                    t = float(input("Time: "))
                    if t < 0:
                        print("Time cannot be less than 0! Please try again!")
                    else:
                        break
                except ValueError:
                    print("Invalid! Please enter a number.")
                    continue
            time.append(t)
            R_concentration = A0*math.exp(-k*t)
            Reactant_concentration.append(round(R_concentration, 3))
            P_concentration = A0 - A0*math.exp(-k*t)
            Product_concentration.append(round(P_concentration, 3))
            print(f'[A] = {R_concentration:.3f}mol/L')
            print(f'[B] = {P_concentration:.3f}mol/L')

            with open(sys.argv[1], "a") as file:
                writer = csv.DictWriter(file, fieldnames)
                writer.writerow({"time(s)": t, "concentration of reactant(mol/L)": round(R_concentration, 3), "concentration of product(mol/L)": round(P_concentration, 3)})
        half_life = math.log(2)/k
        print(f"Since the half-life of first-order reactions is constant, half-life = {half_life}s")

    elif order == "zero":
        count = 0
        while count < n:
            while True:
                try:
                    t = float(input("Time: "))
                    if t < 0:
                        print("Time cannot be less than 0! Please try again!")
                    else:
                        break
                except ValueError:
                    print("Invalid! Please enter a number.")
                    continue
            R_concentration = A0 - k*t
            if R_concentration < 0:
                print("Concentration cannot be a negative value. Please use a smaller time!")
                continue
            else:
                count += 1
                time.append(t)
                Reactant_concentration.append(round(R_concentration, 3))
                P_concentration = A0 - (A0 - k*t)
                Product_concentration.append(round(P_concentration, 3))
                print(f'[A] = {(R_concentration):.3f}mol/L')
                print(f'[B] = {P_concentration:.3f}mol/L')

                with open(sys.argv[1], "a") as file:
                    writer = csv.DictWriter(file, fieldnames)
                    writer.writerow({"time(s)": t, "concentration of reactant(mol/L)": round(R_concentration, 3), "concentration of product(mol/L)": round(P_concentration, 3)})
        print("The half-life of zero order reactions decreases as the reactant's concentration decreases.")

    #formatting the data into a table
    table= []
    headers = "keys"
    with open(sys.argv[1], "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            table.append({"time(s)": row["time(s)"], "concentration of reactant(mol/L)":row["concentration of reactant(mol/L)"], "concentration of product(mol/L)": row["concentration of product(mol/L)"]})
        print(tabulate(table, headers, tablefmt="grid"))

    #plotting the graph
    y = np.array(Reactant_concentration)
    plt.plot(time, y, marker='o', linestyle='-', color = "r", label='reactant')
    plt.plot(time, Product_concentration, marker='*', linestyle="-", color = "b", label='product')
    plt.xlabel("time(s)")
    plt.ylabel("Concentration(mol/L)")
    plot_title = input("Graph's title: ")
    plt.title(f"{plot_title}")
    plt.grid(True)
    plt.legend()
    #saving the file according to the user's desired file format

def file_format_name():
    while True:
        file_name = input("File name: ")
        if re.fullmatch(r"[\w_()]+", file_name):
            file_format = input("File format (pdf/png/jpeg): ").lower().strip()
            valid_formats = {"pdf", "png", "jpeg"}
            if file_format not in valid_formats:
                print("Invalid format! Please try again.")
            else:
                plt.savefig(f"{file_name}.{file_format}")
                print(f"plot saved as {file_name}.{file_format}")
                print("All done! Your data and plot are successfully saved!")
                break
        else:
            print("Please enter a valid file name! Only alphabets, numbers, _ and () are allowed.")

if __name__ == '__main__':
    main()

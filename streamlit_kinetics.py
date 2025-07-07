import streamlit as st
from matplotlib.animation import FuncAnimation
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io


def type_of_calculation():
    st.subheader("Calculating the Rate Constant")
    def get_k():
        calculate_k = st.selectbox("How would you like to calculate k? (Rate and concentration/Arrhenius equation)?", ["---Please select---", "Rate and concentration", "Arrhenius equation"])
        if calculate_k == "Arrhenius equation":
            A = st.number_input("A (frequency factor):", min_value=0.0)
            Ea = st.number_input("Ea (activation energy in J/mol):", min_value=0.0)
            T = st.number_input("Temperature (K):", min_value = 0.0)
            R = 8.31
            k = None
            if st.button("Calculate rate constant"):
                if T == 0:
                    st.warning("Temperature cannot be zero!")
                else:
                    k = A * math.exp(-Ea / (R * T))
                    st.session_state.k = k
                    st.success(f"Rate constant = {st.session_state.k:.6f}")
            if "k" in st.session_state:
                st.info(f"Rate constant = {st.session_state.k:.6f}")
            return k
        if calculate_k == "Rate and concentration":
            k = None
            rate_str = st.text_input("Rate in molL⁻¹s⁻¹: ")
            try:
                rate = float(rate_str)
            except ValueError:
                st.warning("Please enter a valid number! ")
                return
            concentration = st.number_input("Concentration: ", min_value=0.0000)
            if rate <= 0 or concentration <=0:
                st.warning("Rate and concentration cannot be less than 0!")
                return
            order_selected = st.selectbox("Order with respect to the substance? Please select from the following:", ["---Please select---", 0.0, 1.0, 2.0])
            if order_selected == "---Please select---":
                return
            k = rate/(concentration ** order_selected)
            st.session_state.k = k


            if "k" in st.session_state:
                st.info(f"Rate constant = {st.session_state.k:.6f}")
            return k


    def get_conc():
        st.subheader("Information for Plotting Graph")
        range_or_data = st.selectbox("Plot graph using manually inputted data or auto-generated time values based on the range given?",
                                        ["---Please select---", "Manually inputted data (download and animation available!)", "Auto-generate time values based on range given"])
        k = st.session_state.get("k", None)
        A0 = st.number_input("Initial concentration (mol/L):", min_value=0.0)
        order = st.selectbox("Order of Reaction:", ["---Please select---", "Zero", "First", "Second"])
        if order == "---Please select---":
            st.warning("Please select an order!")
            return
        else:
            st.info(f"Order selected: {order} Order")
        st.markdown("##### Product's Information")
        number_of_products = st.number_input("How many products in this reaction?", key = "h")
        product_names = []
        name_of_reactant = st.text_input("The name for the reactant: ")
        for i in range(int(number_of_products)): #storing names of product in a list for accessing later
            product_name = st.text_input(f"Name of product{i+1}: ", key = f"product{i}")
            product_names.append(product_name)
        ratios = [] #each product gets its own ratio #using a list allows each ratio to be accessed using [i]
        for i in range(int(number_of_products)): #the first loop has already finished running, so a 2nd one is needed to perform a diff task
            ratio = st.number_input(f"What is the ratio of {product_names[i]} to the reactant?", min_value = 0.0, key=f"l{i}")
            ratios.append(ratio)
        #displaying the equation for the reaction
        products_info = "+".join(f"{ratios[i]}{product_names[i]}" for i in range(int(number_of_products))) #list comprehension, no need for "appending" to another list
        st.info(f"Your reaction is: \n {name_of_reactant} --> {products_info}")
        if range_or_data == "Auto-generate time values based on range given":
            if k is None:
                st.warning("Please calculate rate constant first!")
                return
            fig,ax = plt.subplots(figsize = (12,6))
            time_min = st.number_input("Minimum time:", min_value = 0.0)
            time_max = st.number_input("Maximum time", min_value = 0.0)
            num_points = 100
            times = np.linspace(time_min, time_max, num_points)
            plt.figure(figsize=(12,6))
            if order == "Second":
                inverse_R = 1/A0 + k*times
                R_concentration = 1/inverse_R
            elif order == "First":
                R_concentration = A0*np.exp(-k*times)
            elif order == "Zero":
                R_concentration = A0 - k*times
            ax.plot(times, R_concentration, label = f"{name_of_reactant}")
            for i in range(int(number_of_products)):
                P_concentration = (A0 - R_concentration)*ratios[i] #indexing into the list of ratios created
                ax.plot(times, P_concentration, label = f"{product_names[i]}")
            st.subheader("Concentration Vs. Time Graph")
            ax.set_xlabel("time(s)")
            ax.set_ylabel("Concentration(mol/L)")
            plot_title = st.text_input("Graph's title: ")
            ax.set_title(f"{plot_title}")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
       
        if range_or_data == "Manually inputted data (download and animation available!)":
            st.markdown("##### Fill in Time Values to Calculate Concentrations")
            n = st.number_input("Number of times to calculate concentration:", min_value=1.0)
            time  = []
            R_conc = []
            P_conc= [[] for _ in range(int(number_of_products))] #creates a LIST of empty lists
            if k is not None:
                for i in range(int(n)):
                    t = st.number_input(f"Time: {i+1}", min_value=0.0, key=f"time_{i}")
                    if order == "Second":
                        if A0 == 0:
                            st.warning("Initial Concentration cannot be zero! ")
                            break
                        else:
                            inverse_R = 1/A0 + k*t
                            R_concentration = 1/inverse_R
                    elif order == "First":
                        R_concentration = A0*math.exp(-k*t)
                    if order == "Zero":
                        R_concentration = A0 - k*t
                        if R_concentration < 0:
                            st.warning("Reactant's concentration cannot be less than 0!")
                            continue
                    time.append(round(t, 3))
                    st.success(f"[{name_of_reactant}] = {R_concentration:.3f}mol/L")
                    R_conc.append(round(R_concentration,3))
                    for j in range(int(number_of_products)):
                        P_concentration = (A0 - R_concentration)*ratios[j]
                        st.success(f"[{product_names[j]}] = {P_concentration:.3f}mol/L")
                        P_conc[j].append(round(P_concentration, 3))
            else:
                st.warning("Please calculate rate constant first!")
            if order == "Second":
                st.write("The half-life of second order reactions increases as the reactant's concentration decreases.")
            elif order == "First":
                if k is not None:
                    half_life = math.log(2)/k
                    st.write(f"Since the half-life of first-order reactions is constant, half-life = {half_life}s")
                else:
                    return
            elif order == "Zero":
                st.write("The half-life of zero order reactions decreases as the reactant's concentration decreases.")


            st.subheader("Time-Concentration Data (Manual Input)")
           
            data = {"time (s)": (time),
            f"Concentration of {name_of_reactant} (mol/L)": (R_conc)}
            for j in range(int(number_of_products)):
                data[f"Concentration of {product_names[j]} (mol/L)"] = (P_conc[j])
            st.dataframe(data) #need to create a dictionary and add the information for products to the dictionary.
       
            st.subheader("Concentration Vs. Time Graph")
            style = st.selectbox("Animated or static?", ["---Please select---", "Static","Animated"])
            if style == "Static":
                fig, ax = plt.subplots()
                y = np.array(R_conc)
                ax.plot(time, y, marker="o", linestyle="-", color = "r", label=f"{name_of_reactant}")
                for j in range(int(number_of_products)):
                    ax.plot(time, P_conc[j], marker="*", linestyle="-", label=f"{product_names[j]}") #automatically assigns a colour
                ax.set_xlabel("time(s)")
                ax.set_ylabel("Concentration(mol/L)")
                plot_title = st.text_input("Graph's title: ")
                ax.set_title(f"{plot_title}")
                ax.grid(True)
                ax.legend()
                st.pyplot(fig)


                st.subheader("Download File")
                format = st.selectbox("File Format:", ["---Please select---", "png", "jpeg", "pdf"])
                if format != "---Please select---":
                    buf = io.BytesIO()
                    fig.savefig(buf, format = format)
                    buf.seek(0)
                else:
                    st.warning("Please select a file format to proceed.")
                    return


                file_name = st.text_input("File name: ", value = f"kinetics_plot.{format}")
                if format == "png" or format == "jpeg":
                    st.download_button(label = "Download image", data = buf, file_name = f"{file_name}", mime=f"image/{format}")
                elif format == "pdf":
                    st.download_button(label = "Download image", data = buf, file_name = f"{file_name}", mime="application/pdf")
   
            elif style == "Animated":
                if not time:
                    return
                else:
                    fig, ax = plt.subplots()
                    x_min = min(time)
                    x_max = max(time)
                    flattened_P_conc = [] #do this bcz P_conc is a list of lists, need to access the items within each of the list
                    for sublist in P_conc:
                        for value in sublist: #then flatten it
                            flattened_P_conc.append(value) #shorter version: R_conc + [value for sublist in P_conc for value in sublist]
                    flattened_y = R_conc + flattened_P_conc
                    y_min = min(flattened_y)
                    y_max = max(flattened_y)
                    ax.set_xlim(x_min, x_max)
                    ax.set_ylim(y_min, y_max)
                    line1, = ax.plot([], [], lw = 2, marker="o", linestyle="-", color = "r", label=f"{name_of_reactant}")
                    lines_of_product = []
                    for j in range(int(number_of_products)):
                        line, = ax.plot([], [], lw = 2, marker="*", linestyle="-", label=f"{product_names[j]}")
                        lines_of_product.append(line)
                    ax.set_xlabel("time(s)")
                    ax.set_ylabel("Concentration(mol/L)")
                    plot_title = st.text_input("Graph's title: ")
                    ax.set_title(f"{plot_title}")
                    ax.grid(True)
                    ax.legend()


                    def init():
                        line1.set_data([], [])
                        for j in range(int(number_of_products)):
                            lines_of_product[j].set_data([], [])
                        return [line1] + lines_of_product


                    def animate(i):
                        x = time[:i+1]
                        y2 = R_conc[:i+1]
                        line1.set_data(x, y2)
                        for j in range(int(number_of_products)):
                            y1 = P_conc[j][:i+1]
                            lines_of_product[j].set_data(x, y1)
                        return [line1] + lines_of_product


                    anim = FuncAnimation(fig, animate,
                                init_func = init,
                                frames = len(time),
                                interval = 1000,
                                blit = True)


                    anim.save("Kinetics_animation.gif",
                    writer = "pillow", fps = 2)
                    st.image("Kinetics_animation.gif", caption="Kinetics Animation!")
            else:
                return
    def helper():
        get_k()
        get_conc()
    helper()


def main():
    type_of_calculation()


main()






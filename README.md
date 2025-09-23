# Reaction Kinetics Simulator
An interactive web app for visualising chemical reaction kinetics using Streamlit

Inspired by *Solen and Harb’s Introduction to Chemical Engineering*, with close attention to maintain accuracy

This was my first major Python project. I started learning Python in May 2025, and by July I had built this simulator. I’ve since kept refining it.

## Functions:
1. Calculate rate constant (k) using:
    - Rate & concentration
    - Arrhenius equation
2. Input or auto-generate time values 
3. Quickly visualise concentration vs. time graphs for reactants and products
4. Choose between:
    - Static plots
    - Animated GIFs
    - Export / download graphs in PNG, JPEG, or PDF

## Features:
1. Adapts to zero, first, or second-order kinetics
2. Supports different ratios for reactant + product 
    - ⚠️ currently does not support multi-reactant reactions
3. Supports multiple products simulation 
4. Animation using matplotlib.animation.FuncAnimation

## Files:
1. streamlit_kinetics.py: current version with streamlit
2. simulator.py: older, simpler version without streamlit

## Deployment
1. [Streamlit Link](https://reaction-kinetics-simulator-2vwkv6rjcwqqtmcf2nc943.streamlit.app/)
    - Note: If the Streamlit app link shows “This app has gone to sleep,” which can happen in just a couple of days of inactivity, just click “Get this app back up” and it should restart in a few seconds.

## Main libraries/tech used: 
Python · Streamlit · Pandas · Matplotlib · NumPy · CSV · Os

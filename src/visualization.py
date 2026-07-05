import numpy as np 
import matplotlib.pyplot as plt 
 
from src.functions import loss_function 
 
 
def show_loss_graph(): 
    x = np.linspace(-2, 8, 300) 
    y = loss_function(x) 
 
    plt.figure(figsize=(8, 5)) 
    plt.plot(x, y) 
 
    plt.title("Loss Function") 
    plt.xlabel("x") 
    plt.ylabel("loss") 
    plt.grid(True) 
 
    plt.show() 
 
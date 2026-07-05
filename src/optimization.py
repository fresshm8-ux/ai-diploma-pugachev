from src.functions import loss_function 
from src.derivatives import loss_derivative 
 
 
def gradient_descent(start_x, learning_rate, steps): 
    x_current = start_x 
    history = [] 
 
    for step in range(steps): 
        current_loss = loss_function(x_current) 
        current_derivative = loss_derivative(x_current) 
 
        history.append({ 
            "step": step, 
            "x": x_current, 
            "loss": current_loss, 
            "derivative": current_derivative 
        }) 
 
        x_current = x_current - learning_rate * current_derivative 
 
    return history 
 
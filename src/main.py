import pandas as pd 
 
from src.functions import loss_function 
from src.derivatives import loss_derivative 
from src.optimization import gradient_descent 
from src.visualization import show_loss_graph 
from src.report_utils import save_report 
 
 
def main(): 
    print("СТАРТ ПРОЕКТА") 
 
    show_loss_graph() 
 
    history = gradient_descent( 
        start_x=-2, 
        learning_rate=0.2, 
        steps=20 
    ) 
 
    history_df = pd.DataFrame(history) 
 
    print(history_df) 
 
    final_x = history_df["x"].iloc[-1] 
    final_loss = history_df["loss"].iloc[-1] 
 
    report = f""" 
Project: Math Optimization Project 
 
Final x: {final_x} 
Final loss: {final_loss} 
""" 
 
    save_report(report, "data/project_report.txt") 
 
    print("ОТЧЁТ СОХРАНЁН") 
 
 
if __name__ == "__main__": 
    main() 
 
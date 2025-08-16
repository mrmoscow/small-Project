import pandas as pd
import numpy as np

def calc_y_trx_model(Phot, Pcold, Thot=296, Tcold=77):
    """
    Calculate Y-factor, Trx, Pgap, and Non, and return the DataFrame and polyfit model.

    Parameters:
        Phot (list or array): Hot load power values.
        Pcold (list or array): Cold load power values (must have the same length as Phot).
        Thot (float, optional): Hot load temperature in Kelvin. Default is 296.
        Tcold (float, optional): Cold load temperature in Kelvin. Default is 77.

    Returns:
        tuple:
            - DataFrame: Contains Phot, Pcold, Thot, Tcold, Yfact, Trx, Pgap, and Non.
            - numpy.ndarray: Polyfit model coefficients [slope, intercept].
    """
    df2 = pd.DataFrame({
        "Phot": Phot,
        "Pcold": Pcold,
        "Thot": Thot,
        "Tcold": Tcold,
    })

    df2['Yfact'] = df2['Phot'] / df2['Pcold']
    df2['Trx'] = (df2['Thot'] - df2['Tcold'] * df2['Yfact']) / (df2['Yfact'] - 1)
    df2['Pgap'] = df2['Phot'] - df2['Pcold']
    #df2['Non'] = df2.loc[0, 'Pgap'] / df2['Pgap']
    #df2['Non'] = df2['Pgap'] / df2['Pgap'].max()
    df2['Non'] =df2['Pgap'].max()/df2['Pgap']
    #df2['Non']=df2['Pgap']/df2['Phot'].max()

    model = np.polyfit(df2['Non'], df2['Trx'], 1)
    return df2, model

# Example usage
#Phot_data= [182,156.3,128.0,98,70.5,60.2,52.4,34.1,12.06]
#Pcold_data= [108,91.3,77.9,52.9,38.2,33.3,29.7,20.8,9.5]

#Phot_data= [70.5,60.2,52.4,34.1,12.06]
#Pcold_data= [38.2,33.3,29.7,20.8,9.5]

#Phot_data = [287.078, 274.789, 247.742, 198.153, 221.82, 175.792, 131.22, 42.953]
#Pcold_data = [119.124, 114.551, 117.49, 101.391, 91.833, 77.624, 68.0769, 24.49]
Phot_data = [3.17,3.79,5.4,6.10,4.97]
Pcold_data = [2.91,3.155,3.72,3.981,3.589]


df_result, model_result = calc_y_trx_model(Phot_data, Pcold_data,294.0,78.5)

print(df_result)
print("Polyfit model:", model_result)
print("Tx is",model_result[1])
# the Tx =model_result[1], 2nd return.

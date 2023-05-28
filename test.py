import numpy as np
import pandas as pd

print ("Test the")


arr = np.array( [[ 1, 2, 3],[ 4, 2, 5]] )

# Printing type of arr object
print("Array is of type: ", type(arr))

# Printing array dimensions (axes)
print("No. of dimensions: ", arr.ndim)

# Printing shape of array
print("Shape of array: ", arr.shape)

# Printing size (total number of elements) of array
print("Size of array: ", arr.size)

# Printing type of elements in array
print("Array stores elements of type: ", arr.dtype)



s = pd.Series([1, 3, 5, np.nan, 6, 8])
dates = pd.date_range("20130101", periods=6)

print(s)
print(dates)


df=pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df)

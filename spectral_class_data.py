from vpython import *


# Lists go temperature(K), Luminosity (Solar luminosities), Approximate Peak Wavelength color (broad strokes for now)
# based on values for X5 V
spectral_class_dict = {
   "O": [54000, 846000, color.blue],
   "B": [15200, 360, color.blue],
   "A": [8310, 9, color.yellow],
   "F": [6700, 2.4, color.yellow],
   "G": [5600, 0.86, color.orange],
   "K": [4400, 0.19, color.red],
   "M": [3200, 0.026, color.red],
}
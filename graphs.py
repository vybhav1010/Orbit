from vpython import *
import math

sbc = 5.67e-8 #Stefan-Boltzmann constant
h = 6.626e-34
c = 299792458
k_b = 1.380649e-23
solar_radius = 40
true_solar_radius = 6.957e8 # m

solar_luminosity = 3.83e26 # W
solar_temperature = 5800 # K

def create_graphs(T):
      global blackbody_graph
      global T_key
      blackbody_graph = graph(width=400, height=200, background=color.white, foreground=color.black,
      xtitle="Wavelength (m)", ytitle="Intensity (W/m^2)", title=f"Black Body Radiation at {round(T)} K")
      T_key = graph(height=100, ymin=0, ymax=1, background=color.white, foreground=color.black,
      xtitle="Planetary Temperature (K)")

def black_body_graph(T):
  plot = gcurve(color=color.red, graph=blackbody_graph)
  def planck_function(wavelength, T):
      try:
        return (2 * h * math.pow(c,2))/math.pow(wavelength, 5) * 1/(math.exp((h * c)/(wavelength * k_b * T)) - 1)

      except OverflowError:
        print(wavelength, T)
        return 0
  for i in range(1,5000):
      wavelength = i * 1e-9
      intensity = planck_function(wavelength, T)
      plot.plot(data=(wavelength, intensity))

def graph_temp_mapping():
  line_break = wtext(text="")
  def get_color(temp):
      red_value = 1/(1+math.exp(-temp/400))
      return vec(red_value, 1-red_value, 1-red_value)
  
  for i in range(1000):
      bars = gvbars(data=[(i,1)], color=get_color(i), graph=T_key)

def delete_graphs():
      blackbody_graph.delete()
      T_key.delete()  


        
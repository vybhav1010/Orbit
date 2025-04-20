from vpython import *
import math
from spectral_class_data import spectral_class_dict
from graphs import create_graphs, black_body_graph, graph_temp_mapping, delete_graphs


solar_luminosity = 3.83e26 # W
solar_temperature = 5800 # K



class Widget:

  def __init__(self):
     self.au = 750

     self.dist = 0
     self.e = 0
     self.size = 0
     self.theta = 0
     self.albedo = 0
     self.stellar_parameters = [solar_temperature, solar_luminosity, color.yellow]

     self.sliders = []
     

  def create_widget(self):
      dist = 0

      def dummy():
          return  

      test_slider = slider(bind=dummy, min=0.1, max=1)

      slider_type = type(test_slider)

      test_slider.delete()

      def p_dst(evt=None):
        dmax = 10
        dmin = 0.1
        if type(evt) == slider_type:
          dtext.text = f" distance: {distance_slider.value} AU \n"
        else:
          if evt.number <= dmax and evt.number >= dmin:
              dtext.text = f" distance: {evt.number} AU \n"
              distance_slider.value = evt.number
          else:
              dtext.text = f" distance: {distance_slider.value} AU \n"
              return

      def p_e(evt=None):
        emax = 5
        emin = 0
        if type(evt) == slider_type:
          etext.text = f" eccentricity: {e_slider.value} \n"
        else:
          if evt.number <= emax and evt.number >= emin:
              etext.text = f" eccentricity: {evt.number} \n"
              e_slider.value = evt.number
          else:
              etext.text = f" eccentricity: {e_slider.value} \n"
              return

      def p_size(evt=None):
          smax = 10
          smin = 0
          if type(evt) == slider_type:
            stext.text = f" size: {size_slider.value} \n"
          else:
            if evt.number <= smax and evt.number >= smin:
                stext.text = f" size: {evt.number} \n"
                size_slider.value = evt.number
            else:
                stext.text = f" size: {size_slider.value} \n"
                return

      def p_theta(evt=None):
          tmin = 0
          tmax = 2*math.pi
          if type(evt) == slider_type:   
              ttext.text = f" theta: {round(theta_slider.value/math.pi, 2)}π \n"
          else:
              if evt.number <= tmax and evt.number >= tmin:
                ttext.text = f" theta: {round(evt.number/math.pi, 2)}π \n"
                theta_slider.value = evt.number
              else:
                ttext.text = f" theta: {round(theta_slider.value/math.pi, 2)}π \n"
                return

      def p_albedo(evt=None):
          amax = 1
          amin = 0.1
          if type(evt) == slider_type:
              atext.text = f" albedo: {albedo_slider.value} \n"
          else:
              if evt.number <= amax and evt.number >= amin:
                atext.text = f" albedo: {evt.number} \n"
                albedo_slider.value = evt.number
              else:    
                atext.text = f" albedo: {albedo_slider.value} \n"
                return

      choice_list = ["Pick Class(Defaults to Sun)", 'O', 'B', 'A', 'F', 'G', 'K', 'M']

      def change_spectral_class(evt):
          if evt.index < 1:
            pass
          else:
          #   print(evt.index)
            index = evt.index
            spectral_class = choice_list[index]
            color = spectral_class_dict[spectral_class][2]
            luminosity = spectral_class_dict[spectral_class][1] * solar_luminosity
            stellar_temp = spectral_class_dict[spectral_class][0]

            delete_graphs()               

            create_graphs(stellar_temp)


            graph_temp_mapping()  
            black_body_graph(stellar_temp)


            self.stellar_parameters = [stellar_temp, luminosity, color]

          
      distance_slider = slider(bind=p_dst,min=0.1, max=10)
      dbox = winput(bind=p_dst, type='numeric')
      dtext = wtext(text=f" distance: {distance_slider.value} AU \n")
      dist = dist * self.au

      e_slider = slider(bind=p_e,min=0, max=5)
      ebox = winput(bind=p_e, type='numeric')
      etext = wtext(text=f" eccentriity: {e_slider.value} \n")


      size_slider = slider(bind=p_size,min=0, max=10)
      sbox = winput(bind=p_size, type='numeric')
      stext = wtext(text=f" size: {size_slider.value} (not indicative of mass)\n")
      

      theta_slider = slider(bind=p_theta,min=0, max=2*math.pi)
      tbox = winput(bind=p_theta, type='numeric')
      ttext = wtext(text=f" theta: {round(theta_slider.value/math.pi,2)}π \n")
        

      albedo_slider = slider(bind=p_albedo, min=0.1, max=1)
      abox = winput(bind=p_albedo, type='numeric')
      atext = wtext(text=f" albedo: {albedo_slider.value} \n")

      spectral_class_menu = menu(choices=choice_list, bind=change_spectral_class)
      wtext(text="\n")


      self.dist = distance_slider.value * self.au
      self.e = e_slider.value
      self.size = size_slider.value
      self.theta = theta_slider.value
      self.albedo = albedo_slider.value

      self.sliders = [distance_slider, e_slider, size_slider, theta_slider, albedo_slider]

  def update_values(self):
    
      self.dist = self.sliders[0].value * self.au
      self.e = self.sliders[1].value
      self.size = self.sliders[2].value
      self.theta = self.sliders[3].value
      self.albedo = self.sliders[4].value

  def return_user_input(self):
     self.update_values()

     return [self.dist, self.e, self.size, self.theta, self.albedo]
  
  def get_stellar_parameters(self):
     return self.stellar_parameters
  





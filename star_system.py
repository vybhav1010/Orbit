from vpython import *
from graphs import create_graphs, black_body_graph, graph_temp_mapping, delete_graphs
import math
from widget import Widget

sbc = 5.67e-8 #Stefan-Boltzmann constant
h = 6.626e-34
c = 299792458
k_b = 1.380649e-23
solar_radius = 40
true_solar_radius = 6.957e8 # m

solar_luminosity = 3.83e26 # W
solar_temperature = 5800 # K

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



class StarSystem:
    
    def __init__(self, star, planets, rate_constant):
        self.au = 750
        self.running = True
        self.star = star
        self.planets = planets
        self.rate_constant = rate_constant
        self.stellar_temp = self.get_stellar_temperature()
        self.widget = Widget()


    def create_light(self):
       local_light(pos=self.star.pos + vec(0,10,0), color=color.white)
       local_light(pos=self.star.pos + vec(0,-10,0), color=color.white)

    def animate(self):

        self.widget.create_widget()
        self.create_buttons()
        self.create_light()

        wtext(text="\n \n")

        create_graphs(self.stellar_temp)
        graph_temp_mapping()
        black_body_graph(self.stellar_temp)

        for planet in self.planets:
          
            self.set_planet(planet)

        dt = 1/self.rate_constant
        time_elapsed = 0
        while True:
            rate(self.rate_constant)

            if self.running:
               for planet in self.planets:
                  self.set_star()
                  self.update_planet(planet, dt)
                  # print(self.star.pos, self.planets[0].pos)
               time_elapsed += dt

    def equilibrium_temperature(self, albedo, r):
       flux = self.star.luminosity/(4 * math.pi * math.pow(r/self.au * 1.496e11, 2)) * albedo
       temp = math.pow(flux/(sbc * 4), 1/4)  
       return temp
    
    def get_stellar_temperature(self):
       L = self.star.luminosity
       radius = (((self.star.radius)/solar_radius) * true_solar_radius)
       return math.pow(L/(4 * math.pi * math.pow(radius, 2) *  sbc), 1/4)
       

    def set_star(self):
       parameters = self.widget.get_stellar_parameters()
       self.star.color = parameters[2]
       self.stellar_temp = parameters[0]
       self.star.luminosity = parameters[1]  
       self.star.pos = vec(0,0,0) 
   
    def set_planet(self, planet):
      pos_vector = planet.pos-self.star.pos
      

      def velocity(e, theta):       
        if(e >= 0 and e < 1):
            sma = planet.sma
            v_mag_apogee = math.sqrt(self.star.mass * ((2/planet.dist) - (1/sma)))
            h = planet.dist * v_mag_apogee
            return (self.star.mass/h) * vec(sin(theta) * -1, (e+cos(theta)), 0)
        elif(e == 1):
            v_mag_apogee = math.sqrt(self.star.mass * ((2/planet.dist)))
            h = planet.dist * v_mag_apogee
            return (self.star .mass/h) * vec(sin(theta) * -1, (e+cos(theta)), 0)
        elif(e >= 1):
            sma = planet.sma
            v_mag_apogee = math.sqrt(self.star.mass * ((2/planet.dist) - (1/sma)))
            h = planet.dist * v_mag_apogee
            return (self.star.mass/h) * vec(sin(theta) * -1, (e+cos(theta)), 0)
            

      acc_planet_mag = self.star.mass/math.pow(mag(pos_vector), 2)
    
        
      theta = atan2(pos_vector.y, pos_vector.x)

      theta_orbit = atan2(pos_vector.y * -1, pos_vector.x * -1)

      planet.vel = velocity(planet.e, theta_orbit)

     
        
      planet.acc = vec(acc_planet_mag * cos(theta) * -1, acc_planet_mag * sin(theta) * -1, 0)
      planet.T = self.equilibrium_temperature(planet.albedo, mag(pos_vector)) 

      planet.make_trail = True

      red_value = 1/(1+math.exp(-planet.T/400))
      planet.color = vec(red_value, 1-red_value, 1-red_value)




    def create_buttons(self):
        def add_planet_handler():
           add_planet_final()

        def add_planet_final():
           values = self.widget.return_user_input()
           print(values)
           self.add_planet(values[0], values[1], values[2], values[3], values[4])
           

        add_button = button(text='<b>Add</b>', 
             bind=add_planet_handler, name=None)
        pause_button = button(text='<b>Pause/Play</b>', bind=self.pause_play, name=None)
   
    def pause_play(self):
      self.running  = not self.running  

    def add_planet(self, dist, e, size, theta, albedo):
      self.running = False

      print(theta)
      
      def position(e, dist, theta):
         if(e >= 0 and e < 1):
            sma = dist/(1+e)
            r = (sma * (1-math.pow(e, 2)))/(1+e * cos(theta))
            return vec(r * cos(theta) * -1, r * sin(theta) * -1, 0)
         elif(e == 1):
            r = (2 * dist)/(1+ cos(theta))
            return vec(r * cos(theta) * -1, r * sin(theta) * -1, 0)
         elif(e > 1):
            sma = dist/(1-e)
            r = (sma * (math.pow(e,2) -1))/(1+e * cos(theta))
            return vec(r * cos(theta - math.pi) * -1, r * sin(theta - math.pi) * -1, 0)
         

 

      planet = sphere(pos=position(e,dist, theta),make_trail=True, trail_type="points", interval = 100, retain=1000, radius=size, 
      dist=dist, e=e, mass=size, sma=0, albedo=albedo)

      # print(position(e,dist, theta))

      scene.center = planet.pos

      if (e>=0 and e<1):
         planet.sma = planet.dist/(1+e)
      elif(e > 1):
         planet.sma = planet.dist/(1-e)
      else:
         planet.sma=0


      self.set_planet(planet)
      self.planets.append(planet)


      self.running = True  

 
    def update_planet(self, planet, dt):
        pos_vector = planet.pos-self.star.pos

        theta = atan2(pos_vector.y, pos_vector.x)       
    
        acc_planet_mag = self.star.mass/math.pow(mag(pos_vector), 2)
        
        planet.acc = vec(acc_planet_mag * cos(theta) * -1, acc_planet_mag * sin(theta) * -1, 0)

        planet.vel = planet.vel + planet.acc * dt

        
        planet.pos = planet.pos + planet.vel * dt
        planet.T = self.equilibrium_temperature(planet.albedo, mag(pos_vector))

        red_value = 1/(1+math.exp(-planet.T/400))

        planet.color = vec(red_value, 1-red_value, 1-red_value)

        planet.trail_color = planet.color



    def update_others(self, planet, others, pos_vector):
       for object in others:
          reverse_pos_vector = object.pos - pos_vector
          theta = atan2(reverse_pos_vector.y, reverse_pos_vector.x)

          acc_mag = planet.mass/math.pow(mag(reverse_pos_vector), 2)

          object.acc = object.acc + vec(acc_mag * cos(theta) * -1, acc_mag * sin(theta) * -1, 0)



sun = sphere(pos=vec(0,0,0),radius=40, mass=333000,luminosity = 3.83e26, color=color.yellow, opacity=1)

scene.height = 400
scene.width = 800

solar_system = StarSystem(sun, [], 1000)





solar_system.animate()




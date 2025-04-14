from vpython import *
import math

sbc = 5.67e-8 #Stefan-Boltzmann constant
h = 6.626e-34
c = 299792458
k_b = 1.380649e-23
solar_radius = 40
true_solar_radius = 6.957e8

class StarSystem:
    
    def __init__(self, star, planets, rate_constant):
        self.au = 750
        self.running = True
        self.star = star
        self.planets = planets
        self.rate_constant = rate_constant

    def create_light(self):
       local_light(pos=self.star.pos + vec(0,10,0), color=color.white)
       local_light(pos=self.star.pos + vec(0,-10,0), color=color.white)

    def animate(self):
        self.create_widget()
      #   self.create_light()
        self.graph_temp_mapping()
        self.black_body_graph(self.get_stellar_temperature(self.star.luminosity))
        print(self.get_stellar_temperature(self.star.luminosity))

        for planet in self.planets:
          
            self.set_planet(planet)

        dt = 1/self.rate_constant
        time_elapsed = 0
        while True:
            rate(self.rate_constant)

            if self.running:
               for planet in self.planets:
                  self.update_planet(planet, dt)
               self.update_star(dt)


               time_elapsed += dt

    def equilibrium_temperature(self, albedo, r):
       flux = self.star.luminosity/(4 * math.pi * math.pow(r/self.au * 1.496e11, 2)) * albedo
       temp = math.pow(flux/(sbc * 4), 1/4)  
       print(temp)
       return temp
    
    def get_stellar_temperature(self, L):
       radius = (((self.star.radius)/solar_radius) * true_solar_radius)
       print(L, math.pow(L/(4 * math.pi * math.pow(radius, 2) *  sbc), 1/4))
       return math.pow(L/(4 * math.pi * math.pow(radius, 2) *  sbc), 1/4)
       
    
    def black_body_graph(self, T):
      blackbody_graph = graph(width=400, height=200, background=color.white, foreground=color.black,
         xtitle="Wavelength (m)", ytitle="Intensity (W/m^2)", title=f"Black Body Radiation at {round(T)} K")
      plot = gcurve(color=color.red, graph=blackbody_graph)
      scene.append_to_caption("\n")
      def planck_function(wavelength, T):
         try:
            return (2 * h * math.pow(c,2))/math.pow(wavelength, 5) * 1/(math.exp((h * c)/(wavelength * k_b * T)) - 1)

         except OverflowError:
            print(wavelength, T)
            return 0
      for i in range(1,5000):
         wavelength = i * 1e-9
         if(i <= 500):
            print(planck_function(wavelength, T))
         intensity = planck_function(wavelength, T)
         plot.plot(data=(wavelength, intensity))

     

    def graph_temp_mapping(self):
      line_break = wtext(text="\n \n")
      def get_color(temp):
         red_value = 1/(1+math.exp(-temp/400))
         return vec(red_value, 1-red_value, 1-red_value)
      
      T_key = graph(height=100, ymin=0, ymax=1, background=color.white, foreground=color.black,
         xtitle="Planetary Temperature (K)")

      
      for i in range(1000):
         bars = gvbars(data=[(i,1)], color=get_color(i), graph=T_key)
                

    def set_planet(self, planet):
      pos_vector = planet.pos-self.star.pos
      



      def velocity(e, theta):       
        r = mag(pos_vector)
        if(e >= 0 and e < 1):
            sma = planet.sma
            v_mag_apogee = math.sqrt(self.star.mass * ((2/planet.dist) - (1/sma)))
            h = planet.dist * v_mag_apogee
            return (self.star.mass/h) * vec(sin(theta) * -1, (e+cos(theta)), 0)
        elif(e == 1):
            v_mag_apogee = math.sqrt(self.star.mass * ((2/planet.dist)))
            h = planet.dist * v_mag_apogee
            return (self.star.mass/h) * vec(sin(theta) * -1, (e+cos(theta)), 0)
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


      # planet.make_trail = True

      
    

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


        def get_luminosity(T):
             luminosity = 4 * math.pi * math.pow(self.star.radius, 2) * sbc * math.pow(T, 4)
             return luminosity

        def get_luminosity(i):
           spectral_list = [color.red, color.orange, color.yellow, color.green, color.blue, color.purple, color.black, color.white]
           if i < 1:
              pass
           else:
              return color_list[i-1]

        def change_spectral_class(evt):
           if evt.index < 1:
              pass
           else:
              self.get_star(evt.index)

        def get_star(spectral):
           # 1 - 7 correspond to OBAFGKM
           if(spectral == 1):
              self.star.color = color.red
              self.star.size = 3
           
              
              
           
        choice_list = ['O', 'B', 'A', 'F', 'G', 'K', 'M']

           
           

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

        spectral_class_menu = menu(choices=choice_list, bind=dummy)
        spectral_class_text = wtext(text=f" Spectral Class: {choice_list[spectral_class_menu.index]} \n")


      #   color_menu = menu(choices=choice_list, bind=dummy)


        def add_planet_handler():
           add_planet_final()

        def add_planet_final():
           self.add_planet(distance_slider.value * self.au, e_slider.value, size_slider.value, albedo_slider.value, theta_slider.value)
           

        add_button = button(text='<b>Add</b>', 
             bind=add_planet_handler, name=None)
        pause_button = button(text='<b>Pause/Play</b>', bind=self.pause_play, name=None)
   
    def pause_play(self):
      self.running  = not self.running  

    def add_planet(self, dist, e, size, albedo, theta):
      self.running = False

      def generate_name(dist, e):
         return str(random() * dist + e)
      
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
      name=generate_name(dist,e), dist=dist, e=e, mass=size, sma=0, albedo=albedo)

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

        print('acc', mag(planet.acc))
        
        planet.pos = planet.pos + planet.vel * dt
        planet.T = self.equilibrium_temperature(planet.albedo, mag(pos_vector))

        red_value = 1/(1+math.exp(-planet.T/400))

        planet.color = vec(red_value, 1-red_value, 1-red_value)

        planet.trail_color = planet.color

        print(planet.color)

        

      #   update_list = [p for p in self.planets if p.name != planet.name]

      #   print(len(self.planets))

      #   update_list.append(self.star)

      #   self.update_others(planet, update_list, pos_vector)

    def update_star(self, dt):
      #  self.star.vel = self.star.vel + self.star.acc * dt

      #  self.star.pos = self.star.pos + self.star.vel * dt
      #  self.star.acc = vec(0,0,0)
      pass


    def update_others(self, planet, others, pos_vector):
       for object in others:
          reverse_pos_vector = object.pos - pos_vector
          theta = atan2(reverse_pos_vector.y, reverse_pos_vector.x)

          acc_mag = planet.mass/math.pow(mag(reverse_pos_vector), 2)

          object.acc = object.acc + vec(acc_mag * cos(theta) * -1, acc_mag * sin(theta) * -1, 0)

           




# venus = sphere(pos=vec(0.72 *au, 0, 0), name="venus", mass = 0.815, radius=9, e=0.0068, color = color.orange, make_trail=True, trail_type="points", interval = 50, retain=1000, )
# earth = sphere(pos=vec(au,0,0), mass=1, name="earth", e= 0.0167, radius=10, color=color.blue, make_trail=True, trail_type="points", interval = 50, retain=1000, )



#random_asteroid = sphere(pos=vec(2*au, 0, 0), name="asteroid", mass = 0.01, radius = 5, e=0.5, color=color.white, make_trail=True)

sun = sphere(pos=vec(0,0,0),radius=40, mass=333000,luminosity = 3.83e26, color=color.yellow, opacity=1)

scene.height = 400
scene.width = 800

solar_system = StarSystem(sun, [], 1000)


solar_system.animate()

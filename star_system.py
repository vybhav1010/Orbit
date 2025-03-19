from vpython import *
import math


class StarSystem:
    def __init__(self, star, planets, rate_constant):
        self.au = 200
        self.running = True
        self.star = star
        self.planets = planets
        self.rate_constant = rate_constant
        self.star.vel = vec(0,0,0)
        self.star.acc = vec(0,0,0)

    def animate(self):
        self.create_widget()

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
            print(sma, "sma")
            v_mag_apogee = math.sqrt(self.star.mass * ((2/planet.dist) - (1/sma)))
            h = planet.dist * v_mag_apogee
            return (self.star.mass/h) * vec(sin(theta) * -1, (e+cos(theta)), 0)

      acc_planet_mag = self.star.mass/math.pow(mag(pos_vector), 2)
    
        
      theta = atan2(pos_vector.y, pos_vector.x)

      theta_orbit = atan2(pos_vector.y * -1, pos_vector.x * -1)

      planet.vel = velocity(planet.e, theta_orbit)
        
      planet.acc = vec(acc_planet_mag * cos(theta) * -1, acc_planet_mag * sin(theta) * -1, 0)
    

    def create_widget(self):
        dist = 0

        def p_dst():
          dtext.text = f"distance: {distance_slider.value} AU \n"


        def p_e():
          etext.text = f"eccentricity: {e_slider.value} \n"

        def p_size():
           stext.text = f"size: {size_slider.value} \n"

        def p_theta():
            ttext.text = f"theta: {round(theta_slider.value/math.pi, 2)}π \n"

        def dummy():
           return   

        def get_color(i):
           color_list = [color.red, color.orange, color.yellow, color.green, color.blue, color.purple, color.black, color.white]
           if i < 1:
              pass
           else:
              return color_list[i-1]   
           
        choice_list = ['Color', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']   
           

        distance_slider = slider(bind=p_dst,min=0.3, max=5)
        dtext = wtext(text=f"distance: {distance_slider.value} AU \n")
        dist = dist * self.au
        e_slider = slider(bind=p_e,min=0, max=5)
        etext = wtext(text=f"eccentriity: {e_slider.value} \n")
        size_slider = slider(bind=p_size,min=0, max=50)
        stext = wtext(text=f"size: {size_slider.value} \n")

        theta_slider = slider(bind=p_theta,min=0, max=2*math.pi)
        ttext = wtext(text=f"theta: {round(theta_slider.value/math.pi,2)}π \n")        

        color_menu = menu(choices=choice_list, bind=dummy)


        def add_planet_handler():
           add_planet_final()

        def add_planet_final():
           self.add_planet(distance_slider.value * au, e_slider.value, size_slider.value, get_color(color_menu.index), theta_slider.value)
           

        add_button = button(text='<b>Add</b>', 
             bind=add_planet_handler, name=None)
        pause_button = button(text='<b>Pause/Play</b>', bind=self.pause_play, name=None)
   
    def pause_play(self):
      self.running  = not self.running  

    def add_planet(self, dist, e, size, color, theta):
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
         

 

      planet = sphere(pos=position(e,dist, theta),make_trail=True, trail_type="points", interval = 100, retain=1000, color=color, radius=size, 
      name=generate_name(dist,e), dist=dist, e=e, mass=size, sma=0)

      if (e>=0 and e<1):
         planet.sma = planet.dist/(1+e)
      elif(e >=1):
         planet.sma = planet.dist/(1-e)
      else:
         planet.sma=0


      self.set_planet(planet)
      self.planets.append(planet)


      self.running = True  

 
    def update_planet(self, planet, dt):
        pos_vector = planet.pos-self.star.pos

        theta = atan2(pos_vector.y, pos_vector.x)

        planet.vel = planet.vel + planet.acc * dt
    
        acc_planet_mag = self.star.mass/math.pow(mag(pos_vector), 2)
        
        planet.acc = vec(acc_planet_mag * cos(theta) * -1, acc_planet_mag * sin(theta) * -1, 0)
        
        planet.pos = planet.pos + planet.vel * dt

      #   update_list = [p for p in self.planets if p.name != planet.name]

      #   print(len(self.planets))

      #   update_list.append(self.star)

      #   self.update_others(planet, update_list, pos_vector)

    def update_star(self, dt):
       self.star.vel = self.star.vel + self.star.acc * dt

       self.star.pos = self.star.pos + self.star.vel * dt
       self.star.acc = vec(0,0,0)


    def update_others(self, planet, others, pos_vector):
       for object in others:
          reverse_pos_vector = object.pos - pos_vector
          theta = atan2(reverse_pos_vector.y, reverse_pos_vector.x)

          acc_mag = planet.mass/math.pow(mag(reverse_pos_vector), 2)

          object.acc = object.acc + vec(acc_mag * cos(theta) * -1, acc_mag * sin(theta) * -1, 0)

           



au = 200


# venus = sphere(pos=vec(0.72 *au, 0, 0), name="venus", mass = 0.815, radius=9, e=0.0068, color = color.orange, make_trail=True, trail_type="points", interval = 50, retain=1000, )
# earth = sphere(pos=vec(au,0,0), mass=1, name="earth", e= 0.0167, radius=10, color=color.blue, make_trail=True, trail_type="points", interval = 50, retain=1000, )



#random_asteroid = sphere(pos=vec(2*au, 0, 0), name="asteroid", mass = 0.01, radius = 5, e=0.5, color=color.white, make_trail=True)

sun = sphere(pos=vec(0,0,0),radius=20, mass=333000, color=color.yellow)

solar_system = StarSystem(sun, [], 1000)


solar_system.animate()

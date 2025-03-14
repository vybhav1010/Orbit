from vpython import *
import math


class StarSystem:
    def __init__(self, star, planets, rate_constant):
        self.au = 200
        self.running = True
        self.star = star
        self.planets = planets
        self.rate_constant = rate_constant

    def animate(self):
        self.create_widget()

        for planet in self.planets:
            self.set_planet(planet)

        dt = 1/self.rate_constant
        time_elapsed = 0
        while self.running:
            rate(self.rate_constant)
            for planet in self.planets:
                self.update_planet(planet, dt)


            time_elapsed += dt

    def set_planet(self, planet):
      pos_vector = planet.pos-self.star.pos


      def velocity(e):       
        r = mag(pos_vector)
        if(e >= 0 and e < 1):
            sma = r/(1 + e)
            v_mag = math.sqrt(self.star.mass * ((2/r) - (1/sma)))
            return vec(0, v_mag, 0)
        elif(e == 1):
            v_mag = math.sqrt(self.star.mass * (2/r))
            return vec(0, v_mag, 0)
        elif(e >= 1):
            sma = r/(1-e)
            v_mag = math.sqrt(self.star.mass * ((2/r) - (1/sma)))
            return vec(0, v_mag, 0) 
        
      acc_planet_mag = self.star.mass/math.pow(mag(pos_vector), 2)
    
        
      theta = atan2(pos_vector.y, pos_vector.x)

      planet.vel = velocity(planet.e)
        
      planet.acc = vec(acc_planet_mag * cos(theta) * -1, acc_planet_mag * sin(theta) * -1, 0)
    

    def create_widget(self):
        dist = 0

        def p_dst():
          dtext.text = f"distance: {distance_slider.value} AU \n"


        def p_e():
          etext.text = f"eccentricity: {e_slider.value} \n"

        def p_size():
           stext.text = f"size: {size_slider.value} \n"

        def dummy():
           return   

        def get_color(i):
           color_list = [color.red, color.orange, color.yellow, color.green, color.blue, color.purple, color.black, color.white]
           print(color_list[i], i)
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

        color_menu = menu(choices=choice_list, bind=dummy)


        def add_planet_handler():
           add_planet_final()

        def add_planet_final():
           self.add_planet(distance_slider.value * au, e_slider.value, size_slider.value, get_color(color_menu.index))
           
           print(self.running)

        add_button = button(text='<b>Add</b>', 
             bind=add_planet_handler, name=None)


    def add_planet(self, dist, e, size, color):
      self.running = False
      planet = sphere(pos=vec(dist, 0, 0),make_trail=True,color=color, radius=size, e =e, mass=1)

      print(dist, e, "add")

      self.set_planet(planet)
      self.planets.append(planet)

      self.running = True  

 
    def update_planet(self, planet, dt):
        

        pos_vector = planet.pos-self.star.pos


        
        theta = atan2(pos_vector.y, pos_vector.x)
        
        try:
            planet.vel = planet.vel + planet.acc * dt
        except TypeError:
            print(planet.color)
    
        acc_planet_mag = self.star.mass/math.pow(mag(pos_vector), 2)
        
        planet.acc = vec(acc_planet_mag * cos(theta) * -1, acc_planet_mag * sin(theta) * -1, 0)
        
        planet.pos = planet.pos + planet.vel * dt


au = 200


venus = sphere(pos=vec(0.72 *au, 0, 0), name="venus", mass = 0.815, radius=9, e=0.0068, color = color.orange, make_trail=True)
earth = sphere(pos=vec(au,0,0), mass=1, name="earth", e= 0.0167, radius=10, color=color.blue, make_trail=True)



random_asteroid = sphere(pos=vec(2*au, 0, 0), name="asteroid", mass = 0.01, radius = 5, e=0.5, color=color.white, make_trail=True)

sun = sphere(radius=20, mass=333000, color=color.yellow)

solar_system = StarSystem(sun, [earth, venus], 200)


solar_system.animate()

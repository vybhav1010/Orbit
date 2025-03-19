from vpython import *
import math

class Sandbox:
  def __init__(self,rate_constant):
    self.rate_constant = rate_constant
    self.running = True
    self.objects = []


  def animate(self):
    self.create_widget()
    dt = 1/self.rate_constant
    time_elapsed = 0
    while True:
        rate(self.rate_constant)

        # for object in self.objects:
        #     object.acc = vec(0,0,0)
        if self.running:
          for object in self.objects:
              self.update_others(object, [oth for oth in self.objects if oth.name !=object.name], dt)
              self.update(object, dt)

          time_elapsed += dt
  

  def create_widget(self):
      x = 0
      y = 0
      def p_size():
          stext.text = f"size: {size_slider.value} \n"

      def p_x():
          xtext.text = f"X: {x_slider.value} \n"

      def p_y():
          ytext.text = f"Y: {y_slider.value} \n" 

      def p_vel():
          vtext.text = f"velocity: {vel_slider.value} \n"  

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
          

      x_slider = slider(bind=p_x,min=0, max=1000)
      xtext = wtext(text=f"X: {x_slider.value} \n")

      y_slider = slider(bind=p_y,min=0, max=1000)
      ytext = wtext(text=f"Y: {y_slider.value} \n")

      vel_slider = slider(bind=p_vel,min=0, max=50)
      vtext = wtext(text=f"velocity: {vel_slider.value} \n")

      theta_slider = slider(bind=p_theta,min=0, max=2*math.pi)
      ttext = wtext(text=f"theta: {round(theta_slider.value/math.pi,2)}π \n")

      size_slider = slider(bind=p_size,min=0, max=50)
      stext = wtext(text=f"size: {size_slider.value} \n")

      color_menu = menu(choices=choice_list, bind=dummy)

      def add_object_handler():
          add_object_final()

      def add_object_final():
          self.add_object(x_slider.value , y_slider.value, size_slider.value,vec(vel_slider.value * cos(theta_slider.value), vel_slider.value * sin(theta_slider.value), 0), get_color(color_menu.index))
          
      add_button = button(text='<b>Add</b>', 
            bind=add_object_handler, name=None)
      clear_button = button(text='<b>Clear</b>',
            bind=self.clear_objects, name=None)
      pause_button = button(text='<b>Pause/Play</b>', bind=self.pause_play, name=None)

  def clear_objects(self):
    for object in self.objects:
      object.visible = False
      self.objects.remove(object)

  def pause_play(self):
    self.running  = not self.running

  def add_object(self, x, y, size, vel, color):
    self.running = False

    def generate_name(x, y):
        return str(random() * x + y)

    object = sphere(pos=vec(x, y, 0), vel=vel, make_trail=True, trail_type="points", interval = 200, retain=70, color=color, radius=size, 
    name=generate_name(x,y), acc=vec(0,0,0), mass=size*10000)

    self.objects.append(object)

    self.running = True  

  def update_others(self, planet, others, dt):
    for object in others:
      reverse_pos_vector = object.pos - planet.pos
      theta = atan2(reverse_pos_vector.y, reverse_pos_vector.x)

      try:
        acc_mag = planet.mass/math.pow(mag(reverse_pos_vector), 2)
      except ZeroDivisionError:
         acc_mag = planet.mass/math.pow(0.0001, 2)

      object.acc = object.acc + vec(acc_mag * cos(theta) * -1, acc_mag * sin(theta) * -1, 0)  

  def update(self, object, dt):
      object.vel = object.vel + object.acc * dt
      object.pos = object.pos + object.vel * dt
      object.acc = vec(0,0,0)


Sandbox(1000).animate()      



   
from tkinter import Tk, Label
from time import sleep
from subprocess import run, PIPE, STDOUT

# temperature display parameters
temp_warning = 20
temp_critical = 25

fg_normal = '#000'
fg_warning = '#000'
fg_critical = '#fff'

bg_normal = '#fff'
bg_warning = '#FFFF00'
bg_critical = '#FF0000'

fg_color = fg_normal
bg_color = bg_normal

root = Tk()
root.title('SNR ERD')
root['bg']=bg_color

location_label = Label(text='SNR ERD t°', font=("Arial Bold", 18), fg=fg_color, bg=bg_color)
show_temp = Label(text='-', font=("Arial Bold", 62), fg=fg_color, bg=bg_color)

location_label.pack()
show_temp.pack()

# device
class snr_erd():
  ip = 'SNR_IP'
  pwd = 'SNR_PASSWORD'

  @classmethod
  def get_info(self, oid):
    cmd = ['snmpget', '-v', '1', '-Oqv', '-c', self.pwd, self.ip, oid]
    result = run(cmd, stdout=PIPE, stderr=STDOUT).stdout.decode('utf-8')
    return result
  
  @classmethod
  def get_temperature(self):
    result = self.get_info('iso.3.6.1.4.1.40418.2.4.4.2.2.0')
    return result

def main():
  time = 0
  delay = 60
  temp =  snr_erd.get_temperature()
  while True:
    if (time - delay) > 0:
      time = 0
      temp =  snr_erd.get_temperature()
    try:
      temp = int(temp)
      if (temp >= temp_warning) and (temp < temp_critical):
        bg_color = bg_warning
        fg_color = fg_warning
      elif temp >= temp_critical:
        bg_color = bg_critical
        fg_color = fg_critical
      else:
        bg_color = bg_normal
        fg_color = fg_normal
    except ValueError:
      bg_color = bg_critical
      fg_color = fg_critical
      temp = 'ERROR'
    show_temp.config(text=str(temp)+'°', bg=bg_color, fg=fg_color)
    root.update()
    time += 1
    sleep(1)

if __name__ == '__main__':
  main()

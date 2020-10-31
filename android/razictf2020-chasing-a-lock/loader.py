import time
import frida

device = frida.get_usb_device()
pid = device.spawn(["com.example.razictf_2"])
device.resume(pid)
time.sleep(1)  # Without it Java.perform silently fails
session = device.attach(pid)
with open("script.js") as f:
    script = session.create_script(f.read())
script.load()

# prevent the python script from terminating
input()

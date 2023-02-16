import PySimpleGUI as sg
from pymem import *
from pymem.process import *

mem = Pymem("HarshDoorstop-Win64-Shipping.exe")
module = module_from_name(mem.process_handle, "HarshDoorstop-Win64-Shipping.exe").lpBaseOfDll
offsets1 = [0x260, 0x20, 0x2B0, 0x370, 0x270, 0x260, 0x70]

def GetPointer(base, offsets):
    addr = mem.read_longlong(base+0x03E5E2C0)
    for offset in offsets:
        if offset != offsets[-1]:
            try:
                addr = mem.read_longlong(addr + offset)
            except Exception as e:
                print(e)
    return addr + offsets[-1]

def ammo_value():
    ammo = mem.read_int(GetPointer(module, offsets1))
    return ammo

sg.theme('Dark Blue 3')

layout = [[sg.Text('Ammo: ', size=(10,1), font=("Helvetica", 20)),
           sg.Text('0', size=(10,1), font=("Helvetica", 20), key='-AMMO-')]]

window = sg.Window('Ammo Overlay', layout, keep_on_top=True, alpha_channel=0.7)

while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    window['-AMMO-'].update(str(ammo_value()))

window.close()

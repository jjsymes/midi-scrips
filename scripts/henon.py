from math import cos, sin
import matplotlib.pyplot as plt
from random import random
from time import sleep
from mido import Message, get_output_names, open_output

def equation_a(x, y, a):
    return (x*cos(a)) - ((y - x**2)*sin(a))

def equation_b(x, y, a):
    return (x*sin(a)) + ((y - x**2)*cos(a))

def henon_mapping_generator(a_parameter, initial_x, initial_y, number_of_iterations, equation_a=equation_a, equation_b=equation_b):
    print(initial_x, initial_y)
    x = initial_x
    y = initial_y
    for _ in range(number_of_iterations):
        x_next, y_next = equation_a(x, y, a_parameter), equation_b(x, y, a_parameter)
        x, y = x_next, y_next
        yield x, y

def radially_expanding_henon_mappings_generator(a_parameter, iterations_per_orbit=32, starting_radius=0.1, radial_step=0.1):
    radius = starting_radius
    while radius <= 1:
        radius += radial_step
        for x, y in henon_mapping_generator(a_parameter, radius, radius, iterations_per_orbit):
            yield x, y

def get_available_midi_output_names():
    return get_output_names()

def get_default_midi_output_name() -> str:
    output_names = get_available_midi_output_names()
    if len(output_names) == 0:
        raise Exception("No MIDI output devices found")
    return output_names[0]

def main():
    # change these parameters
    a_parameter = 1.111
    iterations_per_orbit = 32  # (10 - 1000)
    number_of_orbits = 33 # (1 - 100)
    starting_radius = 0.1 # (0.1 - 1)
    note_duration = .1
    plot = False
    midi_out = True

    radial_step = (1 - starting_radius)/number_of_orbits
    if midi_out:
        midi_out_device_name = get_default_midi_output_name()
        midi_out_device = open_output(midi_out_device_name)
    
    if plot:
        plt.xlim(-1.2, 1.2)
        plt.ylim(-1.2, 1.2)
        plt.show(block=False)

    try:
        for i, xy in enumerate(radially_expanding_henon_mappings_generator(a_parameter, iterations_per_orbit=iterations_per_orbit, starting_radius=starting_radius, radial_step=radial_step)):
            x, y = xy
            if midi_out:
                note = int((abs(x + 1)/2)*127)
                if note < 0:
                    note = 0
                elif note > 127:
                    note = 127
                velocity = int((abs(y + 1)/2)*127)
                if velocity < 0:
                    velocity = 0
                elif velocity > 127:
                    velocity = 127
                print(f"Note: {note}, Velocity: {velocity}, X: {x}, Y: {y}")
                midi_out_device.send(Message('note_on', note=note, velocity=velocity))
                sleep(note_duration)
                midi_out_device.send(Message('note_off', note=note, velocity=velocity))
            if i % iterations_per_orbit == 0:
                color = (random(), random(), random())
            if plot:
                plt.xlim(-1.2, 1.2)
                plt.ylim(-1.2, 1.2)
                plt.scatter(x, y, s=0.1, c=color)
                plt.pause(0.001)
    except OverflowError:
        pass

main()
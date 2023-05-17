from typing import List
from random import random
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo


def logistic_function(x: float, r: float) -> float:
    return r * x * (1 - x)


def logistic_map_output(
    r_parameter: float, x_initial: float, number_of_iterations: int, burn_in: int = 0
) -> List[float]:
    """
    x_{n+1} = r.x_{n}.(1-x_{n})
    :param r_parameter r parameter value to use to generate the logistic map
    :param x_initial: initial value of x
    :param number_of_iterations: number of iterations to run the logistic map for
    :param burn_in: number of iterations to discard before returning the output, defaults to
    :returns: array of x values
    :raises ValueError: raises an exception if x_initial is not between 0 and 1 or
    if burn_in is greater than or equal to number_of_iterations
    """
    if x_initial < 0 or x_initial > 1:
        raise ValueError("x_initial must be between 0 and 1")
    if burn_in >= number_of_iterations:
        raise ValueError("burn_in must be less than number_of_iterations")

    successive_x_values = []
    x = x_initial
    for i in range(number_of_iterations):
        x = logistic_function(x, r_parameter)
        if i >= burn_in:
            successive_x_values.append(x)
    return successive_x_values


def generate_r_values(r_start: float, r_end: float, r_step: float) -> List[float]:
    """
    Generates a list of r values to use for the bifurcation diagram
    :param r_start: starting value of r
    :param r_end: ending value of r
    :param r_step: step size of r
    :returns: list of r values
    """
    r_step_decimal_places = len(str(r_step).split(".")[1])
    number_of_decimal_places = r_step_decimal_places + 1
    return [round((r_start + i * r_step), number_of_decimal_places) for i in range(int((r_end - r_start) // r_step))]

def main():
    r_start = 2.9
    r_end = 3.9999
    r_step = 0.001
    iterations_per_second = 10

    bpm = 120
    tempo = bpm2tempo(bpm)
    mid = MidiFile(ticks_per_beat=960)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=tempo))

    ticks_per_second = mid.ticks_per_beat * bpm / 60
    note_length_ticks = int(ticks_per_second // iterations_per_second)

    # sustain pedal on
    track.append(Message("control_change", control=64, value=127, time=0))

    r_values = generate_r_values(r_start, r_end, r_step)
    
    for i, r in enumerate(r_values):
        x_values = logistic_map_output(r, random(), 1000, 994)
        x_values = [round(x, 2) for x in x_values]
        x_values_no_duplicates = list(set(x_values))
        x_values_no_duplicates.sort()

        x_value_to_play = x_values_no_duplicates[i % len(x_values_no_duplicates)]
        midi_note = int(round(x_value_to_play * 88))

        track.append(Message("note_on", note=midi_note, velocity=64, time=0))

        track.append(
            Message(
                "note_off",
                note=midi_note,
                velocity=127,
                time=note_length_ticks
            )
        )
    
    mid.save("out.mid")


if __name__ == "__main__":
    main()
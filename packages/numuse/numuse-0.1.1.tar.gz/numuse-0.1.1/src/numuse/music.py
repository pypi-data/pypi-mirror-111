from __future__ import annotations
from typing import List, Type
from fractions import Fraction
from .notation import NoteCollection


class Music:
    """Represents notes that are played over time"""

    def __init__(self, measures: List[Measure], BPM: int, beats_in_a_measure: int = 4):
        self.measures = measures
        # TODO this only works for music with only single line measures
        # Otherwise we need to specify that lines need to come in the same order
        # in each measure, but that becomes complicated when # of lines change
        self.continuous = [moment for measure in measures for line in measure.lines for moment in line.moments]
        # Assumes a song stays at a constant tempo
        # TODO: make it dynamic
        self.BPM = BPM
        self.beats_in_a_measure = beats_in_a_measure
        self.measure_length = self.bpm_to_measure_length()

    def bpm_to_measure_length(self, beats_in_a_measure: int = 4) -> float:
        # TODO this doesn't make sense if you have a change of meter
        # but we can do that later
        # returns in seconds
        beats_per_second = self.BPM * 1 / 60
        seconds_per_beat = 1 / beats_per_second
        measure_length = seconds_per_beat * beats_in_a_measure

        return measure_length

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Measure:
    def __init__(
        self,
        lines: List[Line],
        beats_in_a_measure: int = 4,
        beat_duration: Fraction = 1,
    ):
        self.lines = lines
        self.beats_in_a_measure = beats_in_a_measure
        self.beat_duration = beat_duration
        self.measure_duration = sum(m_l.line_duration for m_l in lines)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Moment:
    def __init__(self, time: float, notes: Type[NoteCollection], duration: Fraction):
        self.time = time
        self.notes = notes
        self.duration = duration

    def __str__(self):
        return f"Notes: {self.notes}, Held for: {self.duration}, At time: {self.time}"

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Line:
    """Due to the way we write music notes follow consecutively

    In order to write ideas like this:

    Note 1: ==========================
    Note 2:         ========

    Then one solution is to have two different clefs

    This class represents such a clef

    Note this is required because of the way we notate things sequentially in music
    """

    def __init__(self, moments: List[Moment]):
        self.moments = moments
        self.line_duration = sum(m_m.duration for m_m in self.moments)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class StructuredMusic(Music):
    """Represents notes played over time that are related to an underlying structure

    In this case the structure is a set of notes which have a higher probability of being
    played than other notes.

    The structure is a note collection and can be specified using a RIC

    music_data is now allowed to use a special type of syntax on top of the previous method

    """

    pass

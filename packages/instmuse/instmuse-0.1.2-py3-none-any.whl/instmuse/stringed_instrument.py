from __future__ import annotations
import numuse.tools
import numuse.constants
import numuse.notation
import numuse.musical_system
from typing import List, Tuple, Dict


class Instrument:
    """A device which is inteded to create notes from a musical system"""

    def __init__(
        self,
        musical_system=numuse.musical_system.RBMS_Approximation(
            440, numuse.constants.JUST_INTONATION_RATIOS, 2, 2 ** (1 / 12), 12
        ),
    ):
        self.musical_system = musical_system


class StringedInstrument(Instrument):
    """A stringed instrument with consecutive strings which get higher and only one note can be played
    on a string at a time"""

    def __init__(
        self,
        string_interval_pattern: List[int],
        lowest_note,
        musical_system=numuse.musical_system.RBMS_Approximation(
            440, numuse.constants.JUST_INTONATION_RATIOS, 2, 2 ** (1 / 12), 12
        ),
    ):
        super().__init__(musical_system)
        self.string_interval_pattern = string_interval_pattern
        self.lowest_note = lowest_note
        self.num_strings = len(string_interval_pattern) + 1
        self.open_string_notes = []
        self.generate_open_string_notes()

    def generate_open_string_notes(self):
        """Generates the notes for this stringed instrument"""
        for i in range(self.num_strings):
            if i == 0:
                self.open_string_notes.append(self.lowest_note)
            else:
                self.open_string_notes.append(
                        self.open_string_notes[i - 1] + self.string_interval_pattern[i - 1]
                )


class ModularGridStringedInstrument(StringedInstrument):
    """A stringed instrument arranged in a modular grid, one of the most well known modular grids is
    the modular_grid/fingerboard"""

    def __init__(
        self,
        num_frets: int,
        string_interval_pattern: List[int],
        lowest_note: numuse.notation.Note,
        musical_system=numuse.musical_system.RBMS_Approximation(
            440, numuse.constants.JUST_INTONATION_RATIOS, 2, 2 ** (1 / 12), 12
        ),
    ):
        super().__init__(string_interval_pattern, lowest_note, musical_system)
        self.num_frets = num_frets


class ModularGridNoteCollection(numuse.notation.NoteCollection):
    """A physical configuration which generates notes held
    for a given duration

    This specifies a way to play a notes on a physical instrument

    A list of (x,y) coordinates define a string and fret position
    which in turn define a set of notes

    .. note::
        Even though not ever stringed instrument has frets, we consider
        the location that precisely generates a note from a musical system
        to be a fret

    Since we can consider the modular_grid a 2d sheet with points along the sheet
    we will refer to the the points via tuples of the form

    (string_num, fret_num)

    Where the thickest string is 0, the thinnest being having the highest number.
    (To remember this simply remember that the pitch increase so so should the indexing)

    Similarly we will refer to an open string being played as fret 0 and index incrementally
    while moving towards the center of the device, so that playing a note one unit higher
    than the previous in the musical system corresponds to moving one fret closer to the center of the
    device.
    """

    def __init__(
        self,
        modular_grid_positions: Dict[int, int],
        duration: int = 0,
        modular_grid_instrument=ModularGridStringedInstrument(
            24, [5, 5, 5, 4, 5], numuse.notation.Note(4 - 12 * 2)
        ),
    ):
        self.modular_grid_instrument = modular_grid_instrument
        self.modular_grid_positions = modular_grid_positions
        self.modular_grid_labels = {}
        temp_notes = set()
        for string_pos, fret_pos in self.modular_grid_positions.items():
            mg_note = self.modular_grid_instrument.open_string_notes[string_pos] + fret_pos
            temp_notes.add(
                    mg_note
            )
            self.modular_grid_labels[string_pos] = numuse.tools.ranged_modulus_operator(mg_note.note)
        super().__init__(temp_notes, duration, self.modular_grid_instrument.musical_system)

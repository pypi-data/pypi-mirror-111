import numuse.converters
import numuse.music
from fractions import Fraction
from .converters import generate_MGNCs_from_MG_shorthand

if __name__ == "__main__":

    b = 1
    # half
    h = 1 / 2
    # thirds
    t = Fraction(b, 3)
    # two thirds
    tt = 2 * t

    # TODO develop the equiavlent form of rootedintervalcollection but for modulargridnotecollection
    two_five_one = [
        [("(X 5 X 5 5 5)", [4 * b])],
        [("(X X 5 7 6 7)", [4 * b])],
        [("(X 3 5 4 5 X)", [4 * b])],
    ]


    #print(generate_MGNCs_from_MG_shorthand("(X 5 X 5 5 5) (X X 5 7 6 7) (X 3 5 4 5 X)"))
    measures = numuse.converters.parse_music_measures(two_five_one, generate_MGNCs_from_MG_shorthand)
    m = numuse.music.Music(measures, 120)
    for measure in m.measures:
        for line in measure.m_lines:
            for moment in line.m_moments:
                #print(moment)
                pass

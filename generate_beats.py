#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random

SCORE_TEMPLATE = r"""
\version "2.18.2"

\header {
  title = "%(title)s"
  composer = "%(composer)s"
}

beatstaff = {
  \override Staff.StaffSymbol.line-positions = #'( 0 )
}

music = \new DrumStaff {
  \beatstaff
  \override Stem.neutral-direction = #up
  \drummode {
    \time %(signature)s
    %(beats)s
  }
}

\score {
  \music
  \layout {}
  \midi {}
}
"""

# For any beat, add the annotation to the pool. 1 is whole, 4 quarter, etc.
note_string_to_fraction = {}
rest_string_to_fraction = {}
FRACTIONS = (1, 2, 4, 8, 16, 32)
FRACTIONS = (1, 2, 4, 8)
for i in FRACTIONS:
  note_string_to_fraction['tamb%s' % i] = i
  rest_string_to_fraction['r%s' % i] = i
  # TODO: Below code is totally wrong; proper fix involves moving to a list of
  # fractions, but that will impact all the other code.
  if 0 and i > 1 and i < FRACTIONS[-1]:
    note_string_to_fraction['tamb%s.' % i] = i + i / 2  # <-- Nonsense
    rest_string_to_fraction['r%s' % i] = i + i / 2

all_marks_to_fraction = {}
all_marks_to_fraction.update(note_string_to_fraction)
all_marks_to_fraction.update(rest_string_to_fraction)

def float_is_almost_integer(a_float, b_int):
  a_integer_part = int(a_float + 0.5)
  a_fractional_part = abs(a_float - a_integer_part)
  return a_fractional_part < 1e-5 and a_integer_part == b_int

def generate_bar(marks_to_fraction, whole_notes_per_bar):
  beats_in_bar_total = 0
  generated_beats = []
  while not float_is_almost_integer(beats_in_bar_total, whole_notes_per_bar):
    beat = random.choice(list(marks_to_fraction.keys()))
    new_beats_in_bar_total = beats_in_bar_total + 1.0 / marks_to_fraction[beat]
    if new_beats_in_bar_total > whole_notes_per_bar:
      continue

    generated_beats.append(beat)
    beats_in_bar_total += 1.0 / marks_to_fraction[beat]
  print('Bar:', ' '.join(generated_beats))
  return generated_beats

def generate_bars(marks_to_fraction, whole_notes_per_bar, num_bars):
  return [generate_bar(marks_to_fraction, whole_notes_per_bar)
          for i in range(num_bars)]

def generate_score(marks_to_fraction, whole_notes_per_bar, num_bars):
  bars = generate_bars(marks_to_fraction, whole_notes_per_bar, num_bars)
  return SCORE_TEMPLATE % dict(
      title='A randomly generated rhythm',
      composer='Keir Mierle',
      signature='4/4',
      beats='|\n    '.join(' '.join(note for note in bar) for bar in bars))

if __name__ == '__main__':
  score = generate_score(all_marks_to_fraction, 1, 70)
  with open('generated.ly', 'w') as outfile:
    outfile.write(score)

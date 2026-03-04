# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from bespoke import Card
from bespoke import Deck
from bespoke import Difficulty
from bespoke import Language
from bespoke import Mode
from bespoke import languages


class TestIndex:
    def __init__(
        self,
        target_language: Language,
        native_language: Language,
    ) -> None:
        del native_language
        self._target_language = target_language

    def cards(self, unit: str) -> list[Card]:
        if unit not in self._target_language.full_vocabulary():
            return []
        card = Card(
            id=unit,
            sentence=unit,
            native_sentence="dummy",
            audio_filename="fake.ogg",
            slow_audio_filename="slow.ogg",
            native_audio_filename="native.ogg",
            phonetic="abc",
            units=[unit],
            unit_tags={unit: unit},
            notes=[],
        )
        return [card]

    def size(self, unit: str) -> int:
        return int(unit in self._target_language.full_vocabulary())


class TestDeck(unittest.TestCase):
    def test_draw(self) -> None:
        target = languages.LANGUAGES["japanese"]
        native = languages.LANGUAGES["english"]
        index = TestIndex(target, native)
        deck = Deck(target, native, index)
        deck.set_modes([Mode.LISTEN, Mode.SPEAK])
        mode, card = deck.draw()
        unit = target.vocabulary(Difficulty.A1)[0]
        self.assertEqual(mode, Mode.LISTEN)
        self.assertEqual(card.sentence, unit)

    def test_rate(self) -> None:
        target = languages.LANGUAGES["japanese"]
        native = languages.LANGUAGES["english"]
        index = TestIndex(target, native)
        deck = Deck(target, native, index)
        deck.set_modes([Mode.LISTEN, Mode.SPEAK])
        mode, card = deck.draw()
        unit = target.vocabulary(Difficulty.A1)[0]
        self.assertEqual(card.units, [unit])
        deck.rate(unit, mode, 3)
        _mode, card = deck.draw()
        unit = target.vocabulary(Difficulty.A1)[1]
        self.assertEqual(card.units, [unit])

    def test_assume_known(self) -> None:
        target = languages.LANGUAGES["japanese"]
        native = languages.LANGUAGES["english"]
        index = TestIndex(target, native)
        deck = Deck(target, native, index)
        deck.set_assume_known(Difficulty.A2)
        _mode, card = deck.draw()
        unit = target.vocabulary(Difficulty.B1)[0]
        self.assertEqual(card.sentence, unit)


if __name__ == "__main__":
    unittest.main()

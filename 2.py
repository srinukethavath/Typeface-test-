import re
from unidecode import unidecode

from ..utils import translation, squeeze, check_str, check_empty
from .phonetic_algorithm import PhoneticAlgorithm
import re
from unidecode import unidecode

from ..utils import translation, squeeze, check_str, check_empty
from .phonetic_algorithm import PhoneticAlgorithm



class Soundex(PhoneticAlgorithm):
    
    def __init__(self):
        super().__init__()

        self.translations = translation(
            'AEIOUYWHBPFVCSKGJQXZDTLMNR',
            '000000DD111122222222334556'
        )
        self.pad = lambda code: '{}0000'.format(code)[:4]

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        word = unidecode(word).upper()
        word = re.sub(r'[^A-Z]', r'', word)

        first_letter = word[0]
        tail = ''.join(self.translations[char] for char in word
                       if self.translations[char] != 'D')

        # Dropping first code's letter if duplicate
        if len(tail):
            if tail[0] == self.translations[first_letter]:
                tail = tail[1:]

        code = squeeze(tail).replace('0', '')
        return self.pad(first_letter + code)
from ..distance_metrics import levenshtein_distance, hamming_distance
from ..exceptions import DistanceMetricError
class PhoneticAlgorithm:
    
    def __init__(self):
        self.distances = {
            'levenshtein': levenshtein_distance,
            'hamming': hamming_distance,
        }

    def phonetics(self, word):
        
        pass

    def sounds_like(self, word1, word2):
       
        return self.phonetics(word1) == self.phonetics(word2)

    def distance(self, word1, word2, metric='levenshtein'):
       
        if metric in self.distances:
            distance_func = self.distances[metric]
            return distance_func(self.phonetics(word1), self.phonetics(word2))
        else:
            raise DistanceMetricError('Distance metric not supported! Choose from levenshtein, hamming.')

class RefinedSoundex(PhoneticAlgorithm):
    
    def __init__(self):
        super().__init__()

        self.translations = translation(
            'AEIOUYWHBPFVCKSGJQXZDTLMNR',
            '000000DD112233344555667889'
        )

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        word = unidecode(word).upper()
        word = re.sub(r'[^A-Z]', r'', word)

        first_letter = word[0]
        tail = ''.join(self.translations[char] for char in word
                       if self.translations[char] != 'D')

        return first_letter + squeeze(tail)

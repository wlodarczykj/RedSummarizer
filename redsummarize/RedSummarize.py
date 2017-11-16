import sys

STOP_WORDS = ['the', 'is', 'to', 'that', 'for', 'of', 'a', 'i', 'at', 'it', 'he', 'she']

class Summarizer:
    def __init__(self, filename):
        file = open(filename, "r")
        self.content = file.read()

    @classmethod
    def score_sentence(cls, sentence, score_map):
        words = sentence.split(" ")
        word_count = len(words)
        avg_score = 0

        for word in words:
            if word in score_map:
                avg_score += score_map[word]
        
        return avg_score / word_count

    @classmethod
    def is_punctuation(cls, character):
        return character == '.' or character == '?' or character == '!'


    def summarize(self):
        score_map = {}
        words = self.content.replace("\n", " ").replace(".", " ").split(' ')
        total_word_count = len(words)

        for word in words:
            if word in score_map and word not in STOP_WORDS:
                score_map[word] += 1
            elif word not in STOP_WORDS:
                score_map[word] = 1

        for word in score_map:
            score_map[word] = score_map[word] / total_word_count

        sentence_map = {}
        sentence = ""
        for char in self.content.replace("\n", ""):
            if self.is_punctuation(char):
                sentence_map[sentence] = self.score_sentence(sentence, score_map)
                sentence = ""
            else:
                sentence += char

        best_sentence_score = 0
        best_sentence = ""
        for sen in sentence_map:
            if sentence_map[sen] > best_sentence_score:
                best_sentence = sen

        print(best_sentence)    



if len(sys.argv) > 1:
    ez_sum = Summarizer(sys.argv[1])
    ez_sum.summarize()


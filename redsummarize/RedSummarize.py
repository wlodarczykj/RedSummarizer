import sys

#TODO move this
STOP_WORDS = ['the', 'The', 'They', 'can', 'are', 'be', 'or', 'and', 'is',
             'to', 'that', 'for', 'of', 'a', 'i', 'at', 'it', 'he',
              'she', 'they', 'don\'t', 'do', 'this', 'have', 'in',
              'has', 'an']

class Summarizer:
    def __init__(self, filename):
        file = open(filename, "r")
        self.content = file.read()

    @classmethod
    def score_sentence(cls, sentence, score_map):
        words = sentence.split(" ")
        word_count = len(words)
        avg_prob = 0
        best_word = ("", 0)

        for word in words:
            if word in score_map:
                avg_prob += score_map[word]

                if score_map[word] > best_word[1]:
                    best_word = (word, score_map[word])
        
        avg_prob = avg_prob / word_count

        return avg_prob * best_word[1]

    @classmethod
    def is_punctuation(cls, character):
        return character == '.' or character == '?' or character == '!'

    @classmethod
    def summarize_one(cls, content):
        score_map = {}

        words = content.replace("\n", " ").replace(".", " ").replace("\"", "").split(' ')
        total_word_count = len(words)

        for word in words:
            if word and word in score_map and word not in STOP_WORDS:
                score_map[word] += 1
            elif word and word not in STOP_WORDS:
                score_map[word] = 1

        for word in score_map:
            score_map[word] = score_map[word] / total_word_count

        sentence_map = {}
        sentence = ""
        for char in content.replace("\n", ""):
            sentence += char
            if cls.is_punctuation(char):
                sentence_map[sentence] = cls.score_sentence(sentence, score_map)
                sentence = ""

        best_sentence_score = 0
        best_sentence = ""
        for sen in sentence_map:
            if sentence_map[sen] > best_sentence_score:
                best_sentence_score = sentence_map[sen]
                best_sentence = sen

        return best_sentence

    def summarize(self, num_sentences):
        summarize_content = self.content

        total_sum = ""        
        for x in range(0, num_sentences):
            best = self.summarize_one(summarize_content)
            total_sum += best
            summarize_content = summarize_content.replace(best, "")

        print(total_sum)


if len(sys.argv) > 1:
    ez_sum = Summarizer(sys.argv[1])
    ez_sum.summarize(3)


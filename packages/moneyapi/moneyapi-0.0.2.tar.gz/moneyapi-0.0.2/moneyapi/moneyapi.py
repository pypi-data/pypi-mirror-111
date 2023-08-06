import requests
import json
class Advice:

    def __init__(self, advice_id, message):
        self.advice_id = advice_id
        self.message = message

    def getAdvice(self):
        return self.message

    def getAdviceID(self):
        return self.advice_id

    advice = property(getAdvice)
    ID = property(getAdviceID)


class Question:
    def __init__(self, question_id, question, answers, correct):
        self.question_id = question_id
        self.question = question
        self.answers = answers
        self.correct = correct

    def getChoices(self):
        return self.answers.split(",")

    def getQuestionID(self):
        return self.question_id

    def getCorrect(self):
        return self.correct

    def getQuestion(self):
        return self.question

    problem = property(getQuestion)
    ID = property(getQuestionID)
    answer = property(getCorrect)
    choice = property(getChoices)


class Word:

    def __init__(self, word_id, word, definition):
        self.word_id = word_id
        self.term = word
        self.definition = definition

    def getDefinition(self):
        return self.definition

    def getWordID(self):
        return self.word_id

    def getWord(self):
        return self.term

    word = property(getWord)
    ID = property(getWordID)
    define = property(getDefinition)

class MoneyAPi:

    def __init__(self,saveType=False):
        self.saveType = saveType
        self.version = "1"
        if self.saveType == True:
            self.advices = None
            self.words = None
            self.questions = None

    def getAllAdvices(self):

        if self.saveType == True and self.advices != None:
            return self.advices

        elif self.saveType == True and self.advices == None:
            temp = []
            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/advices').text)[
                "advices"]
            for result in results:
                temp.append(Advice(result["advice_id"], result["message"]))
            self.advices = temp
            return temp

        else:
            temp = []
            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/advices').text)[
                "advices"]
            for result in results:
                temp.append(Advice(result["advice_id"], result["message"]))
            return temp

    def getAllQuestions(self):
        if self.saveType == True and self.questions != None:
            return self.questions

        elif self.saveType == True and self.questions == None:
            temp = []
            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/questions').text)[
                "questions"]
            for result in results:
                temp.append(Question(result["question_id"], result["question"], result["answers"], result["correct"]))

            self.questions = temp
            return temp
        else:

            temp = []
            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/questions').text)[
                "questions"]
            for result in results:
                temp.append(Question(result["question_id"], result["question"], result["answers"], result["correct"]))

            return temp

    def getAllWords(self):

        if self.saveType == True and self.words != None:
            return self.words

        elif self.saveType == True and self.words == None:
            temp = []

            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/words').text)["words"]
            for result in results:
                temp.append(Word(result["word_id"], result["word"], result["definition"]))

            self.words = temp
            return temp

        else:
            temp = []

            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/words').text)["words"]
            for result in results:
                temp.append(Word(result["word_id"], result["word"], result["definition"]))

            return temp

    def getAdvice(self, advice_id):

        if self.saveType == True and self.advices != None:
            return self.advices[advice_id - 1]

        elif self.saveType == True and self.advices == None:
            temp = []
            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/advices/').text)[
                "advices"]
            for result in results:
                temp.append(Advice(result["advice_id"], result["message"]))
            self.advices = temp
            return self.advices[advice_id - 1]

        else:

            temp = []
            results = json.loads(
                requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/advices/' + str(advice_id)).text)[
                "advices"]
            for result in results:
                temp.append(Advice(result["advice_id"], result["message"]))
            return temp[0]

    def getQuestion(self, question_id):
        if self.saveType == True and self.questions != None:
            return self.questions[question_id - 1]

        elif self.saveType == True and self.questions == None:
            print("no\n\n\n")
            temp = []
            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/questions/').text)[
                "questions"]
            for result in results:
                temp.append(Question(result["question_id"], result["question"], result["answers"], result["correct"]))

            self.questions = temp
            return self.questions[question_id - 1]
        else:
            temp = []
            results = json.loads(
                requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/questions/' + str(question_id)).text)[
                "questions"]
            for result in results:
                temp.append(Question(result["question_id"], result["question"], result["answers"], result["correct"]))

            return temp[0]

    def getWord(self, word_id):

        if self.saveType == True and self.words != None:
            return self.words[word_id - 1]

        elif self.saveType == True and self.words == None:
            temp = []

            results = json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/words/').text)[
                "words"]
            for result in results:
                temp.append(Word(result["word_id"], result["word"], result["definition"]))

            self.words = temp
            return self.words[word_id - 1]

        else:
            temp = []

            results = \
            json.loads(requests.get('https://www.moneyapi.xyz/dev/v' + self.version + '/words/' + str(word_id)).text)[
                "words"]
            for result in results:
                temp.append(Word(result["word_id"], result["word"], result["definition"]))

            return temp[0]







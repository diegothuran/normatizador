import nltk
import csv

class Analise (object):
    def __init__(self):

        self.dataPath_treino = 'normatizacao/classificacao/treino.csv'
        self.dataPath_teste ='normatizacao/classificacao/teste_normatizador.csv'
        self.stopwordsnltk = nltk.corpus.stopwords.words('portuguese')

        self.base = self.getBase()
        self.treino = self.aplicastemmer(self.base)
        self.palavrastreinamento = self.buscapalvras(self.treino)
        self.frequenciatreinamento = self.buscafrequencia(self.palavrastreinamento)
        self.palavrasunicastreinamento = self.buscapalavrasunicas(self.frequenciatreinamento)

        self.baseTeste = self.getBaseTeste()
        self.teste = self.aplicastemmer(self.baseTeste)
        self.palavrasteste = self.buscapalvras(self.teste)
        self.frequenciateste = self.buscafrequencia(self.palavrasteste)
        self.palavrasunicasteste = self.buscapalavrasunicas(self.frequenciateste)

    def getBaseTeste(self):
        dados = []

        with open(self.dataPath_teste, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                dados.append((row[0], row[1]))
        return dados

    def getBase(self):
        dados = []

        with open(self.dataPath_treino, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                dados.append((row[0],row[1]))
        return dados

    def aplicastemmer(self,texto):
        stemmer = nltk.stem.RSLPStemmer()
        frasesstemming =[]
        for (palavras,emocao) in texto:
            comstemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in self.stopwordsnltk]
            frasesstemming.append((comstemming,emocao))
        return frasesstemming

    def buscapalvras(self,frases):
        todaspalvras=[]
        for (palavras,emocao) in frases:
            todaspalvras.extend(palavras)
        return todaspalvras

    def buscafrequencia(self,palavras):
        palavras = nltk.FreqDist(palavras)
        return palavras

    def buscapalavrasunicas(self,frequencia):
        freq = frequencia.keys()
        return freq

    def extratorpalavrasTreino(self,documento):
        doc = set(documento)
        caracteristicas = {}

        for palavras in self.palavrasunicastreinamento:
            caracteristicas['%s' %palavras] = (palavras in doc)
        return caracteristicas

    def treinar(self):
        basecompletaTreino = nltk.classify.apply_features(self.extratorpalavrasTreino, self.treino)
        basecompletaTeste = nltk.classify.apply_features(self.extratorpalavrasTreino,self.teste)
        classificador = nltk.NaiveBayesClassifier.train(basecompletaTreino)
        print(nltk.classify.accuracy(classificador, basecompletaTeste))
        return classificador

    def classificarProduto(self,classificador,produto):
        topicostemming = []
        stemmer = nltk.stem.RSLPStemmer()

        for (palavrastreinamento) in produto.split():
            comstem = [p for p in palavrastreinamento.split()]
            topicostemming.append(str(stemmer.stem(comstem[0])))

        novoProduto = self.extratorpalavrasTreino(topicostemming)
        return classificador.classify(novoProduto)

    def classificar(self, produto):
        classificador = self.treinar()
        produtoClassificado = self.classificarProduto(classificador,produto)
        return produtoClassificado
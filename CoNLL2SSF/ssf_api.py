import re

class SSF:
    # Initializes SSF file

    def __init__(self, sentence, relations,root,voice):

        self.sentence = sentence
        self.relations = relations
        self.rootChunk = root
        self.voice=voice

    def processSentence(self, sent_counter):
        id = 0
        internalId = 1
        prevChunk = ''
        currChunk = ''
        ssf_sentence = "<Sentence id='" + str(sent_counter) + "'>\n"
        for block in self.sentence.splitlines():
            word_list = block.split()
            currChunk = self.getChunkId(word_list[5])
            digitInChunk=re.sub("\D", "", currChunk)
            # if digitInChunk == '0':
            #     currChunk = re.sub(r'\d+', '',currChunk)
            # print(currChunk)
            featurelist = self.getFeatureList(word_list[5])
            currChunkPOS= re.sub(r'\d+', '',currChunk)
            if prevChunk != currChunk:
                internalId = 1
                id+=1
                if id!=1:
                    ssf_sentence+="\t))\n"
                if (currChunk != self.rootChunk):
                    drel = self.getDrel(currChunk)

                    ssf_sentence += str(id) + "\t((\t" + currChunkPOS + "\t<fs name='" + currChunk + "' " + drel

                else:
                    voicetype = self.getVoicetype()
                    # print('cuurr', currChunkPOS)
                    ssf_sentence += str(id) + "\t((\t" + currChunkPOS + "\t<fs name='" + currChunk +"' " + voicetype
                ssf_sentence += str(id) + "." + str(internalId) + "\t" + word_list[1] + "\t" + word_list[
                    3] + "\t<fs af='" + word_list[1] + featurelist + "' name='" + word_list[1] + "' posn='" + word_list[
                                    0] + "0'>\n"

            else:
                internalId += 1
                ssf_sentence += str(id) + "." + str(internalId) + "\t" + word_list[1] + "\t" + word_list[
                    3] + "\t<fs af='" + word_list[1]+featurelist + "' name='" + word_list[1] + "' posn='" + word_list[
                                    0] + "0'>\n"
            prevChunk = currChunk
        return ssf_sentence

    def getChunkId(self, features):
        chunkId = 'none'
        feature_list = features.split('|')
        for feature in feature_list:
            if 'chunkId' in feature:
                chunkId = feature.split('-')[1]

        return chunkId

    def getDrel(self, chunkId):
        drel = "drel='"+ self.relations[chunkId] +"'>\n"
        return drel

    def getVoicetype(self):
        voicetype = "voicetype='" + self.voice + "'>\n"
        return voicetype

    def getFeatureList(self, features):
        featurelist = ''
        feature_list = features.split('|')
        for feature in feature_list:
            if 'chunkId' not in feature:
                featurelist += ',' + feature.split('-')[1]
        return featurelist

import re


class CoNLL:
    # Initializes CoNll file. Gets the dependency relations
    # filename: name of the coNLL file : string
    def __init__(self, filename):
        fin = open(filename, 'r', encoding='UTF-8')
        f = fin.read()

        self.sentence_array = f.split("\n\n")

        fin.close()

    def idRelationMapping(self, sentence):
        index_chunk_dict = {}
        chunkid_relid_dict = {}
        root = ''
        voice = ''
        root_Id = 0
        for block in sentence.splitlines():
            word_list = block.split()
            id = word_list[0]
            chunkId = self.getChunkId(word_list[5])
            digitInChunk = re.sub("\D", "", chunkId)
            if word_list[7] == 'root' or word_list[7]=='main':
                root = chunkId
                root_Id = word_list[0]
                voice = self.getVoicetype(word_list[5])
            # If relation has ':', then replace it with '_'
            # Eg. acl:relcl, aux:pass, nsubj:pass
            elif ':' in word_list[7]:
                word_list[7] = word_list[7].replace(':', '_')
            if id not in index_chunk_dict:
                index_chunk_dict[id] = chunkId
            if chunkId not in chunkid_relid_dict:
                chunkid_relid_dict[chunkId] = {}
                chunkid_relid_dict[chunkId][word_list[6]] = word_list[7]
            else:
                if word_list[6] not in chunkid_relid_dict[chunkId]:
                    chunkid_relid_dict[chunkId][word_list[6]] = word_list[7]
                # else:
                #     chunkid_relid_dict[chunkId][word_list[6]].append({'id':word_list[6],'rel':word_list[7]})

        return index_chunk_dict, chunkid_relid_dict, root, voice, root_Id

    def getRelations(self, index_chunk_dict, chunkid_relid_dict):
        relations = {}
        for chunk, relidList in chunkid_relid_dict.items():
            if '0' not in relidList:
                for id, rel in relidList.items():
                    if index_chunk_dict[id] != chunk:
                        # relations[chunk]=id
                        # Tanya- adding this if comment will only add relation if its not present.
                        # If we assign directly without if condition, it will take last relation mapping to another chunk.
                        # This is the reason for diff error sentences. Err33 vs Err95
                        if chunk not in relations.keys():
                            relations[chunk] = rel + ":" + index_chunk_dict[id]
        return relations

    def getChunkId(self, features):
        chunkId = 'none'
        feature_list = features.split('|')
        for feature in feature_list:
            if 'chunkId' in feature:
                chunkId = feature.split('-')[1]
                if chunkId=='':
                    chunkId='none'

        return chunkId

    def getVoicetype(self, features):
        voice = ''
        feature_list = features.split('|')
        for feature in feature_list:
            if 'Voice' in feature:
                voice = feature.split('=')[1]
        return voice

from conll_api import CoNLL
from ssf_api import SSF
import os,sys

DOCUMENT_FORMAT_INITIAL = '<document id="{}_.htm.utf8.cml.V.tkn">\n<head>\n<title></title>\n<caption>Inta-chunk SSF</caption>\n<language>Hindi</language>\n<creation>\n</head>\n<body>\n<tb number = "1" segment = "no" bullet = "no">\n<foreign language = "select" writingsystem = "LTR"></foreign>\n<text>\n'
DOCUMENT_FORMAT_ENDING='</text>\n</tb>\n</body>\n</document>'
output_fname='data/SSF/{}'

#if not os.path.exists('data/SSF'):
 #   os.makedirs('data/SSF')

#path_parent=os.path.dirname(os.getcwd())
#directory = os.path.join(path_parent, 'Input_folder')


for filepath, dirs, files in os.walk('data/DS'):
    try:
        for file in files:
            #print("Processing file s{}".format(file))
            input_fname= os.path.splitext(file)[0]
            input_fpath= os.path.join(filepath, file)
            conll = CoNLL(input_fpath)
            sent_counter = 1
            rootId=''
            ssf_content = DOCUMENT_FORMAT_INITIAL.format(input_fname)
            for sentence in conll.sentence_array:
                index_chunk_dict, chunkid_relid_dict, root, voice, root_Id = conll.idRelationMapping(sentence)
                relations = conll.getRelations(index_chunk_dict, chunkid_relid_dict)
                if len(relations) > 0:
                    ssf = SSF(sentence, relations, root, voice)
                    ssf_content += ssf.processSentence(sent_counter)
                    sent_counter += 1
                    ssf_content += "\t))\n</Sentence>\n\n"
            #print(ssf_content)
            ssf_content+=DOCUMENT_FORMAT_ENDING
            f = open(output_fname.format(file), "w", encoding='UTF-8')
            f.write(ssf_content)
            f.close()
    except Exception as e:
        print(Exception.with_traceback(e))
        pass

import re
def single2multi(single_docs):
    """
    list single doc to multi docs
    """
    multi_docs = []
    for doc in single_docs:
        para_infor = {'src': doc['src'],\
                      'selected_index':doc['idx_predict'],\
                      'p_id': doc['id']}
        if doc['idx_start'] == 0:  # new paragraph
            multi_docs.append([para_infor])
        else:
            multi_docs[-1].append(para_infor)
    return multi_docs


def get_similarity(k_sent, q_sent):
    # q_sent, k_sent: list of word
    # q_sent: candidate sentence, k_sent: selected sentence
    sent1 = ' '.join(k_sent)
    sent2 = ' '.join(q_sent)
    
    sent1 = sent1.lower()
    sent2 = sent2.lower()
    sent1 = re.sub(r'[^a-zA-Z0-9 ]', '', sent1)
    sent2 = re.sub(r'[^a-zA-Z0-9 ]', '', sent2)

    set_word1 = set([w.strip() for w in sent1.split(' ')]) - {''}
    set_word2 = set([w.strip() for w in sent2.split(' ')]) - {''}

    if len(set_word2) == 0:  # ['ताज़ातरीन', 'ख़बरों', 'और', 'वीडियो', 'के', 'लिए', 'आजतक.इन', 'पर', 'आएं', '.']
        return 1
    # tính tỉ lệ từ trong câu mới đã xuất hiện trong câu đã chọn
    # to do: ngram...
    # print('set word query: ', set_word2)
    # print('set word for key: ', set_word1)
    
    similarity = len(set_word2.intersection(set_word1)) / len(set_word2)

    return similarity


def is_same_sentence(query, database, thresold=0.4):
    # query, database: sentence object (id, sent)
    max_similar = 0
    for k_sent in database:
        s = get_similarity(k_sent[1], query[1])  
        max_similar = max(s, max_similar)
    if max_similar >= thresold:
        return True
    else:
        return False


def reorder_sentence(sentences):
    """
    sentence: (id, src) => origin order
    return: sentence-reorder, paragraph segment
    """        
    sentence_ordered = list(sorted(sentences, key=lambda x: x[0]))
    segment = [int(x[0].split('_')[1]) for x in sentence_ordered]
    sentence_id = [x[0].split('_')[2] for x in sentence_ordered]

    sentence_ordered = [x[1] for x in sentence_ordered]
    return {'src': sentence_ordered, 'p_seg': segment, 's_id': sentence_id}


def truncate(multi_docs, max_token=512, debug=0):
    """
    sentence: tuple(f"{p_id}_{sent_id}", sentence) => sort sentence => sort
    """
    candidate_sentences = []  # list of sentence
    for i in range(7):  # 7 from bert
        for doc in multi_docs:
            p_id = doc['p_id']
            s_id = doc['selected_index'][i]
            n_sent = len(doc['src'])
            if s_id < n_sent:  # min = 3 word
                candidate_sentences.append((f'{p_id}_{s_id}', doc['src'][s_id]))
    # check token < 520 => ok luon, ko can lam buoc tiep theo
    total_token = sum([len(s[1]) for s in candidate_sentences])
    # print(total_token)
    if total_token <= max_token:
        if debug:
            print('Keep all!')
        return reorder_sentence(candidate_sentences)

    selected = [False] * len(candidate_sentences)
    selected_sentences = []  # list of sentence
    
    selected_sentences.append(candidate_sentences[0])  # todo: dynamic?
    selected[0] = True
    total_token_selected = len(candidate_sentences[0])
    # print(type(candidate_sentences[0]), candidate_sentences[0])
    for i in range(len(candidate_sentences)):
        if not selected[i] and not is_same_sentence(candidate_sentences[i],\
                                                    selected_sentences, thresold=0.4):
            selected[i] = True
            selected_sentences.append(candidate_sentences[i])
            total_token_selected += len(candidate_sentences[i])
            if debug:
                print('Select sentence ', i)
        if total_token_selected >= max_token:
            break
    return reorder_sentence(selected_sentences)

def transform(BIO_TAG, tokenized_sentence, sentence=None):
    sentence_raw = sentence.split()
    sentence_lower = sentence.lower().split()
    bag = zip(BIO_TAG, tokenized_sentence)
    zip_list = list(bag)

    work_index = 0
    now_index = 0
    entity_list = []
    length = len(zip_list)
    is_visited = [0] * length
    for i in range(length):
        if i == 0:
            is_visited[0] = 1
        if i is not 0 and is_visited[i] == 1:
            continue
        if zip_list[i][0] == "O":
            is_visited[i] = 1
            continue
        work_index = i
        now_index = work_index
        is_visited[now_index] = 1
        suffix = zip_list[i][0][-3:]
        temp_entity = zip_list[now_index][1]
        while (work_index + 1 < length) and (zip_list[work_index + 1][0][-3:] == suffix):
            if zip_list[work_index + 1][1] in sentence_lower:
                temp_entity = " ".join([temp_entity, str(zip_list[work_index + 1][1])])
            else:
                temp_entity += str(zip_list[work_index + 1][1]).strip('#')
            work_index += 1
            is_visited[work_index] = 1
        now_index = work_index + 1
        entity_list.append([temp_entity, suffix])

    contrast_list = []
    temp_list = []
    for item_tuple in entity_list:
        temp_list = []
        for item in item_tuple[0].split():
            temp = ""
            for item_item in item.split():
                replace_word = [x for x in sentence_raw if x.lower() == item_item].pop()
                temp = "".join([temp, replace_word])
            temp_list.append(temp)
        contrast_list.append(temp_list)

    len_entity_list = len(entity_list)
    for i in range(len_entity_list):
        entity_list[i][0] = contrast_list[i]
        entity_list[i][0] = ' '.join(entity_list[i][0])

    return entity_list


if __name__ == '__main__':
    tokens = ['ho', '##lad', '##ay', 'transferred', 'to', '<', 'e', '##1', '>', 'texas', 'christian', 'university', '<',
              '/', 'e', '##1', '>', '(', 'tc', '##u', ')', 'before', 'his', 'sophomore', 'season', 'becoming', 'the',
              'starting', 'catcher', 'for', 'the', '<', 'e', '##2', '>', 'tc', '##u', 'horned', 'frogs', '<', '/', 'e',
              '##2', '>', 'baseball', 'team']
    tags = ['B-per', 'B-per', 'B-per', 'O', 'O', 'O', 'O', 'O', 'O', 'B-org', 'I-org', 'I-org', 'O', 'O', 'O', 'O', 'O',
            'O', 'B-org', 'B-org', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-org',
            'B-org', 'I-org', 'I-org', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    sentence = 'Holaday transferred to <e1> Texas Christian University </e1> ( TCU ) \
                before his sophomore season becoming the starting catcher for the <e2> \
                TCU Horned Frogs </e2> baseball team'

    entity_list = transform(tags, tokens, sentence)
    print(entity_list)

    print('ok')
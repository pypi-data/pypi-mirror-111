def ListConversionDictionary(keys, values):
    dictionary = {}
    ListSetDictionary = []

    for key, value in zip(keys, values):
        KeyValue = dictionary.fromkeys([key], value)
        dictionary.update(KeyValue)
        ListSetDictionary.append(KeyValue)

    return dictionary, ListSetDictionary


# keys = ['姓名', '性别', '年龄', '编号']
# values = ['李志远', '男', 18, 53432]
# print(ListConversionDictionary(keys, values)[0])
# print(ListConversionDictionary(keys, values)[1])

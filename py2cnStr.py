__author__ = 'joel'


def translate(db, py):

    """

    :param db:
    :param py:
    """
    length = len(py)
    stateList = []
    path = []
    Chinese = ''
    time = 0
    for state in db['initial'].keys():
        stateList.append(state)

    waitList = WaitList(py)
    #Start the Viterbi algorithm!
    V = [{}]
    #Initialize base cases (t == 0# )
    for state in stateList:
        for pinyin in waitList.keys():
            dictKey = state + '|' + pinyin
            if dictKey in db['emission'][state].keys():
                V[0][dictKey] = db['initial'][state] + db['emission'][state][dictKey]
            else:
                continue
    opt = min(V[time])
    for key in V[time].keys():
        if V[time][opt] > V[time][key]:
            opt = key
    path.append(opt)
    position = waitList[path[time].split('|')[1]]
    lastPosition = position
    lastState = path[time].split('|')[0]
    py = py[position:]
    #run Viterbi
    while lastPosition < length:
        time += 1
        waitList = WaitList(py)
        V.append({})
        for state in stateList:
            for pinyin in waitList.keys():
                dictKey = state + '|' + pinyin
                dictKey_state = lastState + '|' + state
                if dictKey_state in db['transition'].keys():
                    if dictKey in db['emission'][state].keys():
                        V[time][dictKey] = db['transition'][dictKey_state] + db['emission'][state][dictKey]
                    else:
                        continue
                else:
                    continue
        opt = min(V[time])
        for key in V[time].keys():
            if V[time][opt] > V[time][key]:
                opt = key
        path.append(opt)
        position = waitList[path[time].split('|')[1]]
        lastState = path[time].split('|')[0]
        lastPosition += position
        py = py[position:]
    #translate to Chinese
    for i in range(0, len(path)):
        pinyin = path[i].split('|')[1]
        opt = min(db['vocabulary'][pinyin])
        for key in db['vocabulary'][pinyin].keys():
            if db['vocabulary'][pinyin][opt] > db['vocabulary'][pinyin][key]:
                opt = key
        Chinese += opt

    return Chinese


def WaitList(py):
    List = {}
    key = ''
    for position in range(0, len(py)):
        key = key + '/' + py[position]
        List[key] = position + 1
    return List
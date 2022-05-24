def loadConfigData():
    configData = {}
    configFile = open("config.txt", "r")
    for line in configFile:
        line = line.split("=")
        configData[line[0]] = line[1]
    return configData
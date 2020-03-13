
# The Reader class allows .mrc files to be iterated through, by record
# expects a file object as input
class Reader:
    def __init__(self, marcFile):
        self.marcFile = marcFile
        self.recordStart = 0 # used to trck position in file

    # required for iterator standard
    def __iter__(self):
        return self

    # required for iterator standard
    def __next__(self):
        self.marcFile.seek(self.recordStart)
        recordSize = self.marcFile.read(5) # gets record length

        if recordSize == b'': # check for EOF
            raise StopIteration

        self.marcFile.seek(self.recordStart)
        record = self.marcFile.read(int(recordSize))

        self.recordStart += int(recordSize)
        return record

# used to parse a single record into leader, directory, and data
class Parser:
    # expects a bytes type for input
    def __init__(self, record):
        self.leaderSize = 24
        self.dirEntrySize = 12

        # order matters
        self.record = record
        self.leader = self.get_leader_dict()
        self.directory = self.get_directory_list()

    def get_leader(self): # leader is first 24 octets
        leader = self.record[:self.leaderSize]
        return leader

    def get_leader_dict(self):
        leader = self.get_leader()
        leaderStr = leader.decode()
        leaderDict = {"record length": leaderStr[0:5],
                      "record status": leaderStr[5],
                      "type of record": leaderStr[6],
                      "bibliographic level": leaderStr[7],
                      "type of control": leaderStr[8],
                      "character coding scheme": leaderStr[9],
                      "indicator count": leaderStr[10],
                      "subfield code length": leaderStr[11],
                      "base address of data": leaderStr[12:17],
                      "encoding level": leaderStr[17],
                      "descriptive cataloging form": leaderStr[18],
                      "multipart resource record level": leaderStr[19],
                      "entry map": leaderStr[20:]}
        return leaderDict

    def get_directory(self): # directory is immediatrly after the leader and before variable fields
        directory = self.record[self.leaderSize:int(self.leader["base address of data"])]
        return directory

    # creates a list of dictionaries, containing info about variable fields
    def get_directory_list(self):
        dirList = list()
        directory = self.get_directory()
        dirArray = bytearray(directory)
        while len(dirArray) > 1: # remaining byte will be field terminator, \x1e or RS (record seperator)
            entry = {"tag": dirArray[:3].decode(),
                     "length of field": int(dirArray[3:7]),
                     "starting character position": int(dirArray[7:12])}
            dirList.append(entry)
            del dirArray[:self.dirEntrySize]

        return dirList

    def get_data(self): # data, or variable fields, start at the base address to the end of the record
        data = self.record[int(self.leader["base address of data"]):]
        return data

    def get_data_list(self):
        dataList = list()
        recordData = self.get_data()
        for entry in self.directory:
            start = entry["starting character position"]
            end = start + entry["length of field"]
            dataField = recordData[start:end]

            indicators = bytes()
            if int(entry["tag"]) >= 10: # control fields do not have indicators or subfields
                indicators = dataField[0:2]
                dataField = dataField[2:]
                
            dataList.append({"code": entry["tag"], "indicators": indicators,"data": dataField})
        return dataList

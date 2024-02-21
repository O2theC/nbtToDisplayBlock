import cProfile
import hashlib
import os
import re
import shutil
import time

ob = cProfile.Profile()
try:
    import PySimpleGUI as sg
    from nbt import nbt
except BaseException:
    input("not all librarys are present, press enter to install them")
    os.system("pip install PySimpleGUI==4.60.5 NBT")
    import PySimpleGUI as sg
    from nbt import nbt


def sha512(file_path):
    try:
        with open(file_path, "rb") as f:
            sha512_hash = hashlib.sha512()
            while True:
                data = f.read(8192)  # Read file in chunks of 8192 bytes
                if not data:
                    break
                sha512_hash.update(data)
            return sha512_hash.hexdigest()
    except FileNotFoundError:
        # print(f"File '{file_path}' not found.")
        return "Failed"
    except Exception as e:
        return "Failed"


nbtCache = dict()

settings = sg.UserSettings(filename="./config.json", autosave=True)

filePath = settings.get("nbtFilePath", os.getcwd())
folderPath = settings.get("datapackFolderPath", os.path.expandvars("%appdata%"))
filePath = filePath.replace("\\\\", "\\").replace("\\", "/")
folderPath = folderPath.replace("\\\\", "\\").replace("\\", "/")
settings.set("nbtFilePath", filePath)
settings.set("datapackFolderPath", folderPath)

blocksPer = settings.get("blocksPer", 1)
settings.set("blocksPer", blocksPer)

tickDelay = settings.get("tickDelay", 0)
settings.set("tickDelay", tickDelay)

speedCache = settings.get("speedCache", dict())
settings.set("speedCache", speedCache)

lengCache = settings.get("lengCache", dict())
settings.set("lengCache", lengCache)

timeLeft = "meow"
if os.path.isfile(filePath):
    try:
        try:
            fileName = (
                filePath[filePath.rindex("/") + 1 : filePath.rindex(".")]
                .lower()
                .replace(" ", "_")
            )
        except BaseException:
            fileName = filePath[filePath.rindex("/") + 1 :].lower().replace(" ", "_")
        st = time.time()
        leng = lengCache.get(fileName, "meow")
        if leng == "meow":
            sha = sha512(filePath)
            if sha in nbtCache.keys():
                nbtfile = nbtCache[sha]
            else:
                nbtfile = nbt.NBTFile(filePath)
                nbtCache[sha] = nbtfile
            # nbtfile = nbt.NBTFile(filePath)
            print("test")
            dict()["testing"] = nbtfile
            print("test work")
            leng = len(nbtfile["blocks"])
        print(leng)
        if int(tickDelay) > 0:
            sto = time.time()
            # print(f"time check took {(sto-st):.3f}")
            speedCache = settings.get("speedCache")
            speed = speedCache.get(fileName, {blocksPer: "None1"}).get(
                blocksPer, "None2"
            )
            if speed == "None1":
                speed = 300
            elif speed == "None2":
                cache = speedCache.get(fileName)
                numbers = list()
                for k in cache.keys():
                    numbers.append(int(k))
                lowDiff = 10000
                lowNum = 0
                for num in numbers:
                    diff = int(blocksPer) - num
                    if diff < 0:
                        None
                    elif diff < lowDiff:
                        lowDiff = diff
                        lowNum = num
                if lowNum == 0:
                    speed = 300
                else:
                    speed = cache[str(lowNum)]
        else:
            speed = 10000
        seconds = leng / speed
        seconds += 5
        minutes = 0
        if seconds >= 60:
            minutes = seconds // 60
            seconds = seconds % 60
        seconds = int(seconds)
        minutes = int(minutes)

        secondsBuild = ((leng / int(blocksPer)) * int(tickDelay)) / 20
        minutesBuild = 0
        if secondsBuild >= 60:
            minutesBuild = secondsBuild // 60
            secondsBuild = secondsBuild % 60
        secondsBuild = int(secondsBuild)
        minutesBuild = int(minutesBuild)
        timeLeft = f"Convert Time {minutes:02}:{seconds:02} - Building Time {minutesBuild:02}:{secondsBuild:02}"
    except Exception as e:
        print(e)

layout = [
    [
        sg.Text(".nbt File"),
        sg.Input(
            expand_x=True,
            k="nbtFilePath",
            default_text=str(
                os.path.dirname(filePath) if not os.path.isfile(filePath) else filePath
            ),
            enable_events=True,
        ),
        sg.FileBrowse(
            initial_folder=(
                os.path.dirname(filePath) if os.path.isfile(filePath) else filePath
            ),
            file_types=((".nbt file", "*.nbt"), ("all files", "*")),
            key="nbtFilePathButton",
        ),
    ],
    [
        sg.Text("Datapack folder"),
        sg.Input(
            expand_x=True,
            k="datapackFolderPath",
            default_text=str(folderPath),
            enable_events=True,
        ),
        sg.FolderBrowse(initial_folder=folderPath, key="datapackFolderPathButton"),
    ],
    [
        sg.Input(str(blocksPer), size=(10, None), key="blocksPer", enable_events=True),
        sg.Text(" blocks every "),
        sg.Input(str(tickDelay), size=(10, None), key="tickDelay", enable_events=True),
        sg.Text(" tick(s)"),
    ],
    [sg.Button("Convert"), sg.Text("", key="Info", visible=False)],
    [sg.ProgressBar(max_value=100, expand_x=True, key="bar", size=(0, 15))],
    [sg.Text(timeLeft, visible=True, key="Time"), sg.Push(), sg.Button("Exit")],
]


window = sg.Window(".nbt to display", layout=layout, resizable=True)
while True:
    event, values = window.read()
    # print("window get read")
    try:
        filePathMaybe = values["nbtFilePath"]
        folderPathMaybe = values["datapackFolderPath"]
        filePathMaybe = filePathMaybe.replace("\\\\", "\\").replace("\\", "/")
        folderPathMaybe = folderPathMaybe.replace("\\\\", "\\").replace("\\", "/")

        blocksPer = values["blocksPer"]
        tickDelay = values["tickDelay"]
        blocksPer = re.sub(r"[^0-9]", "", blocksPer)
        tickDelay = re.sub(r"[^0-9]", "", tickDelay)
        settings.set("blocksPer", blocksPer)
        settings.set("tickDelay", tickDelay)

        if os.path.isfile(filePathMaybe):
            filePath = filePathMaybe
            if not (event in ("Exit", sg.WIN_CLOSED)):
                try:
                    try:
                        fileName = (
                            filePath[filePath.rindex("/") + 1 : filePath.rindex(".")]
                            .lower()
                            .replace(" ", "_")
                        )
                    except BaseException:
                        fileName = (
                            filePath[filePath.rindex("/") + 1 :]
                            .lower()
                            .replace(" ", "_")
                        )
                    st = time.time()
                    leng = lengCache.get(fileName, "meow")
                    if leng == "meow":
                        sha = sha512(filePath)
                        if sha in nbtCache.keys():
                            nbtfile = nbtCache[sha]
                        else:
                            nbtfile = nbt.NBTFile(filePath)
                            nbtCache[sha] = nbtfile
                        leng = len(nbtfile["blocks"])
                    sto = time.time()
                    # print(f"time check took {(sto-st):.3f}")
                    speedCache = settings.get("speedCache")
                    speed = speedCache.get(fileName, {blocksPer: "None1"}).get(
                        blocksPer, "None2"
                    )
                    if speed == "None1":
                        speed = 300
                    elif speed == "None2":
                        cache = speedCache.get(fileName)
                        numbers = list()
                        for k in cache.keys():
                            numbers.append(int(k))
                        lowDiff = 10000
                        lowNum = 0
                        for num in numbers:
                            diff = int(blocksPer) - num
                            if diff < 0:
                                None
                            elif diff < lowDiff:
                                lowDiff = diff
                                lowNum = num
                        if lowNum == 0:
                            speed = 300
                        else:
                            speed = cache[str(lowNum)]

                    seconds = leng / speed
                    seconds += 5
                    minutes = 0
                    if seconds >= 60:
                        minutes = seconds // 60
                        seconds = seconds % 60
                    seconds = int(seconds)
                    minutes = int(minutes)

                    secondsBuild = ((leng / int(blocksPer)) * int(tickDelay)) / 20
                    minutesBuild = 0
                    if secondsBuild >= 60:
                        minutesBuild = secondsBuild // 60
                        secondsBuild = secondsBuild % 60
                    secondsBuild = int(secondsBuild)
                    minutesBuild = int(minutesBuild)
                    window["Time"].update(
                        value=f"Convert Time {minutes:02}:{seconds:02} - Building Time {minutesBuild:02}:{secondsBuild:02}",
                        visible=True,
                    )
                except BaseException:
                    None
            settings.set("nbtFilePath", filePath)
            window["nbtFilePathButton"].InitialFolder = (
                os.path.dirname(filePath) if os.path.isfile(filePath) else filePath
            )
            window["nbtFilePathButton"].update()
        if os.path.isdir(folderPathMaybe):
            folderPath = folderPathMaybe
            settings.set("datapackFolderPath", folderPath)
            window["datapackFolderPathButton"].InitialFolder = folderPath
            window["datapackFolderPathButton"].update()

    except BaseException:
        None

    if event in ("Exit", sg.WIN_CLOSED):
        break

    if event == "Convert":
        start = time.time()
        # if os.path.isdir(r"C:\Users\O2C\AppData\Roaming\ATLauncher\instances\Axiom\saves\New World\datapacks\nbtToBlockDisplay"):
        #     shutil.rmtree(r"C:\Users\O2C\AppData\Roaming\ATLauncher\instances\Axiom\saves\New World\datapacks\nbtToBlockDisplay")
        nbtFilePath = window["nbtFilePath"].get()
        datapackFolderPath = window["datapackFolderPath"].get()
        if not os.path.exists(nbtFilePath):
            sg.Window(
                "Path Error",
                [
                    [sg.T(".nbt file path was invaild and could not be found")],
                    [sg.Button(button_text="Ok")],
                ],
                disable_close=True,
            ).read(close=True)
            continue
        if not os.path.exists(datapackFolderPath):
            sg.Window(
                "Path Error",
                [
                    [sg.T("datapack folder path was invaild and could not be found")],
                    [sg.Button(button_text="Ok")],
                ],
                disable_close=True,
            ).read(close=True)
            continue
        try:
            blocksPer = int(window["blocksPer"].get())
        except BaseException:
            blocksPer = -1
        try:
            tickDelay = int(window["tickDelay"].get())
        except BaseException:
            tickDelay = -1
        if blocksPer <= 0:
            sg.Window(
                "Number Error",
                [
                    [sg.T('the "blocks per" value must be 1 or higher')],
                    [sg.Button(button_text="Ok")],
                ],
                disable_close=True,
            ).read(close=True)
            continue
        if tickDelay < 0:
            sg.Window(
                "Number Error",
                [
                    [sg.T('the "every __ tick(s)" value must be 0 or higher')],
                    [sg.Button(button_text="Ok")],
                ],
                disable_close=True,
            ).read(close=True)
            continue
        window["Info"].update(value="Converting, Please Wait", visible=True)
        window.read(timeout=0.01)
        if tickDelay == 0:
            oneFile = True
        else:
            oneFile = False
        try:
            fileName = (
                filePath[filePath.rindex("/") + 1 : filePath.rindex(".")]
                .lower()
                .replace(" ", "_")
            )
        except BaseException:
            fileName = filePath[filePath.rindex("/") + 1 :].lower().replace(" ", "_")
        if not os.path.isdir(os.path.join(datapackFolderPath, "nbtToBlockDisplay")):
            os.mkdir(os.path.join(datapackFolderPath, "nbtToBlockDisplay"))
            os.mkdir(os.path.join(datapackFolderPath, "nbtToBlockDisplay", "data"))
        if not os.path.isfile(
            os.path.join(datapackFolderPath, "nbtToBlockDisplay", "pack.mcmeta")
        ):
            with open(
                os.path.join(datapackFolderPath, "nbtToBlockDisplay", "pack.mcmeta"),
                "w",
            ) as f:
                mcmetaStuff = """{
    "pack": {
        "pack_format": 10,
        "description": "nbtToBlockDisplay"
    }
}"""
                f.write(mcmetaStuff)
        if not os.path.isdir(
            os.path.join(datapackFolderPath, "nbtToBlockDisplay", "data")
        ):
            os.mkdir(os.path.join(datapackFolderPath, "nbtToBlockDisplay", "data"))
        # shutil.rmtree(os.path.join(datapackFolderPath,"nbtToBlockDisplay","data",name))
        if not os.path.isdir(
            os.path.join(datapackFolderPath, "nbtToBlockDisplay", "data", fileName)
        ):
            os.mkdir(
                os.path.join(datapackFolderPath, "nbtToBlockDisplay", "data", fileName)
            )
        if not os.path.isdir(
            os.path.join(
                datapackFolderPath, "nbtToBlockDisplay", "data", fileName, "functions"
            )
        ):
            os.mkdir(
                os.path.join(
                    datapackFolderPath,
                    "nbtToBlockDisplay",
                    "data",
                    fileName,
                    "functions",
                )
            )
        if (not oneFile) and (
            not os.path.isdir(
                os.path.join(
                    datapackFolderPath,
                    "nbtToBlockDisplay",
                    "data",
                    fileName,
                    "functions",
                    "commands",
                )
            )
        ):
            os.mkdir(
                os.path.join(
                    datapackFolderPath,
                    "nbtToBlockDisplay",
                    "data",
                    fileName,
                    "functions",
                    "commands",
                )
            )
        print("folder stuff done", " - ", round(time.time() - start, 3))
        ob.enable()
        window.read(timeout=1)
        try:
            sha = sha512(filePath)
            if sha in nbtCache.keys():
                file = nbtCache[sha]
            else:
                file = nbt.NBTFile(filePath)
                nbtCache[sha] = file
        except BaseException:
            sg.Window(
                "NBT Error",
                [
                    [sg.T("the nbt file is corrupt and could not be read")],
                    [sg.Button(button_text="Ok")],
                ],
                disable_close=True,
            ).read(close=True)
            continue
        ob.disable()
        ob.dump_stats("stats")
        # print(file.keys())
        pal = file["palette"]
        blocksState = list()

        for block in pal:
            name = str(block["Name"])
            properties = dict()
            if "Properties" in block.keys():
                props = block["Properties"]
                for propK in props.keys():
                    properties[str(propK)] = str(props[propK])
            dic = dict()
            name = name.replace("minecraft:", "")
            dic["name"] = name
            dic["properties"] = properties
            blocksState.append(dic)

        # print(blocksState)
        # with open("palette.json", "w") as f:
        # f.write(json.dumps(blocksState, indent=4)) # cool looking debug file,
        # but don't need this to make this work

        # {id:"minecraft:block_display",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]},block_state:{Name:"minecraft:oak_stairs",Properties:{facing:"north"}}}
        print("got palette", " - ", round(time.time() - start, 3))
        window.read(timeout=1)
        blocks = file["blocks"]
        passengerString = ""
        commands = []
        count = 0
        for block in blocks:
            count += 1
            # print(count,"/",len(blocks))
            pos = block["pos"]
            x = int(str(pos[0]))
            y = int(str(pos[1]))
            z = int(str(pos[2]))
            # print(x," - ",y," - ",z)
            # print(block)
            stateNum = int(str(block["state"]))
            state = blocksState[stateNum]
            skip = False
            name = str(state["name"])
            if state["name"] in ("air", "jigsaw"):
                if state["name"] == "jigsaw":
                    name = str(block["nbt"]["final_state"])
                    skip = True
                else:
                    continue
            # print(state)
            if not skip and len(state["properties"]) > 0:
                propertiesString = "{"
                for prop in state["properties"].keys():
                    val = state["properties"][prop]
                    if propertiesString != "{":
                        propertiesString += ","
                    propertiesString += f'{prop}:"{val}"'
                propertiesString += "}"
            else:
                propertiesString = "{}"
            if "_bed" in name:
                if 'part:"head"' not in propertiesString:
                    continue
            xOff = x - 0.5
            yOff = y - 0.5
            zOff = z - 0.5
            blockEntitys = ["white_bed", "chest"]
            turnOffset = [0, 0, 0, 1]
            if name in blockEntitys and "facing:" in propertiesString:
                face = str(state["properties"]["facing"])
                if face == "south":
                    xOff += 0
                    yOff += 0
                    zOff += 0
                    turnOffset = [0, 0, 0, 1]
                elif face == "west":
                    xOff += 0
                    yOff += 0
                    zOff += 0
                    turnOffset = [0, -0.71, 0, 0.71]
                elif face == "north":
                    xOff += 1
                    yOff += 0
                    zOff += 1
                    turnOffset = [0, 1, 0, 0]
                elif face == "east":
                    xOff += 0
                    yOff += 0
                    zOff += 1
                    turnOffset = [0, 0.71, 0, 0.71]

            turnOffsets = (
                f"[{turnOffset[0]}f,{turnOffset[1]}f,{turnOffset[2]}f,{turnOffset[3]}f]"
            )
            spawnPos = f"~{xOff} ~{yOff} ~{zOff}"
            command = (
                "summon block_display "
                + spawnPos
                + " {transformation:{left_rotation:"
                + turnOffsets
                + ',right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[0f,0f,0f]},block_state:{Name:"'
                + name
                + '",Properties:'
                + propertiesString
                + "}}"
            )
            command = command.replace(",Properties:{}", "")
            commands.append(command)

        i = 0
        lengCache[fileName] = len(commands)
        settings.set("lengCache", lengCache)

        print("got commands", " - ", round(time.time() - start, 3))
        # print(stop-start,"\n",round(stop-start,4))
        window["bar"].update(current_count=0, max=len(commands))
        window.read(timeout=1)

        if oneFile:
            try:
                os.remove(
                    os.path.join(
                        datapackFolderPath,
                        "nbtToBlockDisplay",
                        "data",
                        fileName,
                        "functions",
                        "build_instant.mcfunction",
                    )
                )
            except BaseException:
                None
            with open(
                os.path.join(
                    datapackFolderPath,
                    "nbtToBlockDisplay",
                    "data",
                    fileName,
                    "functions",
                    "build_instant.mcfunction",
                ),
                "w",
            ) as f:
                print("ready to write commands", " - ", round(time.time() - start, 3))
                barCount = 0
                leng = len(commands)
                updateInterval = leng // window["bar"].get_size()[0]
                updateInterval = 1 if updateInterval < 1 else updateInterval
                startWrite = time.time()
                com = 0
                print(updateInterval)
                commandsString = ""
                for command in commands:
                    com += 1
                    f.write(command + "\n")
                    barCount += 1
                    # if barCount % updateInterval == 0:
                    #     # window["bar"].update(current_count=barCount)
                    #     pTime = time.time()
                    #     try:
                    #         speed = (com) / (pTime - startWrite)
                    #         seconds = (leng - (com)) / speed
                    #     except BaseException:
                    #         speed = leng - (com)
                    #         seconds = 1
                    #     minutes = 0
                    #     if seconds >= 60:
                    #         minutes = seconds // 60
                    #         seconds = seconds % 60
                    #     seconds = int(seconds)
                    #     minutes = int(minutes)
                    #     # print(f"\r{speed:04.3f}",end="")

                    #     # window["Time"].update(
                    #     #     value=f"Convert Time {minutes:02}:{seconds:02} - Building Time {minutesBuild:02}:{secondsBuild:02}",
                    #     #     visible=True,
                    #     # )
                    #     # window.read(timeout=.01)
                f.write("say Done")

            window["bar"].update(current_count=barCount)
            window.read(timeout=1)
            print("written commands", " - ", round(time.time() - start, 3))

        else:
            try:
                commandDir = os.listdir(
                    os.path.join(
                        datapackFolderPath,
                        "nbtToBlockDisplay",
                        "data",
                        fileName,
                        "functions",
                        "commands",
                    )
                )
                for thing in commandDir:
                    thingPath = os.path.join(
                        datapackFolderPath,
                        "nbtToBlockDisplay",
                        "data",
                        fileName,
                        "functions",
                        "commands",
                        thing,
                    )
                    if os.path.isfile(thingPath):
                        try:
                            num = thing[: thing.rindex(".")]
                            num = int(num)
                            if num >= (len(commands)/blocksPer):
                                os.remove(thingPath)
                        except BaseException:
                            print(thingPath)
            except BaseException:
                None
            try:
                os.mkdir(
                    os.path.join(
                        datapackFolderPath,
                        "nbtToBlockDisplay",
                        "data",
                        fileName,
                        "functions",
                        "commands",
                    )
                )
            except BaseException:
                None
            print("ready to write commands", " - ", round(time.time() - start, 3))
            num = 1
            com = 0
            leng = len(commands)
            blocksPer
            tickDelay
            barCount = 0
            # for meow in range(blocksPer):
            #     if(meow < len(commands)):
            #         commands[meow] = f"execute positioned 0. 88 0. run {commands[meow]}"
            updateInterval = leng // window["bar"].get_size()[0]
            updateInterval = 1 if updateInterval < 1 else updateInterval
            startWrite = time.time()
            with open(
                os.path.join(
                    datapackFolderPath,
                    "nbtToBlockDisplay",
                    "data",
                    fileName,
                    "functions",
                    "build_delayed.mcfunction",
                ),
                "w",
            ) as f:
                # python doesn't like it if i stack this in the line below, so i use a
                # var to seperate them
                standNBT = (
                    "{"
                    + f'NoGravity:1b,Tags:["{fileName}.1"],Marker:1b,Invisible:1b'
                    + "}"
                )
                f.write(f"summon armor_stand ~ ~ ~ {standNBT}\n")
                f.write(f"schedule function {fileName}:commands/1 1t\n")
            secondsBuild = ((leng / int(blocksPer)) * int(tickDelay)) / 20
            minutesBuild = 0
            if secondsBuild >= 60:
                minutesBuild = secondsBuild // 60
                secondsBuild = secondsBuild % 60
            secondsBuild = int(secondsBuild)
            minutesBuild = int(minutesBuild)
            while com < leng:
                with open(
                    os.path.join(
                        datapackFolderPath,
                        "nbtToBlockDisplay",
                        "data",
                        fileName,
                        "functions",
                        "commands",
                        f"{num}.mcfunction",
                    ),
                    "w",
                ) as f:
                    for _ in range(blocksPer):
                        if com >= leng:
                            f.write("say Done\n")
                            f.write(
                                f"execute as @e[tag={fileName}.{num}] run kill @s\n"
                            )
                            break
                        f.write(
                            f"execute as @e[tag={fileName}.{num}] at @s run {commands[com]}\n"
                        )
                        barCount += 1
                        if barCount % updateInterval == 0:
                            window["bar"].update(current_count=barCount)
                            pTime = time.time()
                            try:
                                speed = (com) / (pTime - startWrite)
                                seconds = (leng - (com)) / speed
                            except BaseException:
                                speed = leng - (com)
                                seconds = 1
                            minutes = 0
                            if seconds >= 60:
                                minutes = seconds // 60
                                seconds = seconds % 60
                            seconds = int(seconds)
                            minutes = int(minutes)
                            # print(f"\r{speed:04.3f}",end="")

                            window["Time"].update(
                                value=f"Convert Time {minutes:02}:{seconds:02} - Building Time {minutesBuild:02}:{secondsBuild:02}",
                                visible=True,
                            )
                            window.read(timeout=1)
                        com += 1
                    f.write(
                        f"execute as @e[tag={fileName}.{num}] run tag @s add {fileName}.{num+1}\n"
                    )
                    f.write(
                        f"execute as @e[tag={fileName}.{num}] run tag @s remove {fileName}.{num}\n"
                    )
                    f.write(
                        f"schedule function {fileName}:commands/{num+1} {tickDelay}t\n"
                    )
                num += 1
            window["bar"].update(current_count=barCount)
            window.read(timeout=1)

            print("written commands", " - ", round(time.time() - start, 3))

        stopWrite = time.time()
        print(
            f"Writen {len(commands)} commands in {round(stopWrite-startWrite,3)} seconds\n{round(len(commands)/(stopWrite-startWrite),3)} commands per second"
        )
        speed = len(commands) / (stopWrite - startWrite)
        speedCache = settings.get("speedCache", dict())
        speedCache[fileName] = speedCache.get(fileName, dict())
        speedCache[fileName][blocksPer] = speed
        settings.set("speedCache", speedCache)
        try:
            leng = len(commands)
            seconds = leng / speed
            seconds += 5
            minutes = 0
            if seconds >= 60:
                minutes = seconds // 60
                seconds = seconds % 60
            seconds = int(seconds)
            minutes = int(minutes)
            secondsBuild = ((leng / int(blocksPer)) * int(tickDelay)) / 20
            minutesBuild = 0
            if secondsBuild >= 60:
                minutesBuild = secondsBuild // 60
                secondsBuild = secondsBuild % 60
            secondsBuild = int(secondsBuild)
            minutesBuild = int(minutesBuild)
            window["Time"].update(
                value=f"Convert Time {minutes:02}:{seconds:02} - Building Time {minutesBuild:02}:{secondsBuild:02}",
                visible=True,
            )
        except BaseException:
            None
        window["Info"].update(value="Finished", visible=True)
        window.read(timeout=0.01)
        # with open(f"commandsTest.mcfunction", "w") as f:
        #     for command in commands:
        #         f.write(command + "\n")

        # try:
        #     shutil.rmtree("commands")
        # except BaseException:
        #     None
        # os.mkdir("./commands")
        # for command in commands:
        #     with open(f"commands/command{i}.mcfunction", "w") as f:
        #         f.write(command + "\n")
        #         f.write(f"function cat:commands/command{i+1}")
        #     i += 1
        # try:
        #     shutil.rmtree(
        #         "C:/Users/O2C/AppData/Roaming/ATLauncher/instances/Axiom/saves/New World/datapacks/nbtConvert/data/cat/functions/commands"
        #     )
        # except BaseException:
        #     None

        # shutil.copytree(
        #     "./commands",
        #     "C:/Users/O2C/AppData/Roaming/ATLauncher/instances/Axiom/saves/New World/datapacks/nbtConvert/data/cat/functions/commands",
        # )

    if event == "blocksPer":
        if (
            re.sub(r"[^0-9]", "", window["blocksPer"].get())
            != window["blocksPer"].get()
        ):
            window["blocksPer"].update(
                value=re.sub(r"[^0-9]", "", window["blocksPer"].get())
            )
    if event == "tickTimer":
        if (
            re.sub(r"[^0-9]", "", window["tickTimer"].get())
            != window["tickTimer"].get()
        ):
            window["tickTimer"].update(
                value=re.sub(r"[^0-9]", "", window["tickTimer"].get())
            )

    filePathInput = window["nbtFilePath"].get()
    folderPathInput = window["datapackFolderPath"].get()
    filePathInput = filePathInput.replace("\\\\", "\\").replace("\\", "/")
    folderPathInput = folderPathInput.replace("\\\\", "\\").replace("\\", "/")
    (
        window["nbtFilePath"].update(value=filePathInput)
        if filePathInput != window["nbtFilePath"].get()
        else None
    )
    (
        window["datapackFolderPath"].update(value=folderPathInput)
        if folderPathInput != window["datapackFolderPath"].get()
        else None
    )

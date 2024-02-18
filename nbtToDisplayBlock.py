import os
import re
import shutil
import time
try:
    import PySimpleGUI as sg
    from nbt import nbt
except:
    input("not all librarys are present, press enter to install them")
    os.system("pip install PySimpleGUI==4.60.5 NBT")
    import PySimpleGUI as sg
    from nbt import nbt


def convertNBT(
    filePath,
):
    None


settings = sg.UserSettings(filename="./config.json", autosave=True)

filePath = settings.get("nbtFilePath", os.getcwd())
folderPath = settings.get("datapackFolderPath", os.path.expandvars("%appdata%"))
filePath = filePath.replace("\\\\", "\\").replace("\\", "/")
folderPath = folderPath.replace("\\\\", "\\").replace("\\", "/")
settings.set("nbtFilePath", filePath)
settings.set("datapackFolderPath", folderPath)


layout = [
    [
        sg.Text(".nbt File"),
        sg.Input(
            expand_x=True,
            k="nbtFilePath",
            default_text=str(
                os.path.dirname(filePath) if not os.path.isfile(filePath) else filePath
            ),
        ),
        sg.FileBrowse(
            initial_folder=(
                os.path.dirname(filePath) if os.path.isfile(filePath) else filePath
            ),
            file_types=((".nbt file", "*.nbt"), ("all files", "*")),
        ),
    ],
    [
        sg.Text("Datapack folder"),
        sg.Input(expand_x=True, k="datapackFolderPath", default_text=str(folderPath)),
        sg.FolderBrowse(initial_folder=folderPath),
    ],
    [
        sg.Input("1", size=(10, None), key="blocksPer", enable_events=True),
        sg.Text(" blocks every "),
        sg.Input("0", size=(10, None), key="tickTimer", enable_events=True),
        sg.Text(" tick(s)"),
    ],
    [sg.Button("Convert")],
    [sg.ProgressBar(max_value=100, expand_x=True, key="bar", size=(0, 15))],
    [sg.Push(), sg.Button("Exit")],
]


window = sg.Window(".nbt to display", layout=layout, resizable=True)
while True:
    event, values = window.read()
    try:
        filePathMaybe = values["nbtFilePath"]
        folderPathMaybe = values["datapackFolderPath"]
        filePathMaybe = filePathMaybe.replace("\\\\", "\\").replace("\\", "/")
        folderPathMaybe = folderPathMaybe.replace("\\\\", "\\").replace("\\", "/")
        if os.path.isfile(filePathMaybe):
            filePath = filePathMaybe
            settings.set("nbtFilePath", filePath)
        if os.path.isdir(folderPathMaybe):
            folderPath = folderPathMaybe
            settings.set("datapackFolderPath", folderPath)
    except:
        None

    if event in ("Exit", sg.WIN_CLOSED):
        break

    if event == "Convert":
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
        except:
            blocksPer = -1
        try:
            tickTimer = int(window["tickTimer"].get())
        except:
            tickTimer = -1
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
        if tickTimer < 0:
            sg.Window(
                "Number Error",
                [
                    [sg.T('the "every __ tick(s)" value must be 0 or higher')],
                    [sg.Button(button_text="Ok")],
                ],
                disable_close=True,
            ).read(close=True)
            continue
        start = time.time()
        if tickTimer == 0:
            oneFile = True
        else:
            oneFile = False
        fileName = (
            filePath[filePath.rindex("/") + 1 : filePath.rindex(".")]
            .lower()
            .replace(" ", "_")
        )
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
        print("folder stuff done"," - ",round(time.time()-start,3))
        file = nbt.NBTFile(filePath)
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
        #     f.write(json.dumps(blocksState, indent=4)) # cool looking debug file, but don't need this to make this work

        # {id:"minecraft:block_display",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]},block_state:{Name:"minecraft:oak_stairs",Properties:{facing:"north"}}}
        print("got palette"," - ",round(time.time()-start,3))
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
        print("got commands"," - ",round(time.time()-start,3))
        # print(stop-start,"\n",round(stop-start,4))
        window["bar"].update(current_count = 0,max = len(commands))
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
                        "build.mcfunction",
                    )
                )
            except:
                None
            with open(
                os.path.join(
                    datapackFolderPath,
                    "nbtToBlockDisplay",
                    "data",
                    fileName,
                    "functions",
                    "build.mcfunction",
                ),
                "w",
            ) as f:
                barCount = 0
                for command in commands:
                    f.write(command + "\n")
                    barCount+=1
                    if(barCount%100 == 0):
                        window["bar"].update(current_count = barCount)
                        window.read(timeout=1)
                f.write("say Done")
                
                
            window["bar"].update(current_count = barCount)
            window.read(timeout=1)
            print("written commands"," - ",round(time.time()-start,3))
            
        else:
            try:
                shutil.rmtree(
                    os.path.join(
                        datapackFolderPath,
                        "nbtToBlockDisplay",
                        "data",
                        fileName,
                        "functions",
                        "commands",
                    )
                )
            except:
                None
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
            num = 1
            com = 0
            leng = len(commands)
            blocksPer
            tickTimer
            barCount = 0
            for meow in range(blocksPer):
                if(meow < len(commands)):
                    commands[meow] = f"execute positioned 0. 88 0. run {commands[meow]}"
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
                            break
                        f.write(str(commands[com]) + "\n")
                        barCount+=1
                        if(barCount%100 == 0):
                            window["bar"].update(current_count = barCount)
                            window.read(timeout=1)
                        com += 1
                    f.write(f"schedule function {fileName}:commands/{num+1} {tickTimer}t")
                num += 1
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
                f.write("say Done")
            window["bar"].update(current_count = barCount)
            window.read(timeout=1)
            
            print("written commands"," - ",round(time.time()-start,3))

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
        window["blocksPer"].update(
            value=re.sub(r"[^0-9]", "", window["blocksPer"].get())
        )
    if event == "tickTimer":
        window["tickTimer"].update(
            value=re.sub(r"[^0-9]", "", window["tickTimer"].get())
        )

    filePathInput = window["nbtFilePath"].get()
    folderPathInput = window["datapackFolderPath"].get()
    filePathInput = filePathInput.replace("\\\\", "\\").replace("\\", "/")
    folderPathInput = folderPathInput.replace("\\\\", "\\").replace("\\", "/")
    window["nbtFilePath"].update(value=filePathInput)
    window["datapackFolderPath"].update(value=folderPathInput)

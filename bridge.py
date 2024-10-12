"""
 * The MIT License
 *
 * Copyright (c) 2024 Patrick Hammer
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 * """

#BRIDGE HANDLES NACE-NARS connection with MeTTa (for the world=9 demo)
import sys
import os

def BRIDGE_INIT(widthval, heightval, BOARDval, SetNACEPlanningObjectiveVal):
    global width, height, BOARD, SetNACEPlanningObjective
    width = widthval
    height = heightval
    BOARD = BOARDval
    SetNACEPlanningObjective = SetNACEPlanningObjectiveVal

useONA = False #whether to use OpenNARS-for-Applications instead of MeTTa-NARS for world=9
useNarsese=False
if "ona" in sys.argv:
    useONA = True
if "narsese" in sys.argv:
    useONA = True
    useNarsese = True

if useONA:
    mettanars = os.path.abspath('../OpenNARS-for-Applications/misc/Python')
    sys.path.append(mettanars)
    cwd = os.getcwd()
    os.chdir(mettanars)
    from MeTTa import *
    os.chdir(cwd)
else:
    mettanars = os.path.abspath('../metta-morph/metta-nars/')
    sys.path.append(mettanars)
    cwd = os.getcwd()
    os.chdir(mettanars)
    from NAR import *
    os.chdir(cwd)

def groundedGoal(METTA):
    #s,p,yoff,xoff = groundedFunction(METTA)
    #((S x P) --> left)
    pred = METTA.split("--> ")[1].split(")")[0]
    if pred not in ["left", "right", "up", "down"]:
        exceptionThrown = 1/0 #TODO return flag
    S = METTA.split("(!: (((")[1].split(" x")[0]
    P = METTA.split(" x ")[1].split(")")[0]
    yoffset = "y+1"
    xoffset = "x"
    if pred == "up":
        yoffset = "y-1"
        xoffset = "x"
    if pred == "down":
        yoffset = "y+1"
        xoffset = "x"
    if pred == "left":
        yoffset = "y"
        xoffset = "x-1"
    if pred == "right":
        yoffset = "y"
        xoffset = "x+1"
    print("GROUNDING DEBUG:", S, P, yoffset, xoffset)
    STR = f"lambda world: any( world[0][{yoffset}][{xoffset}] == '{S}' and world[0][y][x] == '{P}' for x in range(1, width-1) for y in range(1, height-1))"
    print("FUNC:", STR)
    FUNC = eval(STR)
    return FUNC

def groundedBelief(METTA, observed_world):
    pred = METTA.split("--> ")[1].split(")")[0]
    S = METTA.split("(.: (((")[1].split(" x")[0]
    P = METTA.split(" x ")[1].split(")")[0]
    #print("DEBUG", S, P); input()
    yoffset = 1
    xoffset = 0
    if pred == "up":
        yoffset = +1
        xoffset = 0
    if pred == "down":
        yoffset = -1
        xoffset = 0
    if pred == "left":
        yoffset = 0
        xoffset = -1
    if pred == "right":
        yoffset = 0
        xoffset = +1
    for x in range(1,width-1):
        for y in range(1,height-1):
            if observed_world[BOARD][y][x] == S:
                 observed_world[BOARD][y+yoffset][x+xoffset] = P
            if observed_world[BOARD][y][x] == P:
                observed_world[BOARD][y-yoffset][x-xoffset] = S

def BRIDGE_Input(METTA, observed_world, NACEToNARS=False, ForceMeTTa=False): #can now also be Narsese
    if METTA.startswith("!") or METTA.endswith("! :|:") or METTA.endswith(". :|:") or METTA.endswith(".") or METTA.endswith("?") or METTA.endswith("? :|:"):
        GOAL = "AddGoalEvent" in METTA or METTA.endswith("! :|:")
        METTA = METTA.replace("AddGoalEvent", "AddBeliefEvent").replace("! :|:", ". :|:")
        useNarseseNow = useNarsese and not ForceMeTTa
        if useNarseseNow:
            METTA2 = NAR_NarseseToMeTTa(METTA)
        else:
            METTA2 = METTA
        atomic_terms = [x for x in METTA2.replace("AddBeliefEvent", "").replace(" x ", " ").replace("(", " ").replace(")", " ").replace("!", "").replace("-->","").split(" ") if x != ""]
        connectors = ["-->", "IntSet", "<->", "<=>"]
        with open("knowledge.metta") as f:
            backgroundknowledge = f.read()
        for belief in backgroundknowledge.split("\n"):
            if belief != "" and not belief.startswith(";"):
                for atomic_term in atomic_terms:
                    if atomic_term != "AddBeliefEvent" and atomic_term != "" and atomic_term not in connectors and ("(" + atomic_term + " " in belief or "(" + atomic_term + " " in belief) and not atomic_term.replace(".","").isnumeric():
                        NAR_AddInput(belief)
                        break
        if useNarseseNow:
            NAR_SetUseNarsese(True) #bypass metta translation in this case
            ret = NAR_AddInput(METTA)
            NAR_SetUseNarsese(False)
        else:
            ret = NAR_AddInput(METTA)
        if NACEToNARS:
            return
        tasks = ret["input"] + ret["derivations"]
        ret = NAR_Cycle(2)
        tasks += (ret["input"] + ret["derivations"])
        processGoals = True
        for taskdict in tasks:
            if 'metta' not in taskdict:
                #print("NOT INCLUDED", taskdict); input() TODO FIX
                continue
            task = taskdict['metta'].replace(" * ", " x ")  #transformation only needed for Narsese version
            if "$1" in task or "#1" in task or "<=>" in task or "==>" in task or "=/>" in task or "/1" in task or "/2" in task: #check only needed for Narsese version
                continue
            if GOAL: #"(!:" in task:
                task = task.replace("(.:", "(!:")
                print("!!!!!TASK", task)
                try:
                    if processGoals:
                        SetNACEPlanningObjective(groundedGoal(task))
                        processGoals = False
                        print("TASK ACCEPTED")
                except:
                    print("TASK REJECTED")
                    None
            elif "(.:" in task:
                print("!!!!!TASK", task)
                try:
                    groundedBelief(task, observed_world)
                    print("TASK ACCEPTED")
                except:
                    print("TASK REJECTED")
                    None

def observeSpatialRelation(y,x, observed_world, horizontal=True, vertical=True):
    board = observed_world[BOARD]
    if horizontal:
        valueMid = board[y][x]
        valueLeft = board[y][x-1]
        valueRight = board[y][x+1]
        MeTTaL = f"!(AddBeliefEvent ((({valueRight} x {valueMid}) --> right) (1.0 0.90)))"
        MeTTaR = f"!(AddBeliefEvent ((({valueLeft} x {valueMid}) --> left) (1.0 0.90)))"
        if valueRight != " " and valueMid != " ":
            BRIDGE_Input(MeTTaL, observed_world, NACEToNARS = True, ForceMeTTa = True)
        if valueRight != " " and valueMid != " " and valueLeft != " ":
            if useONA:
                NAR_SetUseNarsese(True)
                NAR_AddInput("*concurrent")
                NAR_SetUseNarsese(False)
        if valueMid != " " and valueLeft != " ":
            BRIDGE_Input(MeTTaR, observed_world, NACEToNARS = True, ForceMeTTa = True)
    if vertical:
        valueMid = board[y][x]
        valueUp = board[y-1][x]
        valueDown = board[y+1][x]
        MeTTaD = f"!(AddBeliefEvent ((({valueDown} x {valueMid}) --> down) (1.0 0.90)))"
        MeTTaU = f"!(AddBeliefEvent ((({valueUp} x {valueMid}) --> up) (1.0 0.90)))"
        if valueUp != " " and valueMid != " ":
            BRIDGE_Input(MeTTaU, observed_world, NACEToNARS = True, ForceMeTTa = True)
        if valueUp != " " and valueMid != " " and valueDown != " ":
            if useONA:
                NAR_SetUseNarsese(True)
                NAR_AddInput("*concurrent")
                NAR_SetUseNarsese(False)
        if valueMid != " " and valueDown != " ":
            BRIDGE_Input(MeTTaD, observed_world, NACEToNARS = True, ForceMeTTa = True)

def BRIDGE_observationToNARS(observed_world):
    agent = False
    for x in range(1,width-1):
        for y in range(1,height-1):
            if observed_world[BOARD][y][x] == 'x': #AGENT
                agent_x, agent_y = (x,y)
                agent = True
                observeSpatialRelation(y, x, observed_world)
                break
        if agent:
            break

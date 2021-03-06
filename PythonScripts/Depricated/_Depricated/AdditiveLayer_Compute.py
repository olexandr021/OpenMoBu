

####################################################
#
#   AdditiveLayer_Compute.py
#
#  Script makes take 002 looks like take 001
#       by writing additive information into layer 1
#
# Author Sergey Solohin (Neill) 2017
#   e-mail to: s@neill3d.com
# Homepage: www.neill3d.com
#
# NOTE: you should have 2 takes and 2 animation layers
# 
##################################################

from pyfbsdk import *
from pyfbsdk_additions import *

gModels = []
gInitTM = []
gResultTM = []

lSystem = FBSystem()
lApp = FBApplication()
lPlayer = FBPlayerControl()

# let character put in stance pose
lCharacter = lApp.CurrentCharacter

######################################################################
## Functions

def appendModelList( pModel ):
    
    gModels.append(pModel)
    gInitTM.append( FBMatrix() )
    gResultTM.append( FBMatrix() )
    
    for child in pModel.Children:
        appendModelList( child )


def GrabInitTM(initList):

    matrix = FBMatrix()
    
    for model, listElem in zip(gModels, initList):
 
        model.GetMatrix(listElem, FBModelTransformationType.kModelTransformation, False)

def SetResult(initList):

    pTime = FBTime()
    pTime = lSystem.LocalTime
    
    for model, theMatrix in zip(gModels, initList):
 
        model.SetMatrix(theMatrix, FBModelTransformationType.kModelTransformation, False)
        
        t = FBVector4d()
        r = FBVector3d()
        s = FBSVector()
    
        FBMatrixToTRS(t, r, s, theMatrix)
        
        # rotation part
        lAnimProp = model.Rotation
        lRotNode = lAnimProp.GetAnimationNode()
                
        if lRotNode:
            lRotNode.Nodes[0].KeyAdd( pTime, r[0] )
            lRotNode.Nodes[1].KeyAdd( pTime, r[1] )
            lRotNode.Nodes[2].KeyAdd( pTime, r[2] )
    
        # translation part
        lAnimProp = model.Translation
        lMoveNode = lAnimProp.GetAnimationNode()
    
        if lMoveNode:
            lMoveNode.Nodes[0].KeyAdd( pTime, t[0] )
            lMoveNode.Nodes[1].KeyAdd( pTime, t[1] )
            lMoveNode.Nodes[2].KeyAdd( pTime, t[2] ) 

def EvalOneFrame(lTime):
    
    lPlayer.Goto(lTime)
    
    # get target poses
    currTake = lSystem.Scene.Takes[1]
    lSystem.CurrentTake = currTake
    currTake.SetCurrentLayer(1)
    lSystem.Scene.Evaluate()                
    
    SetResult(gInitTM)
    
    # our models are already selected 
    lPlayer.Key()
    
###################################################################
## MAIN

def OnButtonComputeClick(control, event):
    
    if lCharacter is not None:
        #lCharacter.GoToStancePose(False, True)
    
        startIndex = FBBodyNodeId.kFBHipsNodeId
        rootModel = lCharacter.GetModel(FBBodyNodeId(startIndex))
    
        # allocate storage for character models
        appendModelList(rootModel)
    
        # select our models to key them each frame  
        modelList = FBModelList()
        FBGetSelectedModels(modelList)
        for model in modelList:
            model.Selected = False
        
        for model in gModels:
            model.Selected = True
        
        currTake = lSystem.Scene.Takes[1]
        lSystem.CurrentTake = currTake
        numberOfLayers = currTake.GetLayerCount()
        if numberOfLayers < 2:
            currTake.CreateNewLayer()
        
        lTime = FBTime()
        lStartFrame = lPlayer.LoopStart.GetFrame()
        lStopFrame = lPlayer.LoopStop.GetFrame()
    
        lProgress = FBProgress()
        lProgress.ProgressBegin()
        lProgress.Caption = 'Computing an additive layer'
        lProgress.Percent = 0
        
        lApp.UpdateAllWidgets()
        lApp.FlushEventQueue()
        
        # get initial poses
        currTake = lSystem.Scene.Takes[0]
        lSystem.CurrentTake = currTake
        currTake.SetCurrentLayer(0)
        lSystem.Scene.Evaluate()
    
        GrabInitTM(gInitTM)
        
        for lFrame in range(lStartFrame, lStopFrame+1):
    
            lTime.SetTime( 0,0,0, lFrame)
            EvalOneFrame(lTime)
    
            if True == lProgress.UserRequestCancell():
                break
            
            p = 100.0 * lFrame / (lStopFrame-lStartFrame)
            lProgress.Percent = int(p)
            
        lProgress.ProgressDone()
        '''
        # deselect models
        FBGetSelectedModels(modelList)
        for model in modelList:
            model.Selected = False
        '''
    
def PopulateLayout(mainLyt):
    
    # Create Main region frame:
    x = FBAddRegionParam(5,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(5,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(-5,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(-5,FBAttachType.kFBAttachBottom,"")
    
    main = FBVBoxLayout()
    mainLyt.AddRegion("main","main", x, y, w, h)
    mainLyt.SetControl("main",main)

    b = FBLabel()
    b.Caption = 'Choose a base pose take'
    main.Add(b, 24)
    
    b = FBList()
    b.Style = FBListStyle.kFBDropDownList
    main.Add(b, 24)
    
    b = FBLabel()
    b.Caption = 'Choose an animation take'
    main.Add(b, 24)
    
    b = FBList()
    b.Style = FBListStyle.kFBDropDownList
    main.Add(b, 24)
    
    b = FBLabel()
    b.Caption = ''
    main.Add(b, 24)
    
    b = FBButton()
    b.Caption = 'Compute Additive'
    main.Add(b, 24)
    
gDEVELOPMENT = True
    
def CreateTool():    
    print "create tool"
    global t
    
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("Additive Animation Tool")
    PopulateLayout(t)
    t.StartSizeX = 200
    t.StartSizeY = 200
    
    if gDEVELOPMENT:
        ShowTool(t)

CreateTool()
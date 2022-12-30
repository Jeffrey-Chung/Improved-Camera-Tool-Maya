# ala_cameraTools.0.03.py
# This tool creates a camera based on a real lworld camera, and lets user set Arri Master Prime focal lengths.

import maya.cmds as cmds

#function to get selected camera on the outliner
def getSelectedCamera():
    for each_camera_transform in cmds.ls(sl=True): #loop over all cameras that are selected (transform node)
        camera_shape = cmds.listRelatives(each_camera_transform,type="camera") #find the shape node
        if camera_shape: #only set attr if a camera shape was found 
            return camera_shape[0] #return shape node
    return None 
    
# creates an AlexaLF camera and sets the film back. Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
def createCamera():
    cameraName = cmds.camera(n = "ShotCamera", horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)


# Sets the camera Aperature made by the pipeline to match an AlexaLF camera. And sets the scene Render Settings to HD.
def alexaCamera():
    cmds.setAttr(getSelectedCamera()+".horizontalFilmAperture", 1.247)
    cmds.setAttr(getSelectedCamera()+".verticalFilmAperture", 0.702)
    cmds.setAttr(getSelectedCamera()+".farClipPlane", 100000)
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)

#Set the focal length of the camera
def adjustFocalLength(focalLength):
    cmds.setAttr(getSelectedCamera()+".fl", focalLength)
  
         
def addDepthofField():
    shotCamera = getSelectedCamera()
    cmds.setAttr(shotCamera+".depthOfField", True) #Set DOF to be true
    cmds.setAttr(shotCamera+".locatorScale", 30) #Set to a larger locator scale instead of manualling scaling the camera
    cmds.distanceDimension(sp=(0, 0, 0), ep=(-38.579, -21.701, -82.295)) #Use distance tool to create 2 locators between camera and object
    cmds.parent('locator1', shotCamera, r=True) #parent first locator under the selected camera
    cmds.rename('locator2', 'AimLocator') #rename locator closer to the object to 'AimLocator'
    cmds.connectAttr('distanceDimensionShape1.distance', shotCamera+'.focusDistance') #connect distance attribute of distance dimension to focus distance of camera so that DOF can be varied
    #do the same for arnold render view
    cmds.setAttr(shotCamera + ".aiEnableDOF", True)
    cmds.setAttr(shotCamera + ".aiApertureSize", 2.8)
    cmds.connectAttr('distanceDimensionShape1.distance', shotCamera+'.aiFocusDistance')
    
         
            



def cameraTools():
    if cmds.window('cameraTools', exists = True):
        cmds.deleteUI('cameraTools')
        
    cmds.window('cameraTools', resizeToFitChildren=True, menuBar=True)

    cmds.columnLayout(adjustableColumn = True, bgc = [0, 1, 1])
      
    cmds.separator(h=30)
    cmds.text('PREVIS: Creates an AlexaLF camera')
    cmds.text('Sets the correct render settings')
    cmds.separator(h=30)
    
    cmds.button(label = 'Create Camera', command = 'createCamera()', width = 100, height = 100, bgc = [1, 1, 1])

    cmds.separator(h=50)
    cmds.text('LAYOUT: Sets AlexaLF Settings')
    cmds.separator(h=50)
    
    cmds.button(label = 'AlexaLF Settings', command = 'alexaCamera()', width=100, height=100, bgc = [1, 1, 1])
    
    cmds.separator(h=50)
    cmds.text('Depth of Field: Set DOF Rig')
    cmds.separator(h=50)
    
    cmds.button(label = 'DOF Settings', command = 'addDepthofField()', width=100, height=100, bgc = [1, 1, 1])

    cmds.menu(label = "Set Focal Length on Selected Cameras", tearOff = True)
    cmds.menuItem(label = '12mm', command = 'adjustFocalLength(12)')
    cmds.menuItem(label = '14mm', command = 'adjustFocalLength(14)')
    cmds.menuItem(label = '16mm', command = 'adjustFocalLength(16)')
    cmds.menuItem(label = '18mm', command = 'adjustFocalLength(18)')
    cmds.menuItem(label = '21mm', command = 'adjustFocalLength(21)')
    cmds.menuItem(label = '25mm', command = 'adjustFocalLength(25)')
    cmds.menuItem(label = '27mm', command = 'adjustFocalLength(27)')
    cmds.menuItem(label = '32mm', command = 'adjustFocalLength(32)')
    cmds.menuItem(label = '35mm', command = 'adjustFocalLength(35)')
    cmds.menuItem(label = '40mm', command = 'adjustFocalLength(40)')
    cmds.menuItem(label = '50mm', command = 'adjustFocalLength(50)')
    cmds.menuItem(label = '65mm', command = 'adjustFocalLength(65)')
    cmds.menuItem(label = '75mm', command = 'adjustFocalLength(75)')
    cmds.menuItem(label = '100mm', command = 'adjustFocalLength(100)')
    cmds.menuItem(label = '135mm', command = 'adjustFocalLength(135)')
    cmds.menuItem(label = '150mm', command = 'adjustFocalLength(150)')
    
    cmds.showWindow('cameraTools')
   
cameraTools()


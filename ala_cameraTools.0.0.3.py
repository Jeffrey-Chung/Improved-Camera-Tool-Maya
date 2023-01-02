# ala_cameraTools.0.03.py
# This tool creates a camera based on a real lworld camera, and lets user set Arri Master Prime focal lengths.

import maya.cmds as cmds

#function to get selected camera shape on the outliner
def getSelectedCameraShape():
    for each_camera_transform in cmds.ls(sl=True): #loop over all cameras that are selected (transform node)
        camera_shape = cmds.listRelatives(each_camera_transform,type="camera") #find the shape node
        if camera_shape: #only set attr if a camera shape was found 
            return camera_shape[0] #return shape node
    return None 

#function to get selected camera transform on the outliner
def getSelectedCameraTransform():
    cameraTransform = cmds.listRelatives(getSelectedCameraShape(), parent=True) #find the camera shape's parent to get its transform
    return cameraTransform[0] #return the transform node
        
            
#set default resolution to 1920 * 1080 and aspect ratio
def setDefaultSettings():
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)
    

# creates an AlexaLF camera and sets the film back. Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
def createCamera():
    cameraName = cmds.camera(n = "ShotCamera", horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    setDefaultSettings()


# Sets the camera Aperature made by the pipeline to match an AlexaLF camera. And sets the scene Render Settings to HD.
def alexaCamera():
    cmds.setAttr(getSelectedCameraShape()+".horizontalFilmAperture", 1.247)
    cmds.setAttr(getSelectedCameraShape()+".verticalFilmAperture", 0.702)
    cmds.setAttr(getSelectedCameraShape()+".farClipPlane", 100000)
    setDefaultSettings()

#Set the focal length of the camera
def adjustFocalLength(focalLength):
    cmds.setAttr(getSelectedCameraShape()+".fl", focalLength)
    
#Set the locator scale of the camera
def adjustLocatorScale(locatorScale):
    cmds.setAttr(getSelectedCameraShape()+".locatorScale", locatorScale)
  
         
def addDepthofField():
    shotCameraShape = getSelectedCameraShape()
    shotCameraTransform = getSelectedCameraTransform()
    cmds.setAttr(shotCameraShape+".depthOfField", True) #Set DOF to be true
    cmds.setAttr(shotCameraShape+".locatorScale", 30) #Set to a larger locator scale instead of manualling scaling the camera
    
    #Use distance tool to create 2 locators between camera and object
    distanceDimensionShape = cmds.distanceDimension(sp=(cmds.getAttr(shotCameraTransform + '.translateX'), cmds.getAttr(shotCameraTransform + '.translateY'), cmds.getAttr(shotCameraTransform + '.translateZ')), ep=(cmds.getAttr('pSphere1.translateX'), cmds.getAttr('pSphere1.translateY'), cmds.getAttr('pSphere1.translateZ'))) 
    cmds.parent('locator1', shotCameraShape, r=True) #parent first locator under the selected camera
    cmds.rename('locator2', 'AimLocator') #rename locator closer to the object to 'AimLocator'
    cmds.connectAttr(distanceDimensionShape + '.distance', shotCameraShape+'.focusDistance') #connect distance attribute of distance dimension to focus distance of camera so that DOF can be varied
    #do the same for arnold render view
    cmds.setAttr(shotCameraShape + ".aiEnableDOF", True)
    cmds.setAttr(shotCameraShape + ".aiApertureSize", 2.8)
    cmds.connectAttr(distanceDimensionShape + '.distance', shotCameraShape+'.aiFocusDistance')
    
         
            



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
    cmds.text('Make sure that only the camera is selected in the editor before you click')
    cmds.separator(h=50)
    
    cmds.button(label = 'DOF Settings', command = 'addDepthofField()', width=100, height=100, bgc = [1, 1, 1])

    cmds.menu(label = "Set Focal Length", tearOff = True)
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
    
    cmds.menu(label = "Set Locator Scale", tearOff = True)
    cmds.menuItem(label = '5mm', command = 'adjustLocatorScale(5)')
    cmds.menuItem(label = '10mm', command = 'adjustLocatorScale(10)')
    cmds.menuItem(label = '15mm', command = 'adjustLocatorScale(15)')
    cmds.menuItem(label = '20mm', command = 'adjustLocatorScale(20)')
    cmds.menuItem(label = '25mm', command = 'adjustLocatorScale(25)')
    cmds.menuItem(label = '30mm', command = 'adjustLocatorScale(30)')
    cmds.menuItem(label = '35mm', command = 'adjustLocatorScale(35)')
    cmds.menuItem(label = '45mm', command = 'adjustLocatorScale(45)')
    cmds.menuItem(label = '55mm', command = 'adjustLocatorScale(55)')
    cmds.menuItem(label = '70mm', command = 'adjustLocatorScale(70)')
    cmds.menuItem(label = '85mm', command = 'adjustLocatorScale(85)')
    cmds.menuItem(label = '100mm', command = 'adjustLocatorScale(100)')
    
    cmds.showWindow('cameraTools')
   
cameraTools()


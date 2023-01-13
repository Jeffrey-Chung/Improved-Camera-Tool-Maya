# ala_cameraTools.0.03.py
# This tool creates a camera based on a real lworld camera, and lets user set Arri Master Prime focal lengths.

import maya.cmds as cmds

#function to get selected camera shape on the outliner
def getSelectedCameraShape():
    for each_camera_transform in cmds.ls(sl=True): #loop over all cameras that are selected (transform node)
        camera_shape = cmds.listRelatives(each_camera_transform,type="camera") #find the shape node
        if camera_shape: #only set attr if a camera shape was found 
            return camera_shape[0] #return shape node
    

#function to get selected camera transform on the outliner
def getSelectedCameraTransform():
    cameraTransform = cmds.listRelatives(getSelectedCameraShape(), parent=True) #find the camera shape's parent to get its transform
    return cameraTransform[0] #return the transform node
    
#function to get the object to focus for DOF
def getObjecttoFocus():
    for selectedObject in cmds.ls(sl=True):
        if selectedObject != getSelectedCameraTransform():
            return selectedObject
            
#function to get all locator transform nodes in the scene
def getAllLocatorTransform():
    locators = cmds.ls(exactType=('locator'), l=True) or []
    locatorTransform = cmds.listRelatives(locators, parent=True)
    return locatorTransform


#set default resolution to 1920 * 1080 and aspect ratio (16/9)
def setDefaultSettings():
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)
    
#set settings to aspect ratio 4/3, resolution: 1024 * 760
def setFourbyThreeSettings():
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1024)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 768)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.333)

#set settings to aspect ratio 16/10, resolution: 1440 * 900
def setSixtennbyTenSettings():
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1440)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 900)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.6)
    
#set settings to aspect ratio 3/2, resolution: 1080 * 720
def setThreebyTwoSettings():
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1080)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 720)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.5)
    
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
    
def assignLocators(shotCameraTransform, objectToFocus):
    allLocatorTransforms = getAllLocatorTransform() #get all locator transforms
    for locatorTransform in allLocatorTransforms:
        #check if that locator is the same position as the camera to parent
         if cmds.getAttr(locatorTransform + '.translateX') == cmds.getAttr(shotCameraTransform + '.translateX') and cmds.getAttr(locatorTransform  + '.translateY') == cmds.getAttr(shotCameraTransform + '.translateY') and cmds.getAttr(locatorTransform + '.translateZ') == cmds.getAttr(shotCameraTransform + '.translateZ'):
             cmds.parent(locatorTransform, shotCameraTransform) #parent first locator under the selected camera
         elif cmds.getAttr(locatorTransform + '.translateX') == cmds.getAttr(objectToFocus + '.translateX') and cmds.getAttr(locatorTransform  + '.translateY') == cmds.getAttr(objectToFocus + '.translateY') and cmds.getAttr(locatorTransform + '.translateZ') == cmds.getAttr(objectToFocus + '.translateZ'):
             cmds.rename(locatorTransform, 'AimLocator') #rename locator closer to the object to 'AimLocator'
  
#add DOF rig         
def addDepthofField():
    #get selected camera shape, transform and objec to focus for DOF
    shotCameraShape = getSelectedCameraShape()
    shotCameraTransform = getSelectedCameraTransform()
    objectToFocus = getObjecttoFocus()

    cmds.setAttr(shotCameraShape+".depthOfField", True) #Set DOF to be true
    cmds.setAttr(shotCameraShape+".locatorScale", 30) #Set to a larger locator scale instead of manualling scaling the camera
    
    #Use distance tool to create 2 locators between camera and selected object
    distanceDimensionShape = cmds.distanceDimension(sp=(cmds.getAttr(shotCameraTransform + '.translateX'), cmds.getAttr(shotCameraTransform + '.translateY'), cmds.getAttr(shotCameraTransform + '.translateZ')), ep=(cmds.getAttr(objectToFocus + '.translateX'), cmds.getAttr(objectToFocus + '.translateY'), cmds.getAttr(objectToFocus + '.translateZ')))
    assignLocators(shotCameraTransform, objectToFocus)
    cmds.connectAttr(distanceDimensionShape + '.distance', shotCameraShape+'.focusDistance') #connect distance attribute of distance dimension to focus distance of camera so that DOF can be varied
    #do the same for arnold render view
    cmds.setAttr(shotCameraShape + ".aiEnableDOF", True)
    cmds.setAttr(shotCameraShape + ".aiApertureSize", 2.8)
    cmds.connectAttr(distanceDimensionShape + '.distance', shotCameraShape+'.aiFocusDistance')
    
#disable Depth of Field Rig of camera
def disableAllDepthofField(cameraShape, distanceDimensionShape):
    cmds.delete(distanceDimensionShape)
    cmds.setAttr(cameraShape+".depthOfField", False)
    cmds.setAttr(cameraShape + ".aiEnableDOF", False) 

def getOptionMenuValue(typeOfOptionMenu):
    menuValue = cmds.optionMenu(typeOfOptionMenu, q=True, value=True)
    return menuValue           
            
class cameraTools():
    def __init__(self):
        self.win = cmds.window(title="Camera Tool", menuBar=True, widthHeight=(100,100),resizeToFitChildren=True)
        self.tabs = cmds.tabLayout()
        self.drawUI()

    def drawUI(self):
        #first Tab
        firstTab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[firstTab, 'Set Up Camera'])
        cmds.separator(h=10)
        cmds.text('PREVIS: Creates an AlexaLF camera', fn='fixedWidthFont')
        cmds.text('Sets the correct render settings')
        cmds.separator(h=30)
        cmds.button(label = 'Create Camera', command = 'createCamera()')
        cmds.separator(h=30)
        
        cmds.text('Set Aspect Ratio', fn='fixedWidthFont')
        cmds.text('1. Select your aspect ratio for your scene \n 2. Click Confirm Aspect Ratio Button to set those settings\n')
        self.CameraOptionMenu = cmds.optionMenu(w = 250, label = "Set Aspect Ratio")
        #add menu item for all values
        cmds.menuItem(label = "4/3")
        cmds.menuItem(label = "16/9")
        cmds.menuItem(label = "16/10")
        cmds.menuItem(label = "3/2")
        cmds.separator(h=30)
    
        cmds.button(label = 'Confirm Aspect Ratio', command = self.SetAspectRatio)

        cmds.separator(h=30)
        cmds.text('LAYOUT: Sets AlexaLF Settings', fn='fixedWidthFont')
        cmds.separator(h=30)
    
        cmds.button(label = 'AlexaLF Settings', command = 'alexaCamera()')
        cmds.setParent("..")

    
        #Second Tab
        secondTab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[secondTab, 'Camera Settings'])
        cmds.separator(h=10)
        cmds.text('Set Focal Length of Selected Camera', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your focal length in the dropdown menu \n 3. Confirm your settings by clicking on the Confirm Focal Length Button\n')
        self.FocalLengthOptionMenu = cmds.optionMenu(w = 250, label = "Set Focal Length (mm)")
        #add menu item for all values
        cmds.menuItem(label = "12")
        cmds.menuItem(label = "14")
        cmds.menuItem(label = "16")
        cmds.menuItem(label = "18")
        cmds.menuItem(label = "21")
        cmds.menuItem(label = "25")
        cmds.menuItem(label = "27")
        cmds.menuItem(label = "32")
        cmds.menuItem(label = "35")
        cmds.menuItem(label = "40")
        cmds.menuItem(label = "50")
        cmds.menuItem(label = "65")
        cmds.menuItem(label = "75")
        cmds.menuItem(label = "100")
        cmds.menuItem(label = "135")
        cmds.menuItem(label = "150")
        cmds.separator(h=30)
        cmds.button(label = "Confirm Focal Length" , command=self.SetFocalLength)
        
        cmds.separator(h=30)
        cmds.text('Set Locator Scale of Selected Camera', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your locator scale in the dropdown menu \n 3. Confirm your settings by clicking on the Confirm Locator Scale Button\n')
        self.LocatorScaleOptionMenu = cmds.optionMenu(w = 250, label = "Set Locator Scale (mm)")
        cmds.menuItem(label = '5')
        cmds.menuItem(label = '10')
        cmds.menuItem(label = '15')
        cmds.menuItem(label = '20')
        cmds.menuItem(label = '25')
        cmds.menuItem(label = '30')
        cmds.menuItem(label = '35')
        cmds.menuItem(label = '45')
        cmds.menuItem(label = '55')
        cmds.menuItem(label = '70')
        cmds.menuItem(label = '85')
        cmds.menuItem(label = '100')
        cmds.separator(h=30)
        cmds.button(label = "Confirm Locator Scale" , command=self.SetLocatorScale)
        cmds.setParent("..")
        
        #Third tab
        thirdTab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[thirdTab, 'Depth of Field Options'])
        cmds.separator(h=10)
        cmds.text('Depth of Field: Set DOF Rig', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your object to focus on in the outliner \n 3. Apply DOF by clicking on the button below')
        cmds.text("\n\nNOTE: if the focused object's coordinates is at the origin, \nthe aim locator will not spawn but DOF will still be applied as usual", fn='smallObliqueLabelFont')
        cmds.separator(h=30)
    
        cmds.button(label = 'Enable DOF', command = 'addDepthofField()')
        cmds.separator(h=30)
        cmds.text('Depth of Field: Disable DOF Rig', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your distance dimension on in the outliner \n 3. Disable DOF by clicking on the button below')
        cmds.text("\n\nNOTE: You need to delete locators manually", fn='smallObliqueLabelFont')
        cmds.separator(h=30)
        cmds.button(label = 'Disable DOF', command = 'disableAllDepthofField(getSelectedCameraShape(), getObjecttoFocus())')
        cmds.setParent("..")
      
        cmds.showWindow(self.win)
    
    
    #Set the focal length of the camera via the confirm focal length button
    def SetFocalLength(self, *args):
        menuValue = getOptionMenuValue(self.FocalLengthOptionMenu)
        adjustFocalLength(float(menuValue)) 
         
    #Set the locator scale of the camera via the confirm locator scale button    
    def SetLocatorScale(self, *args):
        menuValue = getOptionMenuValue(self.LocatorScaleOptionMenu)
        adjustLocatorScale(float(menuValue))
        
    #adjust aspect ratio 
    def SetAspectRatio(self, *args):
        menuValue = getOptionMenuValue(self.CameraOptionMenu)
        if menuValue == '4/3':
            setFourbyThreeSettings()
        elif menuValue == '16/9':
            setDefaultSettings()
        elif menuValue == '16/10':
            setSixtennbyTenSettings()
        elif menuValue == '3/2':
            setThreebyTwoSettings()
   
cameraTools()

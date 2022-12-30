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

 
def focalLength12():
    cmds.setAttr(getSelectedCamera()+".fl", 12)
      
def focalLength14():
    cmds.setAttr(getSelectedCamera()+".fl", 14)
                                   
def focalLength16():
    cmds.setAttr(getSelectedCamera()+".fl", 16)
                        
def focalLength18():
    cmds.setAttr(getSelectedCamera()+".fl", 18)
                      
def focalLength21():
    cmds.setAttr(getSelectedCamera()+".fl", 21)
            
def focalLength25():
    cmds.setAttr(getSelectedCamera()+".fl", 25)
                     
def focalLength27():
    cmds.setAttr(getSelectedCamera()+".fl", 27)
                    
def focalLength32():
    cmds.setAttr(getSelectedCamera()+".fl", 32)
               
def focalLength35():
    cmds.setAttr(getSelectedCamera()+".fl", 35)
              
def focalLength40():
    cmds.setAttr(getSelectedCamera()+".fl", 40)
                
def focalLength50():
    cmds.setAttr(getSelectedCamera()+".fl", 50)
    
def focalLength65():
    cmds.setAttr(getSelectedCamera()+".fl", 65)
   
def focalLength75():
    cmds.setAttr(getSelectedCamera()+".fl", 75)
       
def focalLength100():
    cmds.setAttr(getSelectedCamera()+".fl", 100)
  
def focalLength135():
    cmds.setAttr(getSelectedCamera()+".fl", 135)
            
def focalLength150():
    cmds.setAttr(getSelectedCamera()+".fl", 150)
  
         
def addDepthofField():
    shotCamera = getSelectedCamera()
    cmds.setAttr(shotCamera+".depthOfField", True) #Set DOF to be true
    cmds.setAttr(shotCamera+".locatorScale", 30) #Set to a larger locator scale instead of manualling scaling the camera
    cmds.distanceDimension(sp=(0, 0, 0), ep=(-38.579, -21.701, -82.295)) #Use distance tool to create 2 locators between camera and object
    cmds.parent('locator1', shotCamera, r=True) #parent first locator under the selected camera
    cmds.rename('locator2', 'AimLocator') #rename locator closer to the object to 'AimLocator'
    cmds.connectAttr('distanceDimensionShape1.distance', shotCamera+'.focusDistance') #connect distance attribute of distance dimension to focus distance of camera so that DOF can be varied
    
         
            



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
    

    cmds.menu(label = "Set Focal Length on Selected Cameras", tearOff = True)
    cmds.menuItem(label = '12mm', command = 'focalLength12()')
    cmds.menuItem(label = '14mm', command = 'focalLength14()')
    cmds.menuItem(label = '16mm', command = 'focalLength16()')
    cmds.menuItem(label = '18mm', command = 'focalLength18()')
    cmds.menuItem(label = '21mm', command = 'focalLength21()')
    cmds.menuItem(label = '25mm', command = 'focalLength25()')
    cmds.menuItem(label = '27mm', command = 'focalLength27()')
    cmds.menuItem(label = '32mm', command = 'focalLength32()')
    cmds.menuItem(label = '35mm', command = 'focalLength35()')
    cmds.menuItem(label = '40mm', command = 'focalLength40()')
    cmds.menuItem(label = '50mm', command = 'focalLength50()')
    cmds.menuItem(label = '65mm', command = 'focalLength65()')
    cmds.menuItem(label = '75mm', command = 'focalLength75()')
    cmds.menuItem(label = '100mm', command = 'focalLength100()')
    cmds.menuItem(label = '135mm', command = 'focalLength135()')
    cmds.menuItem(label = '150mm', command = 'focalLength150()')
    
    cmds.button(label = 'DOF Settings', command = 'addDepthofField()', width=100, height=100, bgc = [1, 1, 1])
    cmds.showWindow('cameraTools')
   

cameraTools()


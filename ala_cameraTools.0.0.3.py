# ala_cameraTools.0.03.py
# This tool creates a camera based on a real lworld camera, and lets user set Arri Master Prime focal lengths.

import maya.cmds as cmds

# creates an AlexaLF camera and sets the film back. Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
def createCamera():
    cameraName = cmds.camera(n = "ShotCamera", horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)


# Sets the camera Aperature made by the pipeline to match an AlexaLF camera. And sets the scene Render Settings to HD.
def alexaCamera():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".horizontalFilmAperture", 1.247)
            cmds.setAttr(cam_shp[0]+".verticalFilmAperture", 0.702)
            cmds.setAttr(cam_shp[0]+".farClipPlane", 100000)
            
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)

 
def focalLength12():
#loop over all cameras that are selected (transform node)
    for each_cam_tf in cmds.ls(sl=True):
#find the shape node
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
#only set attr if a camera shape was found 
        if cam_shp:
#set focal length
            cmds.setAttr(cam_shp[0]+".fl", 12)


def focalLength14():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 14)
                        
def focalLength16():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 16)
            
def focalLength18():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 18)
            
def focalLength21():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 21)
            
def focalLength25():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 25)
            
def focalLength27():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 27)
            
def focalLength32():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 32)
            
def focalLength35():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 35)
            
def focalLength40():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 40)
            
def focalLength50():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 50)
            
def focalLength65():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 65)
            
def focalLength75():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 75)
            
def focalLength100():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 100)
            
def focalLength135():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 135)
            
def focalLength150():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".fl", 150)
         
def addDepthofField():
    #Set DOF to be true
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".depthOfField", True)



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


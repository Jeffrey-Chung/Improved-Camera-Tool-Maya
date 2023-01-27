# ala_cameraTools.0.03.py
# This tool creates a camera based on a real lworld camera, and lets user set Arri Master Prime focal lengths.

import maya.cmds as cmds

#function to get selected camera shape on the outliner
def get_selected_camera_shape():
    for each_camera_transform in cmds.ls(sl=True): #loop over all cameras that are selected (transform node)
        camera_shape = cmds.listRelatives(each_camera_transform,type="camera") #find the shape node
        if camera_shape: #only set attr if a camera shape was found 
            return camera_shape[0] #return shape node
    

#function to get selected camera transform on the outliner
def get_selected_camera_transform():
    camera_transform = cmds.listRelatives(get_selected_camera_shape(), parent=True) #find the camera shape's parent to get its transform
    return camera_transform[0] #return the transform node
    
#function to get the object to focus for DOF
def get_object_to_focus():
    for selected_object in cmds.ls(sl=True):
        if selected_object != get_selected_camera_transform():
            return selected_object

#gets a selected object in general, likely to be used for other tools as well
def get_selected_object():
    for selected_object in cmds.ls(sl=True):
        if selected_object:
            return selected_object
            
            
#function to get all locator transform nodes in the scene
def get_all_locator_transform():
    locators = cmds.ls(exactType=('locator'), l=True) or []
    locator_transform = cmds.listRelatives(locators, parent=True)
    return locator_transform


#set default resolution to 1920 * 1080 and aspect ratio (16/9)
def set_default_settings():
    set_resolution_width = cmds.setAttr('defaultResolution.width', 1920)
    set_resolution_height = cmds.setAttr('defaultResolution.height', 1080)
    set_device_aspect_ratio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)
    
#set settings to aspect ratio 4/3, resolution: 1024 * 760
def set_four_by_three_settings():
    set_resolution_width = cmds.setAttr('defaultResolution.width', 1024)
    set_resolution_height = cmds.setAttr('defaultResolution.height', 768)
    set_device_aspect_ratio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.333)

#set settings to aspect ratio 16/10, resolution: 1440 * 900
def set_sixteen_by_ten_settings():
    set_resolution_width = cmds.setAttr('defaultResolution.width', 1440)
    set_resolution_height = cmds.setAttr('defaultResolution.height', 900)
    set_device_aspect_ratio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.6)
    
#set settings to aspect ratio 3/2, resolution: 1080 * 720
def set_three_by_two_settings():
    set_resolution_width = cmds.setAttr('defaultResolution.width', 1080)
    set_resolution_height = cmds.setAttr('defaultResolution.height', 720)
    set_device_aspect_ratio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.5)
    
# creates an AlexaLF camera and sets the film back. Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
def create_camera():
    camera_name = cmds.camera(n = "ShotCamera", horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    set_default_settings()

# Sets the camera Aperature made by the pipeline to match an AlexaLF camera. And sets the scene Render Settings to HD.
def alexa_camera():
    cmds.setAttr(get_selected_camera_shape()+".horizontalFilmAperture", 1.247)
    cmds.setAttr(get_selected_camera_shape()+".verticalFilmAperture", 0.702)
    cmds.setAttr(get_selected_camera_shape()+".farClipPlane", 100000)
    set_default_settings()

#Set the focal length of the camera
def adjust_focal_length(focal_length):
    cmds.setAttr(get_selected_camera_shape()+".fl", focal_length)
    
#Set the locator scale of the camera
def adjust_locator_scale(locator_scale):
    cmds.setAttr(get_selected_camera_shape()+".locatorScale", locator_scale)
    
def assign_locators(shot_camera_transform, object_to_focus):
    all_locator_transforms = get_all_locator_transform() #get all locator transforms
    for locator_transform in all_locator_transforms:
        #check if that locator is the same position as the camera to parent
         if cmds.getAttr(locator_transform + '.translateX') == cmds.getAttr(shot_camera_transform + '.translateX') and cmds.getAttr(locator_transform + '.translateY') == cmds.getAttr(shot_camera_transform + '.translateY') and cmds.getAttr(locator_transform + '.translateZ') == cmds.getAttr(shot_camera_transform + '.translateZ'):
             cmds.parent(locator_transform, shot_camera_transform) #parent first locator under the selected camera
         elif cmds.getAttr(locator_transform + '.translateX') == cmds.getAttr(object_to_focus + '.translateX') and cmds.getAttr(locator_transform  + '.translateY') == cmds.getAttr(object_to_focus + '.translateY') and cmds.getAttr(locator_transform + '.translateZ') == cmds.getAttr(object_to_focus + '.translateZ'):
             cmds.rename(locator_transform, 'AimLocator') #rename locator closer to the object to 'AimLocator'
  
#refactored code common to both DOF methods
def basic_depth_of_field_settings():
    #get selected camera shape, transform and objec to focus for DOF
    shot_camera_shape = get_selected_camera_shape()
    shot_camera_transform = get_selected_camera_transform()
    object_to_focus = get_object_to_focus()

    cmds.setAttr(shot_camera_shape+".depthOfField", True) #Set DOF to be true
    cmds.setAttr(shot_camera_shape+".locatorScale", 30) #Set to a larger locator scale instead of manualling scaling the camera
    
    #Use distance tool to create 2 locators between camera and selected object
    distance_dimension_shape = cmds.distanceDimension(sp=(cmds.getAttr(shot_camera_transform + '.translateX'), cmds.getAttr(shot_camera_transform + '.translateY'), cmds.getAttr(shot_camera_transform + '.translateZ')), ep=(cmds.getAttr(object_to_focus + '.translateX'), cmds.getAttr(object_to_focus + '.translateY'), cmds.getAttr(object_to_focus + '.translateZ')))
    assignLocators(shot_camera_transform, object_to_focus)
    return shot_camera_shape, distance_dimension_shape
    

#add DOF rig via Focal length         
def add_depth_of_field():
    shot_camera_shape, distance_dimension_shape = basic_depth_of_field_settings()
    cmds.connectAttr(distance_dimension_shape + '.distance', shot_camera_shape+'.focusDistance') #connect distance attribute of distance dimension to focus distance of camera so that DOF can be varied
    #do the same for arnold render view
    cmds.setAttr(shot_camera_shape + ".aiEnableDOF", True)
    cmds.setAttr(shot_camera_shape + ".aiApertureSize", 2.8)
    cmds.connectAttr(distance_dimension_shape + '.distance', shot_camera_shape+'.aiFocusDistance')

    
#connect DOF via f stop, distance will be clamped to 64 units if it goes above
def add_depth_of_field_fstop():
    shot_camera_shape, distance_dimension_shape = basic_depth_of_field_settings()
    cmds.connectAttr(distance_dimension_shape + '.distance', shot_camera_shape+'.fStop') #connect distance attribute of distance dimension to f stop of camera so that DOF can be varied
    
#disable Depth of Field Rig of camera (focal distance + fStop)
def disable_depth_of_field(camera_shape, distance_dimension_shape):
    cmds.delete(distance_dimension_shape)
    cmds.setAttr(camera_shape+".depthOfField", False)
    cmds.setAttr(camera_shape + ".aiEnableDOF", False) 

#get the value from each option menu to coduct event
def get_option_menu_value(option_menu):
    menu_value = cmds.optionMenu(option_menu, q=True, value=True)
    return menu_value  
    
#create circular turntable curve
def create_curve(selected_object):
    turntable_circle = cmds.circle( nr=(0, 0, 1), c=(cmds.getAttr(selected_object + '.translateX'), cmds.getAttr(selected_object + '.translateY'), cmds.getAttr(selected_object + '.translateZ')), r=1000)
    cmds.setAttr(turntable_circle[0] + '.rotateX', -90)   

#create turntable animation for moving the camera
def animate_camera():
    selected_camera = get_selected_camera_transform()
    selected_curve = get_object_to_focus()
    motion_path = cmds.pathAnimation(selected_curve, selected_camera, stu = 0, etu = 180, follow = True, fractionMode = True) #attach the camera to the curve
    cmds.setAttr(selected_camera + '.rotateX', 0) 
    cmds.setAttr(selected_camera + '.rotateY', 180)
    
    '''increase camera angle at the Y axis by 45 degrees in every quarter
    both tangent types are spline to use a non-linear interpolation for a smoother animation for camera'''
    cmds.currentTime(0)
    cmds.setKeyframe(selected_camera, attribute = 'rotateX' , value = 0, inTangentType="spline", outTangentType="spline") #can adjust this attribute to whatever angle you want depending on height of circle
    cmds.setKeyframe(selected_camera, attribute = 'rotateY' , value = -180, inTangentType="spline", outTangentType="spline")
    cmds.currentTime(45)  
    cmds.setKeyframe(selected_camera, attribute = 'rotateY' , value = -135, inTangentType="spline", outTangentType="spline")
    cmds.currentTime(90)  
    cmds.setKeyframe(selected_camera, attribute = 'rotateY' , value = 0, inTangentType="spline", outTangentType="spline")
    cmds.currentTime(135)  
    cmds.setKeyframe(selected_camera, attribute = 'rotateY' , value = 135, inTangentType="spline", outTangentType="spline")
    cmds.currentTime(180)
    cmds.setKeyframe(selected_camera, attribute = 'rotateY' , value = 180, inTangentType="spline", outTangentType="spline")    
            
#class for camera UI
class CameraTool():
    def __init__(self):
        self.win = cmds.window(title="Camera Tool", menuBar=True, widthHeight=(100,100),resizeToFitChildren=True)
        self.tabs = cmds.tabLayout()
        self.draw_UI()

    #function to draw the UI itself
    def draw_UI(self):
        #first Tab: create camera + set aspect ratio
        first_tab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[first_tab, 'Set Up Camera'])
        cmds.separator(h=10)
        cmds.text('PREVIS: Creates an AlexaLF camera', fn='fixedWidthFont')
        cmds.text('Sets the correct render settings')
        cmds.separator(h=20)
        cmds.button(label = 'Create Camera', command = 'create_camera()')
        cmds.separator(h=20)
       
        cmds.text('Set Aspect Ratio', fn='fixedWidthFont')
        cmds.text('1. Select your aspect ratio for your scene \n 2. Click Confirm Aspect Ratio Button to set those settings\n')
        self.camera_option_menu = cmds.optionMenu(w = 250, label = "Set Aspect Ratio")
        #add menu item for all values
        cmds.menuItem(label = "4/3")
        cmds.menuItem(label = "16/9")
        cmds.menuItem(label = "16/10")
        cmds.menuItem(label = "3/2")
        cmds.separator(h=20)
    
        cmds.button(label = 'Confirm Aspect Ratio', command = self.set_aspect_ratio)

        cmds.separator(h=20)
        cmds.text('LAYOUT: Sets AlexaLF Settings', fn='fixedWidthFont')
        cmds.separator(h=20)
    
        cmds.button(label = 'AlexaLF Settings', command = 'alexa_camera()')
        cmds.separator(h=20)
        cmds.setParent("..")

    
        #Second Tab: adjust camera settings via option menus
        second_tab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[second_tab, 'Camera Settings'])
        cmds.separator(h=10)
        cmds.text('Set Focal Length of Selected Camera', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your focal length in the dropdown menu \n 3. Confirm your settings by clicking on the Confirm Focal Length Button\n')
        self.focal_length_option_menu = cmds.optionMenu(w = 250, label = "Set Focal Length (mm)")
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
        cmds.separator(h=20)
        cmds.button(label = "Confirm Focal Length" , command=self.set_focal_length)
        
        cmds.separator(h=20)
        cmds.text('Set Locator Scale of Selected Camera', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your locator scale in the dropdown menu \n 3. Confirm your settings by clicking on the Confirm Locator Scale Button\n')
        self.locator_scale_option_menu = cmds.optionMenu(w = 250, label = "Set Locator Scale (mm)")
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
        cmds.separator(h=20)
        cmds.button(label = "Confirm Locator Scale" , command=self.set_locator_scale)
        cmds.separator(h=20)
        cmds.setParent("..")
        
        #Third tab: DOF options
        third_tab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[third_tab, 'Depth of Field Options'])
        cmds.separator(h=10)
        cmds.text('Depth of Field: Set DOF Rig', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your object to focus on in the outliner \n 3. Apply DOF by clicking on the button below')
        cmds.text("\n\nNOTE: \n1. if the focused object's coordinates is at the origin, \nthe aim locator will not spawn but DOF will still be applied as usual", fn='smallObliqueLabelFont')
        cmds.text('2. For the f stop option, distance will be clamped to 64 units', fn='smallObliqueLabelFont')
        cmds.separator(h=20)
    
        cmds.button(label = 'Enable DOF Focal Length', command = 'add_depth_of_field()')
        cmds.separator(h=10)
        cmds.button(label = 'Enable DOF f Stop', command = 'add_depth_of_field_fstop()')
        cmds.separator(h=20)
        cmds.text('Depth of Field: Disable DOF Rig', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your distance dimension on in the outliner \n 3. Disable DOF by clicking on the button below')
        cmds.text("\n\nNOTE: You need to delete locators manually", fn='smallObliqueLabelFont')
        cmds.separator(h=20)
        cmds.button(label = 'Disable DOF', command = 'disable_depth_of_field(get_selected_camera_shape(), get_object_to_focus())')
        cmds.setParent("..")
        
        #Fourth tab: Turntable camera animation
        fourth_tab = cmds.columnLayout(adjustableColumn = True)
        cmds.tabLayout(self.tabs, edit=True, tabLabel=[fourth_tab, 'Camera Animation'])
        cmds.separator(h=10)
        cmds.text('Turntable circle: Set circular curve', fn='fixedWidthFont')
        cmds.text('1. Select your object in the outliner \n 2. Click on the button below to create the circle')
        cmds.separator(h=20)
        cmds.button(label = 'Create Circle', command = 'create_curve(get_selected_object())')
        cmds.separator(h=20)
        cmds.text('Turntable animation: Setup Camera Animation', fn='fixedWidthFont')
        cmds.text('1. Select your Camera on the outliner \n 2. Select your curve on the outliner \n 3. Click on the Animate Camera button to setup the animation')
        cmds.separator(h=20)
        cmds.button(label = 'Animate Camera', command = 'animate_camera()')
        cmds.separator(h=20)
        cmds.setParent("..")
      
        cmds.showWindow(self.win)
    
    
    #Set the focal length of the camera via the confirm focal length button
    def set_focal_length(self, *args):
        menu_value = get_option_menu_value(self.focal_length_option_menu)
        adjust_focal_length(float(menu_value)) 
         
    #Set the locator scale of the camera via the confirm locator scale button    
    def set_locator_scale(self, *args):
        menu_value = get_option_menu_value(self.locator_scale_option_menu)
        adjust_locator_scale(float(menu_value))
        
    #adjust aspect ratio 
    def set_aspect_ratio(self, *args):
        menu_value = get_option_menu_value(self.camera_option_menu)
        if menu_value == '4/3':
            set_four_by_three_settings()
        elif menu_value == '16/9':
            set_default_settings()
        elif menu_value == '16/10':
            set_sixteen_by_ten_settings()
        elif menu_value == '3/2':
            set_three_by_two_settings()
   
CameraTool()

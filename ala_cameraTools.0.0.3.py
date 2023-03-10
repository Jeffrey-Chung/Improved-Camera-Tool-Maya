# ala_cameraTools.0.03.py
# This tool creates a camera based on a real lworld camera, and lets user set Arri Master Prime focal lengths.
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import mtoa.utils as mutils

aspect_ratios = [
    '4:3',
    '16:9',
    '16:10',
    '3:2'
]

focal_lengths = [
    "12",
    "14",
    "16",
    "18",
    "21",
    "25",
    "27",
    "32",
    "35",
    "45",
    "55",
    "65",
    "75",
    "100",
    "135",
    "150"
]

locator_scales = [
    "5",
    "10",
    "15",
    "20",
    "25",
    "30",
    "35",
    "45",
    "55",
    "70",
    "85",
    "100"
]

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
    assign_locators(shot_camera_transform, object_to_focus)
    return shot_camera_shape, distance_dimension_shape
    


#get the value from each option menu to coduct event
def get_option_menu_value(option_menu):
    menu_value = cmds.optionMenu(option_menu, q=True, value=True)
    return menu_value  
  

def get_maya_window():
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)
    return maya_main_window

#class for camera UI   
class CameraTool(QMainWindow):
    def __init__(self, parent = None):
        super(CameraTool, self).__init__(parent)
        #set name of the UI
        self.setWindowTitle("Camera Tool")
        #Initiate tabs for UI
        tab = QTabWidget()

        #first Tab: create camera + set aspect ratio
        first_tab = QWidget()
        first_tab_layout = QVBoxLayout()
        first_tab.setLayout(first_tab_layout)

        #create camera section
        create_camera_header = QLabel("PREVIS: Creates an AlexaLF camera")
        header_font=QFont('Arial', 15)
        header_font.setBold(True)
        create_camera_header.setFont(header_font)
        first_tab_layout.addWidget(create_camera_header)

        create_camera_button = QPushButton("Create Camera")
        create_camera_button.clicked.connect(self.create_camera)
        first_tab_layout.addWidget(create_camera_button)

        #Adjust Aspect Ratio Section
        aspect_ratio_header = QLabel("Set Aspect Ratio in Dropdown Menu Below")
        aspect_ratio_header.setFont(header_font)
        first_tab_layout.addWidget(aspect_ratio_header)

        self.camera_dropdown = QComboBox()
        self.camera_dropdown.addItems(aspect_ratios)
        self.camera_dropdown.activated.connect(self.set_aspect_ratio)
        first_tab_layout.addWidget(self.camera_dropdown)

        #Set AlexaLF section
        set_alexaLF_settings_header = QLabel("LAYOUT: Sets AlexaLF Settings")
        set_alexaLF_settings_header.setFont(header_font)
        first_tab_layout.addWidget(set_alexaLF_settings_header)

        set_alexaLF_settings_button = QPushButton("AlexaLF Settings")
        set_alexaLF_settings_button.clicked.connect(self.alexa_camera)
        first_tab_layout.addWidget(set_alexaLF_settings_button)

        #Second Tab: adjust camera settings via option menus
        second_tab = QWidget()
        second_tab_layout = QVBoxLayout()
        second_tab.setLayout(second_tab_layout)
        
        #Setup fonts for instructional text
        instructions_font = QFont('Arial', 15)
        instructions_font_second_tab = QFont('Arial', 17)
        
        #Set Focal Length Section
        set_focal_length_header = QLabel("Set Focal Length of Selected Camera (mm)")
        set_focal_length_header.setFont(header_font)
        second_tab_layout.addWidget(set_focal_length_header)

        set_focal_length_instructions = QLabel(' 1. Select your camera in the outliner \n 2. Select your focal length in the dropdown menu')
        set_focal_length_instructions.setFont(instructions_font_second_tab)
        second_tab_layout.addWidget(set_focal_length_instructions)

        self.focal_length_dropdown = QComboBox()
        self.focal_length_dropdown.addItems(focal_lengths)
        self.focal_length_dropdown.activated.connect(self.set_focal_length)
        second_tab_layout.addWidget(self.focal_length_dropdown)
        
        #Set Locator Scale Section
        set_locator_scale_header = QLabel("Set Locator Scale of Selected Camera (mm)")
        set_locator_scale_header.setFont(header_font)
        second_tab_layout.addWidget(set_locator_scale_header)

        set_locator_scale_instructions = QLabel(' 1. Select your camera in the outliner \n 2. Select your locator scale in the dropdown menu')
        set_locator_scale_instructions.setFont(instructions_font_second_tab)
        second_tab_layout.addWidget(set_locator_scale_instructions)

        self.locator_scale_dropdown = QComboBox()
        self.locator_scale_dropdown.addItems(locator_scales)
        self.locator_scale_dropdown.activated.connect(self.set_locator_scale)
        second_tab_layout.addWidget(self.locator_scale_dropdown)

        #Third tab: DOF options
        third_tab = QWidget()
        third_tab_layout = QVBoxLayout()
        third_tab.setLayout(third_tab_layout)

        #Set Up DOF section
        set_dof_header = QLabel("Depth of Field: Set DOF Rig")
        set_dof_header.setFont(header_font)
        third_tab_layout.addWidget(set_dof_header)

        set_dof_instructions = QLabel(' 1. Select your camera in the outliner \n 2. Select your object to focus on in the outliner \n 3. Apply DOF by clicking on the button below')
        set_dof_tip = QLabel('Make sure both camera + distance dimension is selected')
        set_dof_tip_font = QFont()
        set_dof_tip_font.setItalic(True)
        set_dof_tip.setFont(set_dof_tip_font)
        set_dof_note = QLabel("NOTE: \n 1. if the focused object's coordinates is at the origin, \nthe aim locator will not spawn but DOF will still be applied as usual \n 2. For the f stop option, distance will be clamped to 64 units")
        set_dof_note_font = QFont()
        set_dof_note_font.setBold(True)
        set_dof_note.setFont(set_dof_note_font)
        third_tab_layout.addWidget(set_dof_instructions)
        third_tab_layout.addWidget(set_dof_tip)
        third_tab_layout.addWidget(set_dof_note)

        set_dof_with_focal_length_button = QPushButton("Enable DOF Focal Length")
        set_dof_with_focal_length_button.clicked.connect(self.add_depth_of_field)
        third_tab_layout.addWidget(set_dof_with_focal_length_button)

        set_dof_with_f_stop_button = QPushButton("Enable DOF f Stop")
        set_dof_with_f_stop_button.clicked.connect(self.add_depth_of_field_fstop)
        third_tab_layout.addWidget(set_dof_with_f_stop_button)

        #Diable DOF Section
        disable_dof_header = QLabel("Depth of Field: Disable DOF Rig")
        disable_dof_header.setFont(header_font)
        third_tab_layout.addWidget(disable_dof_header)

        disable_dof_instructions = QLabel(' 1. Select your camera in the outliner \n 2. Select your distance dimension on in the outliner\n 3. Disable DOF by clicking on the button below')
        disable_dof_tip = QLabel('Make sure both camera + distance dimension is selected')
        disable_dof_tip_font = QFont('Arial', 15)
        disable_dof_tip_font.setItalic(True)
        disable_dof_tip.setFont(disable_dof_tip_font)
        disable_dof_note = QLabel("NOTE: You need to delete locators manually")
        disable_dof_note_font = QFont('Arial', 15)
        disable_dof_note_font.setBold(True)
        disable_dof_note.setFont(disable_dof_note_font)
        third_tab_layout.addWidget(disable_dof_instructions)
        third_tab_layout.addWidget(disable_dof_tip)
        third_tab_layout.addWidget(disable_dof_note)

        disable_dof_button = QPushButton("Disable DOF")
        disable_dof_button.clicked.connect(self.disable_depth_of_field)
        third_tab_layout.addWidget(disable_dof_button)

        #Fourth tab: Turntable camera animation
        fourth_tab = QWidget()
        fourth_tab_layout = QVBoxLayout()
        fourth_tab.setLayout(fourth_tab_layout)

        #Set Up Curve section
        set_up_curve_header = QLabel("Turntable circle: Set circular curve")
        set_up_curve_header.setFont(header_font)
        fourth_tab_layout.addWidget(set_up_curve_header)

        set_up_curve_instructions = QLabel(' 1. Select your object in the outliner \n 2. Click on the button below to create the circle')
        set_up_curve_instructions.setFont(instructions_font)
        fourth_tab_layout.addWidget(set_up_curve_instructions)

        set_up_curve_button = QPushButton("Create Circle")
        set_up_curve_button.clicked.connect(self.create_curve)
        fourth_tab_layout.addWidget(set_up_curve_button)

        #Set Up Animation section
        set_up_animation_header = QLabel("Turntable animation: Setup Camera Animation")
        set_up_animation_header.setFont(header_font)
        fourth_tab_layout.addWidget(set_up_animation_header)

        set_up_animation_instructions = QLabel(' 1. Select your Camera on the outliner \n 2. Select your curve on the outliner \n 3. Click on the Animate Camera button to setup the animation')
        set_up_animation_instructions.setFont(instructions_font)
        set_up_animation_tip = QLabel('Make sure both camera + distance dimension is selected')
        set_up_animation_tip_font = QFont('Arial', 15)
        set_up_animation_tip_font.setItalic(True)
        set_up_animation_tip.setFont(set_up_animation_tip_font)
        fourth_tab_layout.addWidget(set_up_animation_instructions)
        fourth_tab_layout.addWidget(set_up_animation_tip)

        set_up_animation_button = QPushButton("Animate Camera")
        set_up_animation_button.clicked.connect(self.animate_camera)
        fourth_tab_layout.addWidget(set_up_animation_button)

        #Add all tabs 
        tab.addTab(first_tab, "Set Up Camera")
        tab.addTab(second_tab, "Camera Settings")
        tab.addTab(third_tab, "Depth of Field Options")
        tab.addTab(fourth_tab, "Camera Animation")

        self.setCentralWidget(tab)
        self.show()
    
    #creates an AlexaLF camera and sets the film back. Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
    def create_camera(self):
        camera_name = cmds.camera(n = "ShotCamera", horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
        set_default_settings()
    
    #adjust aspect ratio 
    def set_aspect_ratio(self):
        menu_value = self.camera_dropdown.currentText()
        if menu_value == "4:3":
            set_four_by_three_settings()
        elif menu_value == "16:9":
            set_default_settings()
        elif menu_value == "16:10":
            set_sixteen_by_ten_settings()
        elif menu_value == "3:2":
            set_three_by_two_settings()
    
    #Sets the camera Aperature made by the pipeline to match an AlexaLF camera. And sets the scene Render Settings to HD.
    def alexa_camera(self):  
        cmds.setAttr(get_selected_camera_shape()+".horizontalFilmAperture", 1.247)
        cmds.setAttr(get_selected_camera_shape()+".verticalFilmAperture", 0.702)
        cmds.setAttr(get_selected_camera_shape()+".farClipPlane", 100000)
        set_default_settings()
    
    #Set the focal length of the camera via the confirm focal length button
    def set_focal_length(self):
        menu_value = self.focal_length_dropdown.currentText()
        adjust_focal_length(float(menu_value)) 
    
    #Set the locator scale of the camera via the confirm locator scale button    
    def set_locator_scale(self):
        menu_value = self.locator_scale_dropdown.currentText()
        adjust_locator_scale(float(menu_value))
    
    #add DOF rig via Focal length         
    def add_depth_of_field(self):
        shot_camera_shape, distance_dimension_shape = basic_depth_of_field_settings()
        cmds.connectAttr(distance_dimension_shape + '.distance', shot_camera_shape+'.focusDistance') #connect distance attribute of distance dimension to focus distance of camera so that DOF can be varied
        #do the same for arnold render view
        cmds.setAttr(shot_camera_shape + ".aiEnableDOF", True)
        cmds.setAttr(shot_camera_shape + ".aiApertureSize", 2.8)
        cmds.connectAttr(distance_dimension_shape + '.distance', shot_camera_shape+'.aiFocusDistance')
        
    #connect DOF via f stop, distance will be clamped to 64 units if it goes above
    def add_depth_of_field_fstop(self):
        shot_camera_shape, distance_dimension_shape = basic_depth_of_field_settings()
        cmds.connectAttr(distance_dimension_shape + '.distance', shot_camera_shape+'.fStop') #connect distance attribute of distance dimension to f stop of camera so that DOF can be varied
    
    #disable Depth of Field Rig of camera (focal distance + fStop)
    def disable_depth_of_field(self):
        camera_shape = get_selected_camera_shape()
        distance_dimension_shape = get_object_to_focus()
        cmds.delete(distance_dimension_shape)
        cmds.setAttr(camera_shape+".depthOfField", False)
        cmds.setAttr(camera_shape + ".aiEnableDOF", False)
    
    #create circular turntable curve
    def create_curve(self):
        selected_object = get_selected_object()
        turntable_circle = cmds.circle( nr=(0, 0, 1), c=(cmds.getAttr(selected_object + '.translateX'), cmds.getAttr(selected_object + '.translateY'), cmds.getAttr(selected_object + '.translateZ')), r=1000)
        cmds.setAttr(turntable_circle[0] + '.rotateX', -90)
            
    #create turntable animation for moving the camera
    def animate_camera(self):
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
    
if __name__ == '__main__':
    tab_window = CameraTool(parent=get_maya_window())

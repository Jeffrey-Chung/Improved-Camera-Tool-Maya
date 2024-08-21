'''
ala_camera_tools.py
This tool creates a camera based on a real world camera
and lets user set Arri Master Prime focal lengths.
'''
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
from maya import cmds

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

def get_selected_cam_shape():
    '''
    function to get selected camera shape on the outliner
    '''
    for each_camera_transform in cmds.ls(sl=True):
        camera_shape = cmds.listRelatives(each_camera_transform,type="camera")
        if camera_shape:
            return camera_shape[0]
    return None


def get_selected_cam_transform():
    '''
    function to get selected camera transform on the outliner
    '''
    camera_transform = cmds.listRelatives(get_selected_cam_shape(), parent=True)
    return camera_transform[0]


def get_object_to_focus():
    '''
    function to get the object to focus for DOF
    '''
    for obj in cmds.ls(sl=True):
        if obj != get_selected_cam_transform():
            return obj
    return None


def get_obj():
    '''
    gets a selected object in general, likely to be used for other tools as well
    '''
    for obj in cmds.ls(sl=True):
        if obj:
            return obj
    return None


def get_all_locator_transform():
    '''
    function to get all locator transform nodes in the scene
    '''
    locators = cmds.ls(exactType=('locator'), l=True) or []
    locator_transform = cmds.listRelatives(locators, parent=True)
    return locator_transform


def set_default_settings():
    '''
    Set default resolution to 1920 * 1080 and aspect ratio (16/9)
    '''
    cmds.setAttr('defaultResolution.width', 1920)
    cmds.setAttr('defaultResolution.height', 1080)
    cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)


def set_four_by_three_settings():
    '''
    set settings to aspect ratio 4/3, resolution: 1024 * 760
    '''
    cmds.setAttr('defaultResolution.width', 1024)
    cmds.setAttr('defaultResolution.height', 768)
    cmds.setAttr('defaultResolution.deviceAspectRatio', 1.333)


def set_sixteen_by_ten_settings():
    '''
    set settings to aspect ratio 16/10, resolution: 1440 * 900
    '''
    cmds.setAttr('defaultResolution.width', 1440)
    cmds.setAttr('defaultResolution.height', 900)
    cmds.setAttr('defaultResolution.deviceAspectRatio', 1.6)


def set_three_by_two_settings():
    '''
    Set settings to aspect ratio 3/2, resolution: 1080 * 720
    '''
    cmds.setAttr('defaultResolution.width', 1080)
    cmds.setAttr('defaultResolution.height', 720)
    cmds.setAttr('defaultResolution.deviceAspectRatio', 1.5)


def adjust_focal_length(focal_length):
    '''
    Set the focal length of the camera
    '''
    cmds.setAttr(get_selected_cam_shape()+".fl", focal_length)


def adjust_locator_scale(locator_scale):
    '''
    Set the locator scale of the camera
    '''
    cmds.setAttr(get_selected_cam_shape()+".locatorScale", locator_scale)

def assign_locators(shot_camera_transform):
    '''
    Assign locators between camera and object
    '''
    all_locator_transforms = get_all_locator_transform()
    for locator_transform in all_locator_transforms:
        #check if that locator is the same position as the camera to parent
        locator_transform_x = cmds.getAttr(locator_transform + '.translateX')
        locator_transform_y = cmds.getAttr(locator_transform + '.translateY')
        locator_transform_z = cmds.getAttr(locator_transform + '.translateZ')
        shot_cam_x =  cmds.getAttr(shot_camera_transform + '.translateX')
        shot_cam_y = cmds.getAttr(shot_camera_transform + '.translateY')
        shot_cam_z = cmds.getAttr(shot_camera_transform + '.translateZ')
        # object_x =  cmds.getAttr(object_to_focus + '.translateX')
        # object_y = cmds.getAttr(object_to_focus + '.translateY')
        # object_z = cmds.getAttr(object_to_focus + '.translateZ')
        if locator_transform_x == shot_cam_x:
            if locator_transform_y == shot_cam_y:
                if locator_transform_z == shot_cam_z:
                    cmds.parent(locator_transform, shot_camera_transform)
        else:
            cmds.rename(locator_transform, 'AimLocator')

# Refactored code common to both DOF methods
def basic_depth_of_field_settings():
    '''
    get selected camera shape, transform and objec to focus for DOF
    '''
    shot_camera_shape = get_selected_cam_shape()
    shot_camera_transform = get_selected_cam_transform()
    object_to_focus = get_object_to_focus()

    cmds.setAttr(shot_camera_shape+".depthOfField", True)
    cmds.setAttr(shot_camera_shape+".locatorScale", 30)

    # Use distance tool to create 2 locators between camera and selected object
    shot_cam_x =  cmds.getAttr(shot_camera_transform + '.translateX')
    shot_cam_y = cmds.getAttr(shot_camera_transform + '.translateY')
    shot_cam_z = cmds.getAttr(shot_camera_transform + '.translateZ')
    object_x =  cmds.getAttr(object_to_focus + '.translateX')
    object_y = cmds.getAttr(object_to_focus + '.translateY')
    object_z = cmds.getAttr(object_to_focus + '.translateZ')
    shot_camera_coordinates = (shot_cam_x, shot_cam_y, shot_cam_z)
    object_coord = (object_x, object_y, object_z)
    dist_dimension_shape = cmds.distanceDimension(sp=shot_camera_coordinates, ep=object_coord)
    assign_locators(shot_camera_transform)
    return shot_camera_shape, dist_dimension_shape



def get_option_menu_value(option_menu):
    '''
    get the value from each option menu to coduct event
    '''
    menu_value = cmds.optionMenu(option_menu, q=True, value=True)
    return menu_value


def get_maya_window():
    '''
    Get the UI of the Camera tool
    '''
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)
    return maya_main_window


class CameraTool(QMainWindow):
    '''
    Class for camera UI   
    '''
    # TODO: Refactor code to fix R0914 and R0915 warning
    def __init__(self):
        super().__init__()
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
        set_alexalf_settings_header = QLabel("LAYOUT: Sets AlexaLF Settings")
        set_alexalf_settings_header.setFont(header_font)
        first_tab_layout.addWidget(set_alexalf_settings_header)

        set_alexalf_settings_button = QPushButton("AlexaLF Settings")
        set_alexalf_settings_button.clicked.connect(self.alexa_camera)
        first_tab_layout.addWidget(set_alexalf_settings_button)

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

        set_focal_length_text = ' 1. Select your camera in the outliner'
        set_focal_length_instructions_step_one = QLabel(set_focal_length_text)
        set_focal_length_text = ' \n 2. Select your focal length in the dropdown menu'
        set_focal_length_instructions_step_two = QLabel(set_focal_length_text)
        set_focal_length_instructions_step_one.setFont(instructions_font_second_tab)
        set_focal_length_instructions_step_two.setFont(instructions_font_second_tab)
        second_tab_layout.addWidget(set_focal_length_instructions_step_one)
        second_tab_layout.addWidget(set_focal_length_instructions_step_two)

        self.focal_length_dropdown = QComboBox()
        self.focal_length_dropdown.addItems(focal_lengths)
        self.focal_length_dropdown.activated.connect(self.set_focal_length)
        second_tab_layout.addWidget(self.focal_length_dropdown)

        #Set Locator Scale Section
        set_locator_scale_header = QLabel("Set Locator Scale of Selected Camera (mm)")
        set_locator_scale_header.setFont(header_font)
        second_tab_layout.addWidget(set_locator_scale_header)

        set_locator_scale_text = ' 1. Select your camera in the outliner'
        set_locator_scale_instructions_step_one = QLabel(set_locator_scale_text)
        set_locator_scale_text = ' \n 2. Select your locator scale in the dropdown menu'
        set_locator_scale_instructions_step_two = QLabel(set_locator_scale_text)
        set_locator_scale_instructions_step_one.setFont(instructions_font_second_tab)
        set_locator_scale_instructions_step_two.setFont(instructions_font_second_tab)
        second_tab_layout.addWidget(set_locator_scale_instructions_step_one)
        second_tab_layout.addWidget(set_locator_scale_instructions_step_two)

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

        set_dof_instructions_text = ' 1. Select your camera in the outliner '
        set_dof_instructions_step_one = QLabel(set_dof_instructions_text)
        set_dof_instructions_text = '\n 2. Select your object to focus on in the outliner'
        set_dof_instructions_step_two = QLabel(set_dof_instructions_text)
        set_dof_instructions_text = ' \n 3. Apply DOF by clicking on the button below'
        set_dof_instructions_step_three = QLabel(set_dof_instructions_text)

        set_dof_tip = QLabel('Make sure both camera + distance dimension is selected')
        set_dof_tip_font = QFont()
        set_dof_tip_font.setItalic(True)
        set_dof_tip.setFont(set_dof_tip_font)

        set_dof_note_text = "NOTE: \n 1. if the focused object's coordinates is at the origin, "
        set_dof_note_step_1_pt_1 = QLabel(set_dof_note_text)
        set_dof_note_text = "\nthe aim locator won't spawn but DOF will still be applied as usual"
        set_dof_note_step_1_pt_2 = QLabel(set_dof_note_text)
        set_dof_note_text = "2. For the f stop option, distance will be clamped to 64 units"
        set_dof_note_step_2 = QLabel(set_dof_note_text)
        set_dof_note_font = QFont()
        set_dof_note_font.setBold(True)
        set_dof_note_step_1_pt_1.setFont(set_dof_note_font)
        set_dof_note_step_1_pt_2.setFont(set_dof_note_font)
        set_dof_note_step_2.setFont(set_dof_note_font)
        third_tab_layout.addWidget(set_dof_instructions_step_one)
        third_tab_layout.addWidget(set_dof_instructions_step_two)
        third_tab_layout.addWidget(set_dof_instructions_step_three)
        third_tab_layout.addWidget(set_dof_tip)
        third_tab_layout.addWidget(set_dof_note_step_1_pt_1)
        third_tab_layout.addWidget(set_dof_note_step_1_pt_2)
        third_tab_layout.addWidget(set_dof_note_step_2)

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

        disable_dof_text = ' 1. Select your camera in the outliner '
        disable_dof_instructions_step_one = QLabel(disable_dof_text)
        disable_dof_text = '\n 2. Select your distance dimension on in the outliner'
        disable_dof_instructions_step_two = QLabel(disable_dof_text)
        disable_dof_text = '\n 3. Disable DOF by clicking on the button below'
        disable_dof_instructions_step_three = QLabel(disable_dof_text)
        disable_dof_tip = QLabel('Make sure both camera + distance dimension is selected')
        disable_dof_tip_font = QFont('Arial', 15)
        disable_dof_tip_font.setItalic(True)
        disable_dof_tip.setFont(disable_dof_tip_font)
        disable_dof_note = QLabel("NOTE: You need to delete locators manually")
        disable_dof_note_font = QFont('Arial', 15)
        disable_dof_note_font.setBold(True)
        disable_dof_note.setFont(disable_dof_note_font)
        third_tab_layout.addWidget(disable_dof_instructions_step_one)
        third_tab_layout.addWidget(disable_dof_instructions_step_two)
        third_tab_layout.addWidget(disable_dof_instructions_step_three)
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

        set_up_curve_text = ' 1. Select your object in the outliner \n'
        set_up_curve_instructions_step_one = QLabel(set_up_curve_text)
        set_up_curve_text = ' 2. Click on the button below to create the circle'
        set_up_curve_instructions_step_two = QLabel(set_up_curve_text)
        set_up_curve_instructions_step_one.setFont(instructions_font)
        set_up_curve_instructions_step_two.setFont(instructions_font)
        fourth_tab_layout.addWidget(set_up_curve_instructions_step_one)
        fourth_tab_layout.addWidget(set_up_curve_instructions_step_two)

        set_up_curve_button = QPushButton("Create Circle")
        set_up_curve_button.clicked.connect(self.create_curve)
        fourth_tab_layout.addWidget(set_up_curve_button)

        #Set Up Animation section
        set_up_anim_header = QLabel("Turntable animation: Setup Camera Animation")
        set_up_anim_header.setFont(header_font)
        fourth_tab_layout.addWidget(set_up_anim_header)

        set_up_anim_text = ' 1. Select your Camera on the outliner \n '
        set_up_anim_instruct_step_one = QLabel(set_up_anim_text)
        set_up_anim_text = '2. Select your curve on the outliner \n'
        set_up_anim_instruct_step_two = QLabel(set_up_anim_text)
        set_up_anim_text = ' 3. Click on the Animate Camera button to setup the animation'
        set_up_anim_instruct_step_three = QLabel(set_up_anim_text)
        set_up_anim_instruct.setFont(instructions_font)
        set_up_animation_tip = QLabel('Make sure both camera + distance dimension is selected')
        set_up_animation_tip_font = QFont('Arial', 15)
        set_up_animation_tip_font.setItalic(True)
        set_up_animation_tip.setFont(set_up_animation_tip_font)
        fourth_tab_layout.addWidget(set_up_anim_instruct_step_one)
        fourth_tab_layout.addWidget(set_up_anim_instruct_step_two)
        fourth_tab_layout.addWidget(set_up_anim_instruct_step_three)
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


    def create_camera(self):
        '''
        Creates an AlexaLF camera and sets the film back. 
        Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
        '''
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.camera(n="ShotCamera",horizontalFilmAperture=1.247,verticalFilmAperture=0.702,farClipPlane=100000)
        set_default_settings()


    def set_aspect_ratio(self):
        '''
        #adjust aspect ratio 
        '''
        menu_value = self.camera_dropdown.currentText()
        if menu_value == "4:3":
            set_four_by_three_settings()
        elif menu_value == "16:9":
            set_default_settings()
        elif menu_value == "16:10":
            set_sixteen_by_ten_settings()
        elif menu_value == "3:2":
            set_three_by_two_settings()


    def alexa_camera(self):
        '''
        Sets the camera Aperature made by the pipeline to match an AlexaLF camera.
        And sets the scene Render Settings to HD.
        '''
        cmds.setAttr(get_selected_cam_shape()+".horizontalFilmAperture", 1.247)
        cmds.setAttr(get_selected_cam_shape()+".verticalFilmAperture", 0.702)
        cmds.setAttr(get_selected_cam_shape()+".farClipPlane", 100000)
        set_default_settings()


    def set_focal_length(self):
        '''
        Set the focal length of the camera via the confirm focal length button
        '''
        menu_value = self.focal_length_dropdown.currentText()
        adjust_focal_length(float(menu_value))


    def set_locator_scale(self):
        '''
        Set the locator scale of the camera via the confirm locator scale button  
        '''
        menu_value = self.locator_scale_dropdown.currentText()
        adjust_locator_scale(float(menu_value))


    def add_depth_of_field(self):
        '''
        Add DOF rig via Focal length   
        '''
        shot_camera_shape, dist_dimension_shape = basic_depth_of_field_settings()
        cmds.connectAttr(dist_dimension_shape + '.distance', shot_camera_shape+'.focusDistance')
        #do the same for arnold render view
        cmds.setAttr(shot_camera_shape + ".aiEnableDOF", True)
        cmds.setAttr(shot_camera_shape + ".aiApertureSize", 2.8)
        cmds.connectAttr(dist_dimension_shape + '.distance', shot_camera_shape+'.aiFocusDistance')


    def add_depth_of_field_fstop(self):
        '''
        Connect DOF via f stop, distance will be clamped to 64 units if it goes above
        '''
        shot_camera_shape, dist_dimension_shape = basic_depth_of_field_settings()
        cmds.connectAttr(dist_dimension_shape + '.distance', shot_camera_shape+'.fStop')


    def disable_depth_of_field(self):
        '''
        Disable Depth of Field Rig of camera (focal distance + fStop)
        '''
        camera_shape = get_selected_cam_shape()
        dist_dimension_shape = get_object_to_focus()
        cmds.delete(dist_dimension_shape)
        cmds.setAttr(camera_shape+".depthOfField", False)
        cmds.setAttr(camera_shape + ".aiEnableDOF", False)

    def create_curve(self):
        '''
        Create circular turntable curve
        '''
        obj = get_obj()
        obj_x = cmds.getAttr(obj + '.translateX')
        obj_y = cmds.getAttr(obj + '.translateY')
        obj_z = cmds.getAttr(obj + '.translateZ')
        turntable_circle = cmds.circle(nr=(0, 0, 1), c=(obj_x, obj_y, obj_z), r=1000)
        cmds.setAttr(turntable_circle[0] + '.rotateX', -90)

    def animate_camera(self):
        '''
        - Creates turntable animation for moving the camera
        - Increase camera angle at the Y axis by 45 degrees in every quarter
        both tangent types are spline to use a non-linear interpolation
        for a smoother animation for camera
        '''
        cam = get_selected_cam_transform()
        curve = get_object_to_focus()
        cmds.pathAnimation(curve,cam,stu = 0,etu = 180,follow = True,fractionMode = True)
        cmds.setAttr(cam + '.rotateX', 0)
        cmds.setAttr(cam + '.rotateY', 180)

        cmds.currentTime(0)
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.setKeyframe(cam,attribute = 'rotateX',value = 0,inTangentType="spline",outTangentType="spline")
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.setKeyframe(cam,attribute = 'rotateY',value = -180,inTangentType="spline",outTangentType="spline")
        cmds.currentTime(45)
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.setKeyframe(cam,attribute = 'rotateY',value = -135,inTangentType="spline",outTangentType="spline")
        cmds.currentTime(90)
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.setKeyframe(cam,attribute = 'rotateY',value = 0,inTangentType="spline",outTangentType="spline")
        cmds.currentTime(135)
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.setKeyframe(cam,attribute = 'rotateY',value = 135,inTangentType="spline",outTangentType="spline")
        cmds.currentTime(180)
        # Ignore C0301 warning because we can't change the name of arguments from Maya API
        cmds.setKeyframe(cam, attribute = 'rotateY',value = 180,inTangentType="spline",outTangentType="spline")

if __name__ == '__main__':
    tab_window = CameraTool()

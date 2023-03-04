'''
This script is purely served as a code extract for the previous UI. 
It will not run on its own nor imported into ala_cameraTools.0.0.3.py
script. Therefore treat it as a pseudo code here. 
'''
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
        cmds.text('1. Select your camera in the outliner \n 2. Select your object to focus on in the outliner')
        cmds.text('Make sure both camera + object is selected', fn='obliqueLabelFont')
        cmds.text('3. Apply DOF by clicking on the button below')
        cmds.text("\n\nNOTE: \n1. if the focused object's coordinates is at the origin, \nthe aim locator will not spawn but DOF will still be applied as usual", fn='smallObliqueLabelFont')
        cmds.text('2. For the f stop option, distance will be clamped to 64 units', fn='smallObliqueLabelFont')
        cmds.separator(h=20)
    
        cmds.button(label = 'Enable DOF Focal Length', command = 'add_depth_of_field()')
        cmds.separator(h=10)
        cmds.button(label = 'Enable DOF f Stop', command = 'add_depth_of_field_fstop()')
        cmds.separator(h=20)
        cmds.text('Depth of Field: Disable DOF Rig', fn='fixedWidthFont')
        cmds.text('1. Select your camera in the outliner \n 2. Select your distance dimension on in the outliner')
        cmds.text('Make sure both camera + distance dimension is selected', fn='obliqueLabelFont')
        cmds.text('3. Disable DOF by clicking on the button below')
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
        cmds.text('1. Select your Camera on the outliner \n 2. Select your curve on the outliner')
        cmds.text('Make sure both camera + curve is selected', fn='obliqueLabelFont')
        cmds.text('3. Click on the Animate Camera button to setup the animation')
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
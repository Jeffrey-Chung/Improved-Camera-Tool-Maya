# Improved Camera Tool Maya

Purpose of tool: Ensure that object is always in focus regardless of distance.
 Add additions to the camera tool already completed based on the video here: https://www.youtube.com/watch?v=Yny3tsD_Qhk 
<br/>
<br/>
<ins>Usage</ins> <br/>
<b>Tab 1: Creates camera + Set Aspect Ratio</b>  <br/>
1. The `Create Camera` button would create a shot camera with `horizontalFilmAperture` set to 1.247, `verticalFilmAperture` set to 0.702 and `farClipPlane` set to 100000
2. The dropdown below would set the aspect ratio. Possible options would be `4:3`, `16:9`, `16:10` and `3:2`.
3. The `Sets AlexaLF` button would set the camera aperature to match an AlexaLF camera.

<b>Tab 2: Adjust camera settings via Option Menus</b>  <br/>
1. Option Menu at the top would set the focal length of the camera, ranging from 12mm to 150mm
2. Option Menu at the bottom would set the locator scale of the camera, ranging from 5mm to 100mm

<b>Tab 3: Setup/Disable DOF Rig</b>  <br/>
1.  The `Enable DOF Focal Length` button would create a DOF rig with focal length. As distance increases, focal length increases, ensuring that DOF is maintained.
2. The `Enable DOF f stop` button would create a DOF rig with f stop. As distance increases, f stop increases but f stop value will be clamped to 64 maximum.
3. The `Disable DOF` button would delete the DOF rig, but you need to remove the locators manually.

<b>Tab 4: Turntable camera animation</b>  <br/>
1. The `Create Circle` button would create a circle for the turntable.
2. The `Animate Camera` button would attach the camera to the circle and animate the camera motion by creating frames every 45 seconds.

<ins>Improvements 2022-2023</ins> <br/>
1. Depth of Field (DOF) rig can be added to camera as long as you select a camera and an object to focus on
2. DOF is similarly applied for Arnold as well simuntaneously
3. Locator Scale of can be adjusted similarly to focal length
4. Lots of refactored code into separate functions
5. UI is reverted back to original colour scale temporarily for a search for better colour scheme than blue and white
6. UI has reduced to minimal size
7. In relation to 3. both features can be adjusted via a dropdown menu on the 'Camera Settings' tab
8. Can disable DOF rig, but need to delete locators separately
9. Can adjust aspect ratio of camera before creating one
10. DOF can also be applied via f stop, f stop value will be clamped to 64 maximum
11. Camera can be animated around an object (similar to Animation Window -> Visualize -> Create Turntable for a camera)

<ins>Improvements 2024</ins> <br/>
1. Pylint is used to check for code quality and refactored based on its suggestions, this will also be checked in a pull request.
# Improved Camera Tool Maya

Purpose of tool: Ensure that object is always in focus regardless of distance.
 Add additions to the camera tool already completed based on the video here: https://www.youtube.com/watch?v=Yny3tsD_Qhk 
<br/>
<br/>
<ins>Improvements:</ins> <br/>
1. Depth of Field (DOF) rig can be added to camera as long as you select a camera and an object to focus on <br/>
2. DOF is similarly applied for Arnold as well simuntaneously <br/>
3. Locator Scale of can be adjusted similarly to focal length <br/>
4. Lots of refactored code into separate functions <br/>
5. UI is reverted back to original colour scale temporarily for a search for better colour scheme than blue and white <br/>
6. UI has reduced to minimal size <br />
7. In relation to 3. both features can be adjusted via a dropdown menu on the 'Camera Settings' tab <br />
8. Can disable DOF rig, but need to delete locators separately <br />
9. Can adjust aspect ratio of camera before creating one <br />
10. DOF can also be applied via f stop, f stop value will be clamped to 64 maximum <br />
11. Camera can be animated around an object (similar to Animation Window -> Visualize -> Create Turntable for a camera)<br />
12. Pylint is used to check for code quality, this will also be checked in a pull request.
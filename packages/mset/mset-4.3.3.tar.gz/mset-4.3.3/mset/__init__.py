from typing import Any, List, Tuple, Callable, Union
from __future__ import annotations


class __MsetClient:
	def __init__(self, name):
		"""Attempt to connect to running instance of Toolbag."""
		pass
	def exec(self, *args):
		"""Execute code directly in that instance of Toolbag."""
		pass

cur_server = __MsetClient()

class TextureProjectLayer:
	"""
	A Texture Project Layer (Fill, Stroke, etc.).
	"""
	
	__handle = None
	def __get_activeProjectMaps(self) -> List[str]:
		return cur_server.exec('mset.TextureProjectLayer.get_activeProjectMaps', __handle)

	def __set_activeProjectMaps(self, _activeProjectMaps: List[str]):
		return cur_server.exec('mset.TextureProjectLayer.set_activeProjectMaps', __handle, _activeProjectMaps)

	activeProjectMaps: List[str] = property(__get_activeProjectMaps, __set_activeProjectMaps)
	"""The active project maps for this layer."""
	
	def __get_contentChildren(self) -> List[TextureProjectLayer]:
		return cur_server.exec('mset.TextureProjectLayer.get_contentChildren', __handle)

	def __set_contentChildren(self, _contentChildren: List[TextureProjectLayer]):
		return cur_server.exec('mset.TextureProjectLayer.set_contentChildren', __handle, _contentChildren)

	contentChildren: List[TextureProjectLayer] = property(__get_contentChildren, __set_contentChildren)
	"""This layers content children."""
	
	def __get_maps(self) -> TextureProjectLayerMaps:
		return cur_server.exec('mset.TextureProjectLayer.get_maps', __handle)

	def __set_maps(self, _maps: TextureProjectLayerMaps):
		return cur_server.exec('mset.TextureProjectLayer.set_maps', __handle, _maps)

	maps: TextureProjectLayerMaps = property(__get_maps, __set_maps)
	"""The per map settings of this layer."""
	
	def __get_maskChildren(self) -> List[TextureProjectLayer]:
		return cur_server.exec('mset.TextureProjectLayer.get_maskChildren', __handle)

	def __set_maskChildren(self, _maskChildren: List[TextureProjectLayer]):
		return cur_server.exec('mset.TextureProjectLayer.set_maskChildren', __handle, _maskChildren)

	maskChildren: List[TextureProjectLayer] = property(__get_maskChildren, __set_maskChildren)
	"""This layers mask children."""
	
	def __get_maskColor(self) -> float:
		return cur_server.exec('mset.TextureProjectLayer.get_maskColor', __handle)

	def __set_maskColor(self, _maskColor: float):
		return cur_server.exec('mset.TextureProjectLayer.set_maskColor', __handle, _maskColor)

	maskColor: float = property(__get_maskColor, __set_maskColor)
	"""The mask color of this layer. Works similar to opacity, but for the mask tree."""
	
	def __get_name(self) -> str:
		return cur_server.exec('mset.TextureProjectLayer.get_name', __handle)

	def __set_name(self, _name: str):
		return cur_server.exec('mset.TextureProjectLayer.set_name', __handle, _name)

	name: str = property(__get_name, __set_name)
	"""The name of this layer."""
	
	def __get_opacity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayer.get_opacity', __handle)

	def __set_opacity(self, _opacity: float):
		return cur_server.exec('mset.TextureProjectLayer.set_opacity', __handle, _opacity)

	opacity: float = property(__get_opacity, __set_opacity)
	"""The transparency of this layer."""
	
	def __get_parent(self) -> TextureProjectLayer:
		return cur_server.exec('mset.TextureProjectLayer.get_parent', __handle)

	def __set_parent(self, _parent: TextureProjectLayer):
		return cur_server.exec('mset.TextureProjectLayer.set_parent', __handle, _parent)

	parent: TextureProjectLayer = property(__get_parent, __set_parent)
	"""The parent of this layer."""
	
	def __get_uid(self) -> int:
		return cur_server.exec('mset.TextureProjectLayer.get_uid', __handle)

	def __set_uid(self, _uid: int):
		return cur_server.exec('mset.TextureProjectLayer.set_uid', __handle, _uid)

	uid: int = property(__get_uid, __set_uid)
	"""The unique identifier of this layer."""
	
	def addContentChild(self, contentType: str) -> TextureProjectLayer:
		"""
		Get a parameter in this layer's mask.
		"""
		return cur_server.exec('mset.TextureProjectLayer.addContentChild', __handle, contentType)

	def addMaskChild(self, maskType: str) -> TextureProjectLayer:
		"""
		Set a given parameter for this layer's mask.
		"""
		return cur_server.exec('mset.TextureProjectLayer.addMaskChild', __handle, maskType)

	def duplicate(self) -> TextureProjectLayer:
		"""
		Duplcates this layer in this painter project. Returns duplicated layer.
		"""
		return cur_server.exec('mset.TextureProjectLayer.duplicate', __handle)

	def getBlendMode(self, projectMap: str):
		"""
		Gets the blend mode of this layer for a given project map.
		"""
		return cur_server.exec('mset.TextureProjectLayer.getBlendMode', __handle, projectMap)

	def isDescendantOfMask(self):
		"""
		Checks if this layer is a descendant of a mask layer for this painter project.
		"""
		return cur_server.exec('mset.TextureProjectLayer.isDescendantOfMask', __handle)

	def moveDown(self):
		"""
		Moves this layer down it's parent list in the painter project.
		"""
		return cur_server.exec('mset.TextureProjectLayer.moveDown', __handle)

	def moveUp(self):
		"""
		Moves this layer up it's parent list in the painter project.
		"""
		return cur_server.exec('mset.TextureProjectLayer.moveUp', __handle)

	def remove(self):
		"""
		Removes this layer from this painter project.
		"""
		return cur_server.exec('mset.TextureProjectLayer.remove', __handle)

	def setBlendMode(self, projectMap: str, mode: str):
		"""
		Sets the blend mode of this layer for a given project map.
		"""
		return cur_server.exec('mset.TextureProjectLayer.setBlendMode', __handle, projectMap,mode)


class BakerMap:
	"""
	Baker Map Settings
	"""
	
	__handle = None
	def __get_enabled(self) -> bool:
		return cur_server.exec('mset.BakerMap.get_enabled', __handle)

	def __set_enabled(self, _enabled: bool):
		return cur_server.exec('mset.BakerMap.set_enabled', __handle, _enabled)

	enabled: bool = property(__get_enabled, __set_enabled)
	"""Whether or not this Baker Map should render when baking."""
	
	def __get_suffix(self) -> str:
		return cur_server.exec('mset.BakerMap.get_suffix', __handle)

	def __set_suffix(self, _suffix: str):
		return cur_server.exec('mset.BakerMap.set_suffix', __handle, _suffix)

	suffix: str = property(__get_suffix, __set_suffix)
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix(self):
		"""
		Resets the current map suffix to its default.
		"""
		return cur_server.exec('mset.BakerMap.resetSuffix', __handle)


class UIControl:
	"""
	User Interface Control
	"""
	
	__handle = None

class SceneObject:
	"""
	Scene Object
	"""
	
	__handle = None
	def __get_collapsed(self) -> bool:
		return cur_server.exec('mset.SceneObject.get_collapsed', __handle)

	def __set_collapsed(self, _collapsed: bool):
		return cur_server.exec('mset.SceneObject.set_collapsed', __handle, _collapsed)

	collapsed: bool = property(__get_collapsed, __set_collapsed)
	"""Controls the display of the object's children in the outline view."""
	
	def __get_locked(self) -> bool:
		return cur_server.exec('mset.SceneObject.get_locked', __handle)

	def __set_locked(self, _locked: bool):
		return cur_server.exec('mset.SceneObject.set_locked', __handle, _locked)

	locked: bool = property(__get_locked, __set_locked)
	"""Controls the locking of object settings in the user interface."""
	
	def __get_name(self) -> str:
		return cur_server.exec('mset.SceneObject.get_name', __handle)

	def __set_name(self, _name: str):
		return cur_server.exec('mset.SceneObject.set_name', __handle, _name)

	name: str = property(__get_name, __set_name)
	"""The name of the object."""
	
	def __get_parent(self) -> SceneObject:
		return cur_server.exec('mset.SceneObject.get_parent', __handle)

	def __set_parent(self, _parent: SceneObject):
		return cur_server.exec('mset.SceneObject.set_parent', __handle, _parent)

	parent: SceneObject = property(__get_parent, __set_parent)
	"""The parent of the object."""
	
	def __get_visible(self) -> bool:
		return cur_server.exec('mset.SceneObject.get_visible', __handle)

	def __set_visible(self, _visible: bool):
		return cur_server.exec('mset.SceneObject.set_visible', __handle, _visible)

	visible: bool = property(__get_visible, __set_visible)
	"""Controls object viewport visibility."""
	
	def destroy(self):
		"""
		Destroys the object and removes it from the scene.
		"""
		return cur_server.exec('mset.SceneObject.destroy', __handle)

	def duplicate(self, name: str = '') -> SceneObject:
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		return cur_server.exec('mset.SceneObject.duplicate', __handle, name='')

	def findInChildren(self, searchStr: str) -> SceneObject:
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		return cur_server.exec('mset.SceneObject.findInChildren', __handle, searchStr)

	def getBounds(self) -> List[List[float]]:
		"""
		Gets the bounds of this object, or None if it doesn't have any. Formatted as [min_xyz, max_xyz]
		"""
		return cur_server.exec('mset.SceneObject.getBounds', __handle)

	def getChildren(self) -> List[SceneObject]:
		"""
		Returns a list of all immediate children of the object.
		"""
		return cur_server.exec('mset.SceneObject.getChildren', __handle)

	def setKeyframe(self, lerp: str):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		return cur_server.exec('mset.SceneObject.setKeyframe', __handle, lerp)


class TransformObject(SceneObject):
	"""
	Transform Object
	"""
	
	__handle = None
	def __get_pivot(self) -> List[float]:
		return cur_server.exec('mset.TransformObject.get_pivot', __handle)

	def __set_pivot(self, _pivot: List[float]):
		return cur_server.exec('mset.TransformObject.set_pivot', __handle, _pivot)

	pivot: List[float] = property(__get_pivot, __set_pivot)
	"""The pivot of the object, as a list of 3 floats."""
	
	def __get_position(self) -> List[float]:
		return cur_server.exec('mset.TransformObject.get_position', __handle)

	def __set_position(self, _position: List[float]):
		return cur_server.exec('mset.TransformObject.set_position', __handle, _position)

	position: List[float] = property(__get_position, __set_position)
	"""The position of the object, as a list of 3 floats."""
	
	def __get_rotation(self) -> List[float]:
		return cur_server.exec('mset.TransformObject.get_rotation', __handle)

	def __set_rotation(self, _rotation: List[float]):
		return cur_server.exec('mset.TransformObject.set_rotation', __handle, _rotation)

	rotation: List[float] = property(__get_rotation, __set_rotation)
	"""The rotation of the object, as a list of 3 floats."""
	
	def __get_scale(self) -> List[float]:
		return cur_server.exec('mset.TransformObject.get_scale', __handle)

	def __set_scale(self, _scale: List[float]):
		return cur_server.exec('mset.TransformObject.set_scale', __handle, _scale)

	scale: List[float] = property(__get_scale, __set_scale)
	"""The scale of the object, as a list of 3 floats."""
	
	def centerPivot(self):
		"""
		Centers the pivot point of this object to its bounding box.
		"""
		return cur_server.exec('mset.TransformObject.centerPivot', __handle)


class UIBaseTextField(UIControl):
	"""
	UI Base Text Field. Abstract class, do not use in your plugins.
	"""
	
	__handle = None
	def __get_onCancel(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIBaseTextField.get_onCancel', __handle)

	def __set_onCancel(self, _onCancel: Callable[[], None]):
		return cur_server.exec('mset.UIBaseTextField.set_onCancel', __handle, _onCancel)

	onCancel: Callable[[], None] = property(__get_onCancel, __set_onCancel)
	"""A callable, called when text editing is canceled."""
	
	def __get_onChange(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIBaseTextField.get_onChange', __handle)

	def __set_onChange(self, _onChange: Callable[[], None]):
		return cur_server.exec('mset.UIBaseTextField.set_onChange', __handle, _onChange)

	onChange: Callable[[], None] = property(__get_onChange, __set_onChange)
	"""A callable, called when the text is changed."""
	
	def __get_width(self) -> float:
		return cur_server.exec('mset.UIBaseTextField.get_width', __handle)

	def __set_width(self, _width: float):
		return cur_server.exec('mset.UIBaseTextField.set_width', __handle, _width)

	width: float = property(__get_width, __set_width)
	"""The width of the control."""
	

class UIBaseSlider(UIControl):
	"""
	UI Base Slider. Abstract class, do not use in your plugins.
	"""
	
	__handle = None
	def __get_onChange(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIBaseSlider.get_onChange', __handle)

	def __set_onChange(self, _onChange: Callable[[], None]):
		return cur_server.exec('mset.UIBaseSlider.set_onChange', __handle, _onChange)

	onChange: Callable[[], None] = property(__get_onChange, __set_onChange)
	"""A callable, called when the tracked value changes."""
	
	def __get_width(self) -> float:
		return cur_server.exec('mset.UIBaseSlider.get_width', __handle)

	def __set_width(self, _width: float):
		return cur_server.exec('mset.UIBaseSlider.set_width', __handle, _width)

	width: float = property(__get_width, __set_width)
	"""The width of the control."""
	

class Callbacks:
	"""
	Callbacks
	"""
	
	__handle = None
	def __get_onPeriodicUpdate(self) -> Callable[[],None]:
		return cur_server.exec('mset.Callbacks.get_onPeriodicUpdate', __handle)

	def __set_onPeriodicUpdate(self, _onPeriodicUpdate: Callable[[], None]):
		return cur_server.exec('mset.Callbacks.set_onPeriodicUpdate', __handle, _onPeriodicUpdate)

	onPeriodicUpdate: Callable[[], None] = property(__get_onPeriodicUpdate, __set_onPeriodicUpdate)
	"""This Callback will run periodically: a few times per second. This can be useful for plugins that need to refresh external files or make frequent polling checks. Since this callback is run frequently, care should be taken to keep the average execution time low, or poor performance could result."""
	
	def __get_onRegainFocus(self) -> Callable[[],None]:
		return cur_server.exec('mset.Callbacks.get_onRegainFocus', __handle)

	def __set_onRegainFocus(self, _onRegainFocus: Callable[[], None]):
		return cur_server.exec('mset.Callbacks.set_onRegainFocus', __handle, _onRegainFocus)

	onRegainFocus: Callable[[], None] = property(__get_onRegainFocus, __set_onRegainFocus)
	"""This Callback will run when the application regains focus. This can be useful for plugins that need to refresh files or make other checks when the user switches to Toolbag."""
	
	def __get_onSceneChanged(self) -> Callable[[],None]:
		return cur_server.exec('mset.Callbacks.get_onSceneChanged', __handle)

	def __set_onSceneChanged(self, _onSceneChanged: Callable[[], None]):
		return cur_server.exec('mset.Callbacks.set_onSceneChanged', __handle, _onSceneChanged)

	onSceneChanged: Callable[[], None] = property(__get_onSceneChanged, __set_onSceneChanged)
	"""This Callback will run when the scene is changed (e.g. by moving an object)."""
	
	def __get_onSceneLoaded(self) -> Callable[[],None]:
		return cur_server.exec('mset.Callbacks.get_onSceneLoaded', __handle)

	def __set_onSceneLoaded(self, _onSceneLoaded: Callable[[], None]):
		return cur_server.exec('mset.Callbacks.set_onSceneLoaded', __handle, _onSceneLoaded)

	onSceneLoaded: Callable[[], None] = property(__get_onSceneLoaded, __set_onSceneLoaded)
	"""This Callback will run when a new scene is loaded."""
	
	def __get_onShutdownPlugin(self) -> Callable[[],None]:
		return cur_server.exec('mset.Callbacks.get_onShutdownPlugin', __handle)

	def __set_onShutdownPlugin(self, _onShutdownPlugin: Callable[[], None]):
		return cur_server.exec('mset.Callbacks.set_onShutdownPlugin', __handle, _onShutdownPlugin)

	onShutdownPlugin: Callable[[], None] = property(__get_onShutdownPlugin, __set_onShutdownPlugin)
	"""This Callback will run immediately before the plugin is shut down."""
	

class CameraLens:
	"""
	Camera Lens Settings
	"""
	
	__handle = None
	def __get_distortionBarrel(self) -> float:
		return cur_server.exec('mset.CameraLens.get_distortionBarrel', __handle)

	def __set_distortionBarrel(self, _distortionBarrel: float):
		return cur_server.exec('mset.CameraLens.set_distortionBarrel', __handle, _distortionBarrel)

	distortionBarrel: float = property(__get_distortionBarrel, __set_distortionBarrel)
	"""Strength of the barrel distortion effect."""
	
	def __get_distortionCABlue(self) -> float:
		return cur_server.exec('mset.CameraLens.get_distortionCABlue', __handle)

	def __set_distortionCABlue(self, _distortionCABlue: float):
		return cur_server.exec('mset.CameraLens.set_distortionCABlue', __handle, _distortionCABlue)

	distortionCABlue: float = property(__get_distortionCABlue, __set_distortionCABlue)
	"""Strength of the chromatic aberration in the blue component."""
	
	def __get_distortionCAGreen(self) -> float:
		return cur_server.exec('mset.CameraLens.get_distortionCAGreen', __handle)

	def __set_distortionCAGreen(self, _distortionCAGreen: float):
		return cur_server.exec('mset.CameraLens.set_distortionCAGreen', __handle, _distortionCAGreen)

	distortionCAGreen: float = property(__get_distortionCAGreen, __set_distortionCAGreen)
	"""Strength of the chromatic aberration in the green component."""
	
	def __get_distortionCARed(self) -> float:
		return cur_server.exec('mset.CameraLens.get_distortionCARed', __handle)

	def __set_distortionCARed(self, _distortionCARed: float):
		return cur_server.exec('mset.CameraLens.set_distortionCARed', __handle, _distortionCARed)

	distortionCARed: float = property(__get_distortionCARed, __set_distortionCARed)
	"""Strength of the chromatic aberration in the red component."""
	
	def __get_distortionChromaticAberration(self) -> float:
		return cur_server.exec('mset.CameraLens.get_distortionChromaticAberration', __handle)

	def __set_distortionChromaticAberration(self, _distortionChromaticAberration: float):
		return cur_server.exec('mset.CameraLens.set_distortionChromaticAberration', __handle, _distortionChromaticAberration)

	distortionChromaticAberration: float = property(__get_distortionChromaticAberration, __set_distortionChromaticAberration)
	"""Strength of the chromatic aberration effect."""
	
	def __get_dofAperture(self) -> str:
		return cur_server.exec('mset.CameraLens.get_dofAperture', __handle)

	def __set_dofAperture(self, _dofAperture: str):
		return cur_server.exec('mset.CameraLens.set_dofAperture', __handle, _dofAperture)

	dofAperture: str = property(__get_dofAperture, __set_dofAperture)
	"""Path of the aperture shape texture file."""
	
	def __get_dofApertureRotation(self) -> float:
		return cur_server.exec('mset.CameraLens.get_dofApertureRotation', __handle)

	def __set_dofApertureRotation(self, _dofApertureRotation: float):
		return cur_server.exec('mset.CameraLens.set_dofApertureRotation', __handle, _dofApertureRotation)

	dofApertureRotation: float = property(__get_dofApertureRotation, __set_dofApertureRotation)
	"""Rotation of the aperture shape texture."""
	
	def __get_dofEnabled(self) -> bool:
		return cur_server.exec('mset.CameraLens.get_dofEnabled', __handle)

	def __set_dofEnabled(self, _dofEnabled: bool):
		return cur_server.exec('mset.CameraLens.set_dofEnabled', __handle, _dofEnabled)

	dofEnabled: bool = property(__get_dofEnabled, __set_dofEnabled)
	"""Enables the depth of field effect."""
	
	def __get_dofFarBlur(self) -> float:
		return cur_server.exec('mset.CameraLens.get_dofFarBlur', __handle)

	def __set_dofFarBlur(self, _dofFarBlur: float):
		return cur_server.exec('mset.CameraLens.set_dofFarBlur', __handle, _dofFarBlur)

	dofFarBlur: float = property(__get_dofFarBlur, __set_dofFarBlur)
	"""Far blur of the depth of field."""
	
	def __get_dofFocusDistance(self) -> float:
		return cur_server.exec('mset.CameraLens.get_dofFocusDistance', __handle)

	def __set_dofFocusDistance(self, _dofFocusDistance: float):
		return cur_server.exec('mset.CameraLens.set_dofFocusDistance', __handle, _dofFocusDistance)

	dofFocusDistance: float = property(__get_dofFocusDistance, __set_dofFocusDistance)
	"""Focal distance of the depth of field."""
	
	def __get_dofMaxBokehSize(self) -> float:
		return cur_server.exec('mset.CameraLens.get_dofMaxBokehSize', __handle)

	def __set_dofMaxBokehSize(self, _dofMaxBokehSize: float):
		return cur_server.exec('mset.CameraLens.set_dofMaxBokehSize', __handle, _dofMaxBokehSize)

	dofMaxBokehSize: float = property(__get_dofMaxBokehSize, __set_dofMaxBokehSize)
	"""Maximum bokeh size of the depth of field."""
	
	def __get_dofNearBlur(self) -> float:
		return cur_server.exec('mset.CameraLens.get_dofNearBlur', __handle)

	def __set_dofNearBlur(self, _dofNearBlur: float):
		return cur_server.exec('mset.CameraLens.set_dofNearBlur', __handle, _dofNearBlur)

	dofNearBlur: float = property(__get_dofNearBlur, __set_dofNearBlur)
	"""Near blur scale of the depth of field."""
	
	def __get_dofSwirlVignette(self) -> float:
		return cur_server.exec('mset.CameraLens.get_dofSwirlVignette', __handle)

	def __set_dofSwirlVignette(self, _dofSwirlVignette: float):
		return cur_server.exec('mset.CameraLens.set_dofSwirlVignette', __handle, _dofSwirlVignette)

	dofSwirlVignette: float = property(__get_dofSwirlVignette, __set_dofSwirlVignette)
	"""Swirl vignette amount of the depth of field."""
	
	def __get_flareSize(self) -> float:
		return cur_server.exec('mset.CameraLens.get_flareSize', __handle)

	def __set_flareSize(self, _flareSize: float):
		return cur_server.exec('mset.CameraLens.set_flareSize', __handle, _flareSize)

	flareSize: float = property(__get_flareSize, __set_flareSize)
	"""Size of the lens flare effect."""
	
	def __get_flareStrength(self) -> float:
		return cur_server.exec('mset.CameraLens.get_flareStrength', __handle)

	def __set_flareStrength(self, _flareStrength: float):
		return cur_server.exec('mset.CameraLens.set_flareStrength', __handle, _flareStrength)

	flareStrength: float = property(__get_flareStrength, __set_flareStrength)
	"""Strength of the lens flare effect."""
	
	def __get_flareThreshold(self) -> float:
		return cur_server.exec('mset.CameraLens.get_flareThreshold', __handle)

	def __set_flareThreshold(self, _flareThreshold: float):
		return cur_server.exec('mset.CameraLens.set_flareThreshold', __handle, _flareThreshold)

	flareThreshold: float = property(__get_flareThreshold, __set_flareThreshold)
	"""Threshold of the lens flare effect."""
	
	def __get_safeFrameEnabled(self) -> bool:
		return cur_server.exec('mset.CameraLens.get_safeFrameEnabled', __handle)

	def __set_safeFrameEnabled(self, _safeFrameEnabled: bool):
		return cur_server.exec('mset.CameraLens.set_safeFrameEnabled', __handle, _safeFrameEnabled)

	safeFrameEnabled: bool = property(__get_safeFrameEnabled, __set_safeFrameEnabled)
	"""Displays the safe frame in the viewport."""
	
	def __get_safeFrameOpacity(self) -> float:
		return cur_server.exec('mset.CameraLens.get_safeFrameOpacity', __handle)

	def __set_safeFrameOpacity(self, _safeFrameOpacity: float):
		return cur_server.exec('mset.CameraLens.set_safeFrameOpacity', __handle, _safeFrameOpacity)

	safeFrameOpacity: float = property(__get_safeFrameOpacity, __set_safeFrameOpacity)
	"""Opacity of the safe frame display."""
	

class CameraLimits:
	"""
	Camera Limits Settings
	"""
	
	__handle = None
	def __get_farLimit(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_farLimit', __handle)

	def __set_farLimit(self, _farLimit: float):
		return cur_server.exec('mset.CameraLimits.set_farLimit', __handle, _farLimit)

	farLimit: float = property(__get_farLimit, __set_farLimit)
	"""The far orbit limit distance."""
	
	def __get_farLimitEnabled(self) -> bool:
		return cur_server.exec('mset.CameraLimits.get_farLimitEnabled', __handle)

	def __set_farLimitEnabled(self, _farLimitEnabled: bool):
		return cur_server.exec('mset.CameraLimits.set_farLimitEnabled', __handle, _farLimitEnabled)

	farLimitEnabled: bool = property(__get_farLimitEnabled, __set_farLimitEnabled)
	"""Enables the far orbit distance limit."""
	
	def __get_nearLimit(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_nearLimit', __handle)

	def __set_nearLimit(self, _nearLimit: float):
		return cur_server.exec('mset.CameraLimits.set_nearLimit', __handle, _nearLimit)

	nearLimit: float = property(__get_nearLimit, __set_nearLimit)
	"""The near orbit limit distance."""
	
	def __get_nearLimitEnabled(self) -> bool:
		return cur_server.exec('mset.CameraLimits.get_nearLimitEnabled', __handle)

	def __set_nearLimitEnabled(self, _nearLimitEnabled: bool):
		return cur_server.exec('mset.CameraLimits.set_nearLimitEnabled', __handle, _nearLimitEnabled)

	nearLimitEnabled: bool = property(__get_nearLimitEnabled, __set_nearLimitEnabled)
	"""Enables the near orbit distance limit."""
	
	def __get_panLimit(self) -> str:
		return cur_server.exec('mset.CameraLimits.get_panLimit', __handle)

	def __set_panLimit(self, _panLimit: str):
		return cur_server.exec('mset.CameraLimits.set_panLimit', __handle, _panLimit)

	panLimit: str = property(__get_panLimit, __set_panLimit)
	"""Limits the panning to either the Y-axis or completly (valid values are: 'Off', 'YAxis', 'Locked')."""
	
	def __get_pitchLimitEnabled(self) -> bool:
		return cur_server.exec('mset.CameraLimits.get_pitchLimitEnabled', __handle)

	def __set_pitchLimitEnabled(self, _pitchLimitEnabled: bool):
		return cur_server.exec('mset.CameraLimits.set_pitchLimitEnabled', __handle, _pitchLimitEnabled)

	pitchLimitEnabled: bool = property(__get_pitchLimitEnabled, __set_pitchLimitEnabled)
	"""Enables the pitch angle limit."""
	
	def __get_pitchLimitMax(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_pitchLimitMax', __handle)

	def __set_pitchLimitMax(self, _pitchLimitMax: float):
		return cur_server.exec('mset.CameraLimits.set_pitchLimitMax', __handle, _pitchLimitMax)

	pitchLimitMax: float = property(__get_pitchLimitMax, __set_pitchLimitMax)
	"""The maximum pitch angle, in degrees."""
	
	def __get_pitchLimitMin(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_pitchLimitMin', __handle)

	def __set_pitchLimitMin(self, _pitchLimitMin: float):
		return cur_server.exec('mset.CameraLimits.set_pitchLimitMin', __handle, _pitchLimitMin)

	pitchLimitMin: float = property(__get_pitchLimitMin, __set_pitchLimitMin)
	"""The minimum pitch angle, in degrees."""
	
	def __get_useLimitsInViewport(self) -> bool:
		return cur_server.exec('mset.CameraLimits.get_useLimitsInViewport', __handle)

	def __set_useLimitsInViewport(self, _useLimitsInViewport: bool):
		return cur_server.exec('mset.CameraLimits.set_useLimitsInViewport', __handle, _useLimitsInViewport)

	useLimitsInViewport: bool = property(__get_useLimitsInViewport, __set_useLimitsInViewport)
	"""Enables use of camera motion limits in the viewport."""
	
	def __get_yawLimitEnabled(self) -> bool:
		return cur_server.exec('mset.CameraLimits.get_yawLimitEnabled', __handle)

	def __set_yawLimitEnabled(self, _yawLimitEnabled: bool):
		return cur_server.exec('mset.CameraLimits.set_yawLimitEnabled', __handle, _yawLimitEnabled)

	yawLimitEnabled: bool = property(__get_yawLimitEnabled, __set_yawLimitEnabled)
	"""Enables the yaw angle limit."""
	
	def __get_yawLimitMax(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_yawLimitMax', __handle)

	def __set_yawLimitMax(self, _yawLimitMax: float):
		return cur_server.exec('mset.CameraLimits.set_yawLimitMax', __handle, _yawLimitMax)

	yawLimitMax: float = property(__get_yawLimitMax, __set_yawLimitMax)
	"""The maximum yaw limit angle, in degrees."""
	
	def __get_yawLimitMin(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_yawLimitMin', __handle)

	def __set_yawLimitMin(self, _yawLimitMin: float):
		return cur_server.exec('mset.CameraLimits.set_yawLimitMin', __handle, _yawLimitMin)

	yawLimitMin: float = property(__get_yawLimitMin, __set_yawLimitMin)
	"""The minimum yaw limit angle, in degrees."""
	
	def __get_yawLimitOffset(self) -> float:
		return cur_server.exec('mset.CameraLimits.get_yawLimitOffset', __handle)

	def __set_yawLimitOffset(self, _yawLimitOffset: float):
		return cur_server.exec('mset.CameraLimits.set_yawLimitOffset', __handle, _yawLimitOffset)

	yawLimitOffset: float = property(__get_yawLimitOffset, __set_yawLimitOffset)
	"""The offset of the yaw limit angle, in degrees."""
	

class CameraPostEffect:
	"""
	Camera Post Effect
	"""
	
	__handle = None
	def __get_bloomBrightness(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_bloomBrightness', __handle)

	def __set_bloomBrightness(self, _bloomBrightness: float):
		return cur_server.exec('mset.CameraPostEffect.set_bloomBrightness', __handle, _bloomBrightness)

	bloomBrightness: float = property(__get_bloomBrightness, __set_bloomBrightness)
	"""Brightness multiplier for the bloom effect."""
	
	def __get_bloomSize(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_bloomSize', __handle)

	def __set_bloomSize(self, _bloomSize: float):
		return cur_server.exec('mset.CameraPostEffect.set_bloomSize', __handle, _bloomSize)

	bloomSize: float = property(__get_bloomSize, __set_bloomSize)
	"""Size scalar for the bloom effect."""
	
	def __get_contrast(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_contrast', __handle)

	def __set_contrast(self, _contrast: float):
		return cur_server.exec('mset.CameraPostEffect.set_contrast', __handle, _contrast)

	contrast: float = property(__get_contrast, __set_contrast)
	"""Contrast multiplier."""
	
	def __get_contrastCenter(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_contrastCenter', __handle)

	def __set_contrastCenter(self, _contrastCenter: float):
		return cur_server.exec('mset.CameraPostEffect.set_contrastCenter', __handle, _contrastCenter)

	contrastCenter: float = property(__get_contrastCenter, __set_contrastCenter)
	"""A value above which color values are brightened, and below which color values are darkened to achive the contrast effect."""
	
	def __get_exposure(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_exposure', __handle)

	def __set_exposure(self, _exposure: float):
		return cur_server.exec('mset.CameraPostEffect.set_exposure', __handle, _exposure)

	exposure: float = property(__get_exposure, __set_exposure)
	"""Exposure multiplier."""
	
	def __get_grainSharpness(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_grainSharpness', __handle)

	def __set_grainSharpness(self, _grainSharpness: float):
		return cur_server.exec('mset.CameraPostEffect.set_grainSharpness', __handle, _grainSharpness)

	grainSharpness: float = property(__get_grainSharpness, __set_grainSharpness)
	"""Sharpness scalar for the film grain effect."""
	
	def __get_grainStrength(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_grainStrength', __handle)

	def __set_grainStrength(self, _grainStrength: float):
		return cur_server.exec('mset.CameraPostEffect.set_grainStrength', __handle, _grainStrength)

	grainStrength: float = property(__get_grainStrength, __set_grainStrength)
	"""Strength multiplier for the film grain effect."""
	
	def __get_saturation(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_saturation', __handle)

	def __set_saturation(self, _saturation: float):
		return cur_server.exec('mset.CameraPostEffect.set_saturation', __handle, _saturation)

	saturation: float = property(__get_saturation, __set_saturation)
	"""Adjusts the intensity of color saturation (default is 1.0)."""
	
	def __get_sharpen(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_sharpen', __handle)

	def __set_sharpen(self, _sharpen: float):
		return cur_server.exec('mset.CameraPostEffect.set_sharpen', __handle, _sharpen)

	sharpen: float = property(__get_sharpen, __set_sharpen)
	"""Strength of the edge sharpening effect."""
	
	def __get_sharpenLimit(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_sharpenLimit', __handle)

	def __set_sharpenLimit(self, _sharpenLimit: float):
		return cur_server.exec('mset.CameraPostEffect.set_sharpenLimit', __handle, _sharpenLimit)

	sharpenLimit: float = property(__get_sharpenLimit, __set_sharpenLimit)
	"""A numerical limit on the stength of the edge sharpening effect."""
	
	def __get_toneMappingMode(self) -> str:
		return cur_server.exec('mset.CameraPostEffect.get_toneMappingMode', __handle)

	def __set_toneMappingMode(self, _toneMappingMode: str):
		return cur_server.exec('mset.CameraPostEffect.set_toneMappingMode', __handle, _toneMappingMode)

	toneMappingMode: str = property(__get_toneMappingMode, __set_toneMappingMode)
	"""Tone mapping mode (allowed values are: 'Linear', 'Reinhard', 'Filmic')"""
	
	def __get_vignetteSoftness(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_vignetteSoftness', __handle)

	def __set_vignetteSoftness(self, _vignetteSoftness: float):
		return cur_server.exec('mset.CameraPostEffect.set_vignetteSoftness', __handle, _vignetteSoftness)

	vignetteSoftness: float = property(__get_vignetteSoftness, __set_vignetteSoftness)
	"""Softness scalar for the vignette effect."""
	
	def __get_vignetteStrength(self) -> float:
		return cur_server.exec('mset.CameraPostEffect.get_vignetteStrength', __handle)

	def __set_vignetteStrength(self, _vignetteStrength: float):
		return cur_server.exec('mset.CameraPostEffect.set_vignetteStrength', __handle, _vignetteStrength)

	vignetteStrength: float = property(__get_vignetteStrength, __set_vignetteStrength)
	"""Strength multiplier for the vignette effect."""
	

class GradientData:
	"""
	Gradient Data, used with Texture Project layers to control various effects.
	"""
	
	__handle = None
	def addColor(self, color: List[float], position: float, weight: float):
		"""
		Adds a color to this gradient.
		"""
		return cur_server.exec('mset.GradientData.addColor', __handle, color,position,weight)

	def getColor(self, index: int) -> Tuple[List[float], float]:
		"""
		Gets a color of this gradient.
		"""
		return cur_server.exec('mset.GradientData.getColor', __handle, index)

	def getColorCount(self) -> int:
		"""
		Gets the number of colors this gradient has.
		"""
		return cur_server.exec('mset.GradientData.getColorCount', __handle)

	def reset(self):
		"""
		Resets this gradient to a default configuration (black to white).
		"""
		return cur_server.exec('mset.GradientData.reset', __handle)

	def setColor(self, index: int, color: List[float], weight: float):
		"""
		Sets a given color of this gradient.
		"""
		return cur_server.exec('mset.GradientData.setColor', __handle, index,color,weight)


class Image:
	"""
	A CPU-side image. Used for image loading and saving, and pixel manipulations. See mset.Texture for material and rendering uses.
	"""
	
	__handle = None
	def compressBCn(self, mode: int):
		"""
		Encodes the image in a GPU-friendly block-compressed format. Currently supported modes are 4, 5, 6, and 7. Source images must be in an 8bit-per-channel color mode (such as BGRA8 or R8), except for mode 6, which requires a floating point color format.BC4 (mode=4) encodes grayscale in 4 bits per pixel.BC5 (mode=5) encodes two color channels in 8 bits per pixel. This is often useful for normal maps.BC6H(mode=6) encodes HDR RGB color in 8 bits per pixel. This is useful for high dynamic range images, such as backgrounds or panoramas.BC7 (mode=7) encodes RGB color and an alpha channel in 8 bits per pixel.
		"""
		return cur_server.exec('mset.Image.compressBCn', __handle, mode)

	def convertPixelFormat(self, format: int):
		"""
		Converts the image to the specified format. Some formats of interest:BGRA8: 0RGBA16: 1RGBA_FLOAT16: 2RGBA_FLOAT32: 3RGB10_A2: 5R8: 13R16: 14RG8: 15RG16: 16R_FLOAT16: 17RG_FLOAT16: 18R_FLOAT32: 19RG_FLOAT32: 20R11G11B10_FLOAT: 21
		"""
		return cur_server.exec('mset.Image.convertPixelFormat', __handle, format)

	def createTexture(self, sRGB: bool = True):
		"""
		Creates a mset.Texture object from the image contents, ready for GPU use.
		"""
		return cur_server.exec('mset.Image.createTexture', __handle, sRGB=True)

	def flipVertical(self):
		"""
		Vertically flips an image. Some pixel formats, such as BC7, may not be flippable.
		"""
		return cur_server.exec('mset.Image.flipVertical', __handle)

	def generateMipmaps(self, sRGB: bool = False):
		"""
		Generates mipmaps for the image. Can optionally account for sRGB color space.
		"""
		return cur_server.exec('mset.Image.generateMipmaps', __handle, sRGB=False)

	def getPixelFormat(self) -> str:
		"""
		Returns the current pixel format, or -1 if the image is invalid. See convertPixelFormat() for a list of format values.
		"""
		return cur_server.exec('mset.Image.getPixelFormat', __handle)

	def writeOut(self, path: str):
		"""
		Writes the image contents to a file on disk. The file format is determined by the file extension.
		"""
		return cur_server.exec('mset.Image.writeOut', __handle, path)


class LevelData:
	"""
	Level Data, used with Texture Project layers to control various effects.
	"""
	
	__handle = None
	def getHandle(self, color: str) -> List[float]:
		"""
		Gets the settings for this level.
		"""
		return cur_server.exec('mset.LevelData.getHandle', __handle, color)

	def reset(self):
		"""
		Resets this level to a default configuration.
		"""
		return cur_server.exec('mset.LevelData.reset', __handle)

	def setLevel(self, color: str, black: float, gamma: float, white: float, outputBlack: float, outputWhite: float):
		"""
		Configures this level.
		"""
		return cur_server.exec('mset.LevelData.setLevel', __handle, color,black,gamma,white,outputBlack,outputWhite)


class Library:
	"""
	The Marmoset Library. Provides access to a library of thousands of materials, textures, smart materials, skies, and much more. Customize your library to suit your needs.
	"""
	
	__handle = None
	def addAsset(self, desc: Dict):
		"""
		Add an asset to your current library distribution. You must supply a dictionary with the following keys: { name: str, author: str, link: str, tags: str, type: str, path: str, filename: str }
		"""
		return cur_server.exec('mset.Library.addAsset', __handle, desc)

	def removeAsset(self, name: str):
		"""
		Remove an asset from your current library distribution.
		"""
		return cur_server.exec('mset.Library.removeAsset', __handle, name)


class Material:
	"""
	Material
	"""
	
	__handle = None
	def __get_albedo(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_albedo', __handle)

	def __set_albedo(self, _albedo: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_albedo', __handle, _albedo)

	albedo: MaterialSubroutine = property(__get_albedo, __set_albedo)
	"""The MaterialSubroutine currently assigned to the Albedo Slot"""
	
	def __get_clearCoatMicrosurface(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_clearCoatMicrosurface', __handle)

	def __set_clearCoatMicrosurface(self, _clearCoatMicrosurface: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_clearCoatMicrosurface', __handle, _clearCoatMicrosurface)

	clearCoatMicrosurface: MaterialSubroutine = property(__get_clearCoatMicrosurface, __set_clearCoatMicrosurface)
	"""The MaterialSubroutine currently assigned to the Clear Coat Microsurface Slot"""
	
	def __get_clearCoatReflection(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_clearCoatReflection', __handle)

	def __set_clearCoatReflection(self, _clearCoatReflection: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_clearCoatReflection', __handle, _clearCoatReflection)

	clearCoatReflection: MaterialSubroutine = property(__get_clearCoatReflection, __set_clearCoatReflection)
	"""The MaterialSubroutine currently assigned to the Clear Coat Reflection Slot"""
	
	def __get_clearcoatReflectivity(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_clearcoatReflectivity', __handle)

	def __set_clearcoatReflectivity(self, _clearcoatReflectivity: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_clearcoatReflectivity', __handle, _clearcoatReflectivity)

	clearcoatReflectivity: MaterialSubroutine = property(__get_clearcoatReflectivity, __set_clearcoatReflectivity)
	"""The MaterialSubroutine currently assigned to the Clear Coat Reflectivity Slot"""
	
	def __get_diffusion(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_diffusion', __handle)

	def __set_diffusion(self, _diffusion: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_diffusion', __handle, _diffusion)

	diffusion: MaterialSubroutine = property(__get_diffusion, __set_diffusion)
	"""The MaterialSubroutine currently assigned to the Diffusion Slot"""
	
	def __get_displacement(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_displacement', __handle)

	def __set_displacement(self, _displacement: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_displacement', __handle, _displacement)

	displacement: MaterialSubroutine = property(__get_displacement, __set_displacement)
	"""The MaterialSubroutine currently assigned to the Displacement Slot"""
	
	def __get_emission(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_emission', __handle)

	def __set_emission(self, _emission: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_emission', __handle, _emission)

	emission: MaterialSubroutine = property(__get_emission, __set_emission)
	"""The MaterialSubroutine currently assigned to the Emission Slot"""
	
	def __get_extra(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_extra', __handle)

	def __set_extra(self, _extra: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_extra', __handle, _extra)

	extra: MaterialSubroutine = property(__get_extra, __set_extra)
	"""The MaterialSubroutine currently assigned to the Extra Slot"""
	
	def __get_microsurface(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_microsurface', __handle)

	def __set_microsurface(self, _microsurface: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_microsurface', __handle, _microsurface)

	microsurface: MaterialSubroutine = property(__get_microsurface, __set_microsurface)
	"""The MaterialSubroutine currently assigned to the Microsurface Slot"""
	
	def __get_name(self) -> Material:
		return cur_server.exec('mset.Material.get_name', __handle)

	def __set_name(self, _name: Material):
		return cur_server.exec('mset.Material.set_name', __handle, _name)

	name: Material = property(__get_name, __set_name)
	"""The name of the Material. Please note that Materials must have unique names in Toolbag scenes."""
	
	def __get_occlusion(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_occlusion', __handle)

	def __set_occlusion(self, _occlusion: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_occlusion', __handle, _occlusion)

	occlusion: MaterialSubroutine = property(__get_occlusion, __set_occlusion)
	"""The MaterialSubroutine currently assigned to the Occlusion Slot"""
	
	def __get_reflection(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_reflection', __handle)

	def __set_reflection(self, _reflection: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_reflection', __handle, _reflection)

	reflection: MaterialSubroutine = property(__get_reflection, __set_reflection)
	"""The MaterialSubroutine currently assigned to the Reflection Slot"""
	
	def __get_reflectivity(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_reflectivity', __handle)

	def __set_reflectivity(self, _reflectivity: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_reflectivity', __handle, _reflectivity)

	reflectivity: MaterialSubroutine = property(__get_reflectivity, __set_reflectivity)
	"""The MaterialSubroutine currently assigned to the Reflectivity Slot"""
	
	def __get_surface(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_surface', __handle)

	def __set_surface(self, _surface: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_surface', __handle, _surface)

	surface: MaterialSubroutine = property(__get_surface, __set_surface)
	"""The MaterialSubroutine currently assigned to the Surface Slot"""
	
	def __get_texture(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_texture', __handle)

	def __set_texture(self, _texture: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_texture', __handle, _texture)

	texture: MaterialSubroutine = property(__get_texture, __set_texture)
	"""The MaterialSubroutine used for texture parameters"""
	
	def __get_transmission(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_transmission', __handle)

	def __set_transmission(self, _transmission: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_transmission', __handle, _transmission)

	transmission: MaterialSubroutine = property(__get_transmission, __set_transmission)
	"""The MaterialSubroutine currently assigned to the Transmission Slot"""
	
	def __get_transparency(self) -> MaterialSubroutine:
		return cur_server.exec('mset.Material.get_transparency', __handle)

	def __set_transparency(self, _transparency: MaterialSubroutine):
		return cur_server.exec('mset.Material.set_transparency', __handle, _transparency)

	transparency: MaterialSubroutine = property(__get_transparency, __set_transparency)
	"""The MaterialSubroutine currently assigned to the Transparency Slot"""
	
	def assign(self, object: SceneObject, includeChildren: bool = True):
		"""
		Assigns the material to a scene object. If 'includeChildren' is true, this material will also be applied to the children of the object.
		"""
		return cur_server.exec('mset.Material.assign', __handle, object,includeChildren)

	def destroy(self):
		"""
		Destroys the Material and removes it from the scene.
		"""
		return cur_server.exec('mset.Material.destroy', __handle)

	def duplicate(self, name: str = '') -> Material:
		"""
		Duplicates the Material, optionally assigning it a name. If no name is specified, one will be automatically generated.Returns the new material.
		"""
		return cur_server.exec('mset.Material.duplicate', __handle, name='')

	def exportFile(self, path: str):
		"""
		Exports this material to the path specified.
		"""
		return cur_server.exec('mset.Material.exportFile', __handle, path)

	def getAssignedObjects(self) -> List[SceneObject]:
		"""
		Returns a list of all scene objects to which this material is assigned.
		"""
		return cur_server.exec('mset.Material.getAssignedObjects', __handle)

	def getCustomShader(self) -> str:
		"""
		Returns the name of the custom shader file, or an empty string if there is none.
		"""
		return cur_server.exec('mset.Material.getCustomShader', __handle)

	def getGroup(self) -> str:
		"""
		Returns the string name of the group the material is assigned to or an empty string, if the material is in no group.
		"""
		return cur_server.exec('mset.Material.getGroup', __handle)

	def getSubroutine(self, subroutine: str) -> MaterialSubroutine:
		"""
		Returns the subroutine in a given slot, specified by string name in the UI. See also setSubroutine().
		"""
		return cur_server.exec('mset.Material.getSubroutine', __handle, subroutine)

	def renderPreview(self, width: int, height: int):
		"""
		Renders the material, applied to a sample mesh, to a preview image. Returns an mset.Image instance.
		"""
		return cur_server.exec('mset.Material.renderPreview', __handle, width,height)

	def setCustomShader(self, shaderFile: str):
		"""
		Assigns a custom shader to the material. The supplied file name must refer to a .frag or .vert file in data/shader/mat/custom. Passing an empty string will unset any custom shader present.
		"""
		return cur_server.exec('mset.Material.setCustomShader', __handle, shaderFile)

	def setGroup(self, name: str):
		"""
		Assigns the material to a new or existing group. Use '' to assign the material to no group.
		"""
		return cur_server.exec('mset.Material.setGroup', __handle, name)

	def setKeyframe(self, lerp: str):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		return cur_server.exec('mset.Material.setKeyframe', __handle, lerp)

	def setSubroutine(self, subroutine: str, shader: str):
		"""
		Assigns a shader type to a given subroutine. Both parameters are string names. 'shader' must be a valid shader name, and 'subroutine' must be one of: 'subdivision', 'displacement', 'surface', 'microsurface', 'albedo', 'diffusion', 'reflectivity', 'reflection', 'clearcoat reflection', 'clearcoat microsurface', 'clearcoat reflectivity', 'occlusion', 'emissive', 'transparency', 'extra', 'texture'.
		"""
		return cur_server.exec('mset.Material.setSubroutine', __handle, subroutine,shader)


class MaterialSubroutine:
	"""
	Material Subroutine
	"""
	
	__handle = None
	def getField(self, name: str) -> Union[NoneType, int, float, str, Texture]:
		"""
		Returns the value of a field.
		"""
		return cur_server.exec('mset.MaterialSubroutine.getField', __handle, name)

	def getFieldNames(self) -> List[str]:
		"""
		Returns a list of all field names of the subroutine.
		"""
		return cur_server.exec('mset.MaterialSubroutine.getFieldNames', __handle)

	def setField(self, name: str, value: Union[int, float, str, Texture]):
		"""
		Sets the value of a field. Texture fields may be set by either passing a string path or an mset.Texture instance.
		"""
		return cur_server.exec('mset.MaterialSubroutine.setField', __handle, name,value)


class MaterialSurfaceMap:
	"""
	A Material Surface Map, with customizable parameters.
	"""
	
	__handle = None
	def __get_color(self) -> List[int]:
		return cur_server.exec('mset.MaterialSurfaceMap.get_color', __handle)

	def __set_color(self, _color: List[int]):
		return cur_server.exec('mset.MaterialSurfaceMap.set_color', __handle, _color)

	color: List[int] = property(__get_color, __set_color)
	"""The base color of this map."""
	
	def __get_contrast(self) -> float:
		return cur_server.exec('mset.MaterialSurfaceMap.get_contrast', __handle)

	def __set_contrast(self, _contrast: float):
		return cur_server.exec('mset.MaterialSurfaceMap.set_contrast', __handle, _contrast)

	contrast: float = property(__get_contrast, __set_contrast)
	"""The level of contrast for this map."""
	
	def __get_invert(self) -> bool:
		return cur_server.exec('mset.MaterialSurfaceMap.get_invert', __handle)

	def __set_invert(self, _invert: bool):
		return cur_server.exec('mset.MaterialSurfaceMap.set_invert', __handle, _invert)

	invert: bool = property(__get_invert, __set_invert)
	"""Determines if contrast/color have been flipped."""
	
	def __get_mode(self) -> str:
		return cur_server.exec('mset.MaterialSurfaceMap.get_mode', __handle)

	def __set_mode(self, _mode: str):
		return cur_server.exec('mset.MaterialSurfaceMap.set_mode', __handle, _mode)

	mode: str = property(__get_mode, __set_mode)
	"""The mode of this map, can be either 'texture' or 'material'"""
	
	def __get_texture(self) -> Texture:
		return cur_server.exec('mset.MaterialSurfaceMap.get_texture', __handle)

	def __set_texture(self, _texture: Texture):
		return cur_server.exec('mset.MaterialSurfaceMap.set_texture', __handle, _texture)

	texture: Texture = property(__get_texture, __set_texture)
	"""The texture that corresponds to this map, or None if none exists."""
	
	def reset(self):
		"""
		Resets this map with the default base color/contrst.
		"""
		return cur_server.exec('mset.MaterialSurfaceMap.reset', __handle)


class Mesh:
	"""
	Mesh
	"""
	
	__handle = None
	def __get_bitangents(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_bitangents', __handle)

	def __set_bitangents(self, _bitangents: List[float]):
		return cur_server.exec('mset.Mesh.set_bitangents', __handle, _bitangents)

	bitangents: List[float] = property(__get_bitangents, __set_bitangents)
	"""Mesh bitangents, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	
	def __get_colors(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_colors', __handle)

	def __set_colors(self, _colors: List[float]):
		return cur_server.exec('mset.Mesh.set_colors', __handle, _colors)

	colors: List[float] = property(__get_colors, __set_colors)
	"""Mesh colors, as a list of float groups of 4 ( e.g. [r,g,b,a, r,g,b,a] )"""
	
	def __get_normals(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_normals', __handle)

	def __set_normals(self, _normals: List[float]):
		return cur_server.exec('mset.Mesh.set_normals', __handle, _normals)

	normals: List[float] = property(__get_normals, __set_normals)
	"""Mesh normals, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	
	def __get_polygons(self) -> List[int]:
		return cur_server.exec('mset.Mesh.get_polygons', __handle)

	def __set_polygons(self, _polygons: List[int]):
		return cur_server.exec('mset.Mesh.set_polygons', __handle, _polygons)

	polygons: List[int] = property(__get_polygons, __set_polygons)
	"""Mesh polygon groups, as a list of int groups of 2, start and count ( e.g. [0,2, 1,2] )"""
	
	def __get_secondaryUVs(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_secondaryUVs', __handle)

	def __set_secondaryUVs(self, _secondaryUVs: List[float]):
		return cur_server.exec('mset.Mesh.set_secondaryUVs', __handle, _secondaryUVs)

	secondaryUVs: List[float] = property(__get_secondaryUVs, __set_secondaryUVs)
	"""Mesh secondary texture coordinates, as a list of float groups of 2 ( e.g. [u,v, u,v] )"""
	
	def __get_tangents(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_tangents', __handle)

	def __set_tangents(self, _tangents: List[float]):
		return cur_server.exec('mset.Mesh.set_tangents', __handle, _tangents)

	tangents: List[float] = property(__get_tangents, __set_tangents)
	"""Mesh tangents, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	
	def __get_triangles(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_triangles', __handle)

	def __set_triangles(self, _triangles: List[float]):
		return cur_server.exec('mset.Mesh.set_triangles', __handle, _triangles)

	triangles: List[float] = property(__get_triangles, __set_triangles)
	"""Mesh triangle indices, as a list of int groups of 3 ( e.g. [0,1,2, 1,3,2] )"""
	
	def __get_uvs(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_uvs', __handle)

	def __set_uvs(self, _uvs: List[float]):
		return cur_server.exec('mset.Mesh.set_uvs', __handle, _uvs)

	uvs: List[float] = property(__get_uvs, __set_uvs)
	"""Mesh texture coordinates as a list of float groups of 2 ( e.g. [u,v, u,v] )"""
	
	def __get_vertices(self) -> List[float]:
		return cur_server.exec('mset.Mesh.get_vertices', __handle)

	def __set_vertices(self, _vertices: List[float]):
		return cur_server.exec('mset.Mesh.set_vertices', __handle, _vertices)

	vertices: List[float] = property(__get_vertices, __set_vertices)
	"""Mesh vertex positions, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	

class Projector:
	"""
	A Projector object that controls layer projection.
	"""
	
	__handle = None
	def __get_clamp(self) -> bool:
		return cur_server.exec('mset.Projector.get_clamp', __handle)

	def __set_clamp(self, _clamp: bool):
		return cur_server.exec('mset.Projector.set_clamp', __handle, _clamp)

	clamp: bool = property(__get_clamp, __set_clamp)
	"""If clamping is enabled for UVs or not."""
	
	def __get_edgeFade(self) -> float:
		return cur_server.exec('mset.Projector.get_edgeFade', __handle)

	def __set_edgeFade(self, _edgeFade: float):
		return cur_server.exec('mset.Projector.set_edgeFade', __handle, _edgeFade)

	edgeFade: float = property(__get_edgeFade, __set_edgeFade)
	"""The amount of edge fading. Used in triplanar projection to blend edges."""
	
	def __get_normalWeight(self) -> float:
		return cur_server.exec('mset.Projector.get_normalWeight', __handle)

	def __set_normalWeight(self, _normalWeight: float):
		return cur_server.exec('mset.Projector.set_normalWeight', __handle, _normalWeight)

	normalWeight: float = property(__get_normalWeight, __set_normalWeight)
	"""The amount of normal fading. Used in triplanar projection to blend normals."""
	
	def __get_position(self) -> List[float]:
		return cur_server.exec('mset.Projector.get_position', __handle)

	def __set_position(self, _position: List[float]):
		return cur_server.exec('mset.Projector.set_position', __handle, _position)

	position: List[float] = property(__get_position, __set_position)
	"""A list of 3 floats (x, y, z) describing the position of this projector."""
	
	def __get_projectionMethod(self) -> str:
		return cur_server.exec('mset.Projector.get_projectionMethod', __handle)

	def __set_projectionMethod(self, _projectionMethod: str):
		return cur_server.exec('mset.Projector.set_projectionMethod', __handle, _projectionMethod)

	projectionMethod: str = property(__get_projectionMethod, __set_projectionMethod)
	"""The projection method of this projector (uv, triplanar, positional, brush, or planar)."""
	
	def __get_rotation(self) -> List[float]:
		return cur_server.exec('mset.Projector.get_rotation', __handle)

	def __set_rotation(self, _rotation: List[float]):
		return cur_server.exec('mset.Projector.set_rotation', __handle, _rotation)

	rotation: List[float] = property(__get_rotation, __set_rotation)
	"""A list of 3 floats (x, y, z) describing the rotation of this projector."""
	
	def __get_scale(self) -> List[float]:
		return cur_server.exec('mset.Projector.get_scale', __handle)

	def __set_scale(self, _scale: List[float]):
		return cur_server.exec('mset.Projector.set_scale', __handle, _scale)

	scale: List[float] = property(__get_scale, __set_scale)
	"""A list of 3 floats (x, y, z) describing the scale of this projector."""
	
	def __get_tiling(self) -> List[float]:
		return cur_server.exec('mset.Projector.get_tiling', __handle)

	def __set_tiling(self, _tiling: List[float]):
		return cur_server.exec('mset.Projector.set_tiling', __handle, _tiling)

	tiling: List[float] = property(__get_tiling, __set_tiling)
	"""The tiling configuration of this projector."""
	
	def __get_transform(self) -> List[float]:
		return cur_server.exec('mset.Projector.get_transform', __handle)

	def __set_transform(self, _transform: List[float]):
		return cur_server.exec('mset.Projector.set_transform', __handle, _transform)

	transform: List[float] = property(__get_transform, __set_transform)
	"""A list of 16 floats describing the transform matrix of this projector."""
	
	def __get_uvRotation(self) -> float:
		return cur_server.exec('mset.Projector.get_uvRotation', __handle)

	def __set_uvRotation(self, _uvRotation: float):
		return cur_server.exec('mset.Projector.set_uvRotation', __handle, _uvRotation)

	uvRotation: float = property(__get_uvRotation, __set_uvRotation)
	"""Rotation of UVs in the W axis."""
	

class RenderCameraOptions:
	"""
	Options when configuring a camera to render with Toolbag.
	"""
	
	__handle = None
	def __get_camera(self) -> CameraObject:
		return cur_server.exec('mset.RenderCameraOptions.get_camera', __handle)

	def __set_camera(self, _camera: CameraObject):
		return cur_server.exec('mset.RenderCameraOptions.set_camera', __handle, _camera)

	camera: CameraObject = property(__get_camera, __set_camera)
	"""The reference to this camera object."""
	
	def __get_enabled(self) -> bool:
		return cur_server.exec('mset.RenderCameraOptions.get_enabled', __handle)

	def __set_enabled(self, _enabled: bool):
		return cur_server.exec('mset.RenderCameraOptions.set_enabled', __handle, _enabled)

	enabled: bool = property(__get_enabled, __set_enabled)
	"""If this camera is enabled when exporting images/videos."""
	

class RenderOptions:
	"""
	The final scene render configuration.
	"""
	
	__handle = None
	def __get_albedoEnergyConservation(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_albedoEnergyConservation', __handle)

	def __set_albedoEnergyConservation(self, _albedoEnergyConservation: type ):
		return cur_server.exec('mset.RenderOptions.set_albedoEnergyConservation', __handle, _albedoEnergyConservation)

	albedoEnergyConservation: type  = property(__get_albedoEnergyConservation, __set_albedoEnergyConservation)
	"""Albedo is energy converving. Applies to the albedo and specular render passes."""
	
	def __get_depthDither(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_depthDither', __handle)

	def __set_depthDither(self, _depthDither: type ):
		return cur_server.exec('mset.RenderOptions.set_depthDither', __handle, _depthDither)

	depthDither: type  = property(__get_depthDither, __set_depthDither)
	"""Whether dithering is enabled when rendering depth passes."""
	
	def __get_depthNormalization(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_depthNormalization', __handle)

	def __set_depthNormalization(self, _depthNormalization: str):
		return cur_server.exec('mset.RenderOptions.set_depthNormalization', __handle, _depthNormalization)

	depthNormalization: str = property(__get_depthNormalization, __set_depthNormalization)
	"""The normal view to render when using a Depth render pass. Valid values are 'Bounding Sphere', 'Bounding Box', and 'Disabled'."""
	
	def __get_drawWireframe(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_drawWireframe', __handle)

	def __set_drawWireframe(self, _drawWireframe: type ):
		return cur_server.exec('mset.RenderOptions.set_drawWireframe', __handle, _drawWireframe)

	drawWireframe: type  = property(__get_drawWireframe, __set_drawWireframe)
	"""Enables the rendering of mesh wireframes."""
	
	def __get_normalFlipX(self) -> bool:
		return cur_server.exec('mset.RenderOptions.get_normalFlipX', __handle)

	def __set_normalFlipX(self, _normalFlipX: bool):
		return cur_server.exec('mset.RenderOptions.set_normalFlipX', __handle, _normalFlipX)

	normalFlipX: bool = property(__get_normalFlipX, __set_normalFlipX)
	"""Whether to flip normal outputs along the X axis."""
	
	def __get_normalFlipY(self) -> bool:
		return cur_server.exec('mset.RenderOptions.get_normalFlipY', __handle)

	def __set_normalFlipY(self, _normalFlipY: bool):
		return cur_server.exec('mset.RenderOptions.set_normalFlipY', __handle, _normalFlipY)

	normalFlipY: bool = property(__get_normalFlipY, __set_normalFlipY)
	"""Whether to flip normal outputs along the Y axis."""
	
	def __get_normalFlipZ(self) -> bool:
		return cur_server.exec('mset.RenderOptions.get_normalFlipZ', __handle)

	def __set_normalFlipZ(self, _normalFlipZ: bool):
		return cur_server.exec('mset.RenderOptions.set_normalFlipZ', __handle, _normalFlipZ)

	normalFlipZ: bool = property(__get_normalFlipZ, __set_normalFlipZ)
	"""Whether to flip normal outputs along the Z axis."""
	
	def __get_normalSpace(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_normalSpace', __handle)

	def __set_normalSpace(self, _normalSpace: str):
		return cur_server.exec('mset.RenderOptions.set_normalSpace', __handle, _normalSpace)

	normalSpace: str = property(__get_normalSpace, __set_normalSpace)
	"""The normal space to render when using a Normal render pass. Valid values are 'tangent', 'object', and 'view'."""
	
	def __get_occludeAmbient(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_occludeAmbient', __handle)

	def __set_occludeAmbient(self, _occludeAmbient: type ):
		return cur_server.exec('mset.RenderOptions.set_occludeAmbient', __handle, _occludeAmbient)

	occludeAmbient: type  = property(__get_occludeAmbient, __set_occludeAmbient)
	"""Whether screen space ambient occlusion should occlude ambient light in raster rendering."""
	
	def __get_occludeDiffuse(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_occludeDiffuse', __handle)

	def __set_occludeDiffuse(self, _occludeDiffuse: type ):
		return cur_server.exec('mset.RenderOptions.set_occludeDiffuse', __handle, _occludeDiffuse)

	occludeDiffuse: type  = property(__get_occludeDiffuse, __set_occludeDiffuse)
	"""Whether screen space ambient occlusion should occlude diffuse light in raster rendering."""
	
	def __get_occludeSpecular(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_occludeSpecular', __handle)

	def __set_occludeSpecular(self, _occludeSpecular: type ):
		return cur_server.exec('mset.RenderOptions.set_occludeSpecular', __handle, _occludeSpecular)

	occludeSpecular: type  = property(__get_occludeSpecular, __set_occludeSpecular)
	"""Whether screen space ambient occlusion should occlude specular light in raster rendering."""
	
	def __get_occlusionColor(self) -> List[float]:
		return cur_server.exec('mset.RenderOptions.get_occlusionColor', __handle)

	def __set_occlusionColor(self, _occlusionColor: List[float]):
		return cur_server.exec('mset.RenderOptions.set_occlusionColor', __handle, _occlusionColor)

	occlusionColor: List[float] = property(__get_occlusionColor, __set_occlusionColor)
	"""The color of the ambient occlusion."""
	
	def __get_occlusionStrength(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_occlusionStrength', __handle)

	def __set_occlusionStrength(self, _occlusionStrength: type ):
		return cur_server.exec('mset.RenderOptions.set_occlusionStrength', __handle, _occlusionStrength)

	occlusionStrength: type  = property(__get_occlusionStrength, __set_occlusionStrength)
	"""Whether screen space ambient occlusion should occlude ambient light in raster rendering."""
	
	def __get_positionDither(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_positionDither', __handle)

	def __set_positionDither(self, _positionDither: type ):
		return cur_server.exec('mset.RenderOptions.set_positionDither', __handle, _positionDither)

	positionDither: type  = property(__get_positionDither, __set_positionDither)
	"""Whether dithering is enabled when rendering position passes."""
	
	def __get_positionNormalization(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_positionNormalization', __handle)

	def __set_positionNormalization(self, _positionNormalization: str):
		return cur_server.exec('mset.RenderOptions.set_positionNormalization', __handle, _positionNormalization)

	positionNormalization: str = property(__get_positionNormalization, __set_positionNormalization)
	"""The normal view to render when using a Position render pass. Valid values are 'Bounding Sphere', 'Bounding Box', and 'Disabled'."""
	
	def __get_rayTraceBounces(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceBounces', __handle)

	def __set_rayTraceBounces(self, _rayTraceBounces: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceBounces', __handle, _rayTraceBounces)

	rayTraceBounces: type  = property(__get_rayTraceBounces, __set_rayTraceBounces)
	"""The maximum number of bounces a ray can perform."""
	
	def __get_rayTraceCaustics(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceCaustics', __handle)

	def __set_rayTraceCaustics(self, _rayTraceCaustics: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceCaustics', __handle, _rayTraceCaustics)

	rayTraceCaustics: type  = property(__get_rayTraceCaustics, __set_rayTraceCaustics)
	"""Whether caustics light paths are allowed when ray tracing."""
	
	def __get_rayTraceDenoiseFade(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDenoiseFade', __handle)

	def __set_rayTraceDenoiseFade(self, _rayTraceDenoiseFade: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDenoiseFade', __handle, _rayTraceDenoiseFade)

	rayTraceDenoiseFade: type  = property(__get_rayTraceDenoiseFade, __set_rayTraceDenoiseFade)
	"""If enabled, the denoiser fades in after a set number of frames."""
	
	def __get_rayTraceDenoiseMode(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDenoiseMode', __handle)

	def __set_rayTraceDenoiseMode(self, _rayTraceDenoiseMode: str):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDenoiseMode', __handle, _rayTraceDenoiseMode)

	rayTraceDenoiseMode: str = property(__get_rayTraceDenoiseMode, __set_rayTraceDenoiseMode)
	"""The current denoising mode. Can be 'off', 'cpu', or 'gpu'."""
	
	def __get_rayTraceDenoiseQuality(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDenoiseQuality', __handle)

	def __set_rayTraceDenoiseQuality(self, _rayTraceDenoiseQuality: str):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDenoiseQuality', __handle, _rayTraceDenoiseQuality)

	rayTraceDenoiseQuality: str = property(__get_rayTraceDenoiseQuality, __set_rayTraceDenoiseQuality)
	"""The current level of denoising quality. Can be 'low', 'medium', or 'high'."""
	
	def __get_rayTraceDenoiseRealTime(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDenoiseRealTime', __handle)

	def __set_rayTraceDenoiseRealTime(self, _rayTraceDenoiseRealTime: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDenoiseRealTime', __handle, _rayTraceDenoiseRealTime)

	rayTraceDenoiseRealTime: type  = property(__get_rayTraceDenoiseRealTime, __set_rayTraceDenoiseRealTime)
	"""Allows for denoising to occur in real time."""
	
	def __get_rayTraceDenoiseStartFrame(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDenoiseStartFrame', __handle)

	def __set_rayTraceDenoiseStartFrame(self, _rayTraceDenoiseStartFrame: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDenoiseStartFrame', __handle, _rayTraceDenoiseStartFrame)

	rayTraceDenoiseStartFrame: type  = property(__get_rayTraceDenoiseStartFrame, __set_rayTraceDenoiseStartFrame)
	"""The starting frame for denoising to occur."""
	
	def __get_rayTraceDenoiseStrength(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDenoiseStrength', __handle)

	def __set_rayTraceDenoiseStrength(self, _rayTraceDenoiseStrength: str):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDenoiseStrength', __handle, _rayTraceDenoiseStrength)

	rayTraceDenoiseStrength: str = property(__get_rayTraceDenoiseStrength, __set_rayTraceDenoiseStrength)
	"""The current level of denoising quality. Can be 'low', 'medium', or 'high'."""
	
	def __get_rayTraceDiffuseIntensity(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceDiffuseIntensity', __handle)

	def __set_rayTraceDiffuseIntensity(self, _rayTraceDiffuseIntensity: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceDiffuseIntensity', __handle, _rayTraceDiffuseIntensity)

	rayTraceDiffuseIntensity: type  = property(__get_rayTraceDiffuseIntensity, __set_rayTraceDiffuseIntensity)
	"""The base intensity of diffuse interactions. Can be scaled for a more stylistic look."""
	
	def __get_rayTraceRadianceClamp(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceRadianceClamp', __handle)

	def __set_rayTraceRadianceClamp(self, _rayTraceRadianceClamp: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceRadianceClamp', __handle, _rayTraceRadianceClamp)

	rayTraceRadianceClamp: type  = property(__get_rayTraceRadianceClamp, __set_rayTraceRadianceClamp)
	"""The maximum brightness allowed when ray tracing. Useful to reduce fireflies."""
	
	def __get_rayTraceReflectionIntensity(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceReflectionIntensity', __handle)

	def __set_rayTraceReflectionIntensity(self, _rayTraceReflectionIntensity: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceReflectionIntensity', __handle, _rayTraceReflectionIntensity)

	rayTraceReflectionIntensity: type  = property(__get_rayTraceReflectionIntensity, __set_rayTraceReflectionIntensity)
	"""The base intensity of reflection interactions. Can be scaled for a more stylistic look."""
	
	def __get_rayTraceSampleAccumulation(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceSampleAccumulation', __handle)

	def __set_rayTraceSampleAccumulation(self, _rayTraceSampleAccumulation: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceSampleAccumulation', __handle, _rayTraceSampleAccumulation)

	rayTraceSampleAccumulation: type  = property(__get_rayTraceSampleAccumulation, __set_rayTraceSampleAccumulation)
	"""The number of samples total allowed to be traced in the viewport each frame."""
	
	def __get_rayTraceSampleCount(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceSampleCount', __handle)

	def __set_rayTraceSampleCount(self, _rayTraceSampleCount: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceSampleCount', __handle, _rayTraceSampleCount)

	rayTraceSampleCount: type  = property(__get_rayTraceSampleCount, __set_rayTraceSampleCount)
	"""The number of samples allowed to be traced in the viewport each frame."""
	
	def __get_rayTraceTransmissionBounces(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_rayTraceTransmissionBounces', __handle)

	def __set_rayTraceTransmissionBounces(self, _rayTraceTransmissionBounces: type ):
		return cur_server.exec('mset.RenderOptions.set_rayTraceTransmissionBounces', __handle, _rayTraceTransmissionBounces)

	rayTraceTransmissionBounces: type  = property(__get_rayTraceTransmissionBounces, __set_rayTraceTransmissionBounces)
	"""The maximum number of transmission bounces a ray can perform."""
	
	def __get_reflectDiffuse(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_reflectDiffuse', __handle)

	def __set_reflectDiffuse(self, _reflectDiffuse: type ):
		return cur_server.exec('mset.RenderOptions.set_reflectDiffuse', __handle, _reflectDiffuse)

	reflectDiffuse: type  = property(__get_reflectDiffuse, __set_reflectDiffuse)
	"""Whether screen space reflections should be enabled."""
	
	def __get_reflectionDiffuseDistance(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_reflectionDiffuseDistance', __handle)

	def __set_reflectionDiffuseDistance(self, _reflectionDiffuseDistance: type ):
		return cur_server.exec('mset.RenderOptions.set_reflectionDiffuseDistance', __handle, _reflectionDiffuseDistance)

	reflectionDiffuseDistance: type  = property(__get_reflectionDiffuseDistance, __set_reflectionDiffuseDistance)
	"""The distance diffuse reflections should be allowed to propigate."""
	
	def __get_reflectionDiffuseIntensity(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_reflectionDiffuseIntensity', __handle)

	def __set_reflectionDiffuseIntensity(self, _reflectionDiffuseIntensity: type ):
		return cur_server.exec('mset.RenderOptions.set_reflectionDiffuseIntensity', __handle, _reflectionDiffuseIntensity)

	reflectionDiffuseIntensity: type  = property(__get_reflectionDiffuseIntensity, __set_reflectionDiffuseIntensity)
	"""The level of brightness the diffuse reflections have."""
	
	def __get_reflectionIntensity(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_reflectionIntensity', __handle)

	def __set_reflectionIntensity(self, _reflectionIntensity: type ):
		return cur_server.exec('mset.RenderOptions.set_reflectionIntensity', __handle, _reflectionIntensity)

	reflectionIntensity: type  = property(__get_reflectionIntensity, __set_reflectionIntensity)
	"""The level of brightness the reflections have."""
	
	def __get_shadowBias(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_shadowBias', __handle)

	def __set_shadowBias(self, _shadowBias: type ):
		return cur_server.exec('mset.RenderOptions.set_shadowBias', __handle, _shadowBias)

	shadowBias: type  = property(__get_shadowBias, __set_shadowBias)
	"""A bias value for how distance the furthest shadow cascade is from the camera."""
	
	def __get_shadowCascadeDistance(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_shadowCascadeDistance', __handle)

	def __set_shadowCascadeDistance(self, _shadowCascadeDistance: type ):
		return cur_server.exec('mset.RenderOptions.set_shadowCascadeDistance', __handle, _shadowCascadeDistance)

	shadowCascadeDistance: type  = property(__get_shadowCascadeDistance, __set_shadowCascadeDistance)
	"""A bias value for how distance the furthest shadow cascade is from the camera."""
	
	def __get_shadowQuality(self) -> str:
		return cur_server.exec('mset.RenderOptions.get_shadowQuality', __handle)

	def __set_shadowQuality(self, _shadowQuality: str):
		return cur_server.exec('mset.RenderOptions.set_shadowQuality', __handle, _shadowQuality)

	shadowQuality: str = property(__get_shadowQuality, __set_shadowQuality)
	"""Shadow quality. Valid values are 'Low', 'High', and 'Mega'."""
	
	def __get_useRasterOcclusion(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_useRasterOcclusion', __handle)

	def __set_useRasterOcclusion(self, _useRasterOcclusion: type ):
		return cur_server.exec('mset.RenderOptions.set_useRasterOcclusion', __handle, _useRasterOcclusion)

	useRasterOcclusion: type  = property(__get_useRasterOcclusion, __set_useRasterOcclusion)
	"""Whether screen space ambient occlusion is enabled in raster rendering."""
	
	def __get_useRayTracing(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_useRayTracing', __handle)

	def __set_useRayTracing(self, _useRayTracing: type ):
		return cur_server.exec('mset.RenderOptions.set_useRayTracing', __handle, _useRayTracing)

	useRayTracing: type  = property(__get_useRayTracing, __set_useRayTracing)
	"""Whether real time ray tracing is enabled."""
	
	def __get_useReflections(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_useReflections', __handle)

	def __set_useReflections(self, _useReflections: type ):
		return cur_server.exec('mset.RenderOptions.set_useReflections', __handle, _useReflections)

	useReflections: type  = property(__get_useReflections, __set_useReflections)
	"""Whether screen space reflections should be enabled."""
	
	def __get_useShadowCascades(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_useShadowCascades', __handle)

	def __set_useShadowCascades(self, _useShadowCascades: type ):
		return cur_server.exec('mset.RenderOptions.set_useShadowCascades', __handle, _useShadowCascades)

	useShadowCascades: type  = property(__get_useShadowCascades, __set_useShadowCascades)
	"""Use cascaded shadow maps for directional lights. This can provide better resolution distribution over larger scenes."""
	
	def __get_watermarkColored(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_watermarkColored', __handle)

	def __set_watermarkColored(self, _watermarkColored: type ):
		return cur_server.exec('mset.RenderOptions.set_watermarkColored', __handle, _watermarkColored)

	watermarkColored: type  = property(__get_watermarkColored, __set_watermarkColored)
	"""Determines if the Marmoset watermark is set to colored mode."""
	
	def __get_watermarkDark(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_watermarkDark', __handle)

	def __set_watermarkDark(self, _watermarkDark: type ):
		return cur_server.exec('mset.RenderOptions.set_watermarkDark', __handle, _watermarkDark)

	watermarkDark: type  = property(__get_watermarkDark, __set_watermarkDark)
	"""Determines if the Marmoset watermark is set to dark mode."""
	
	def __get_watermarkEnabled(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_watermarkEnabled', __handle)

	def __set_watermarkEnabled(self, _watermarkEnabled: type ):
		return cur_server.exec('mset.RenderOptions.set_watermarkEnabled', __handle, _watermarkEnabled)

	watermarkEnabled: type  = property(__get_watermarkEnabled, __set_watermarkEnabled)
	"""Whether the Marmoset watermark is enabled."""
	
	def __get_watermarkPosition(self) -> List[float]:
		return cur_server.exec('mset.RenderOptions.get_watermarkPosition', __handle)

	def __set_watermarkPosition(self, _watermarkPosition: List[float]):
		return cur_server.exec('mset.RenderOptions.set_watermarkPosition', __handle, _watermarkPosition)

	watermarkPosition: List[float] = property(__get_watermarkPosition, __set_watermarkPosition)
	"""The position of the watermark. [0,0] coresponds to top left, and [1,1] corresponds to bottom right."""
	
	def __get_watermarkSize(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_watermarkSize', __handle)

	def __set_watermarkSize(self, _watermarkSize: type ):
		return cur_server.exec('mset.RenderOptions.set_watermarkSize', __handle, _watermarkSize)

	watermarkSize: type  = property(__get_watermarkSize, __set_watermarkSize)
	"""Size of the watermark relative to the render's minimum side."""
	
	def __get_wireframeColor(self) -> List[float]:
		return cur_server.exec('mset.RenderOptions.get_wireframeColor', __handle)

	def __set_wireframeColor(self, _wireframeColor: List[float]):
		return cur_server.exec('mset.RenderOptions.set_wireframeColor', __handle, _wireframeColor)

	wireframeColor: List[float] = property(__get_wireframeColor, __set_wireframeColor)
	"""Wireframe color as an RGBA array."""
	
	def __get_wireframeCull(self) -> type:
		return cur_server.exec('mset.RenderOptions.get_wireframeCull', __handle)

	def __set_wireframeCull(self, _wireframeCull: type ):
		return cur_server.exec('mset.RenderOptions.set_wireframeCull', __handle, _wireframeCull)

	wireframeCull: type  = property(__get_wireframeCull, __set_wireframeCull)
	"""Cull backfaces when rendering wireframes."""
	

class RenderOutputOptions:
	"""
	Render Output options, the configuration of image or video export.
	"""
	
	__handle = None
	def __get_compressionQuality(self) -> int:
		return cur_server.exec('mset.RenderOutputOptions.get_compressionQuality', __handle)

	def __set_compressionQuality(self, _compressionQuality: int):
		return cur_server.exec('mset.RenderOutputOptions.set_compressionQuality', __handle, _compressionQuality)

	compressionQuality: int = property(__get_compressionQuality, __set_compressionQuality)
	"""The level of compression for compressed video file formats like avi. Can be between 0 and 100. Does not apply to image exports."""
	
	def __get_format(self) -> str:
		return cur_server.exec('mset.RenderOutputOptions.get_format', __handle)

	def __set_format(self, _format: str):
		return cur_server.exec('mset.RenderOutputOptions.set_format', __handle, _format)

	format: str = property(__get_format, __set_format)
	"""The output format for this export. can be 'JPEG', 'PNG', 'TGA', 'PSD', 'PSD (16-bit)', 'EXR (16-bit)', 'EXR (32-bit)', 'DDS (16-bit)', 'DDS (32-bit)', 'PFM (32-bit)', 'MP4 Lossless' on MacOS or 'AVI Lossless' on Windows, 'MPEG4', or 'Auto'."""
	
	def __get_height(self) -> int:
		return cur_server.exec('mset.RenderOutputOptions.get_height', __handle)

	def __set_height(self, _height: int):
		return cur_server.exec('mset.RenderOutputOptions.set_height', __handle, _height)

	height: int = property(__get_height, __set_height)
	"""The height of this output."""
	
	def __get_outputPath(self) -> str:
		return cur_server.exec('mset.RenderOutputOptions.get_outputPath', __handle)

	def __set_outputPath(self, _outputPath: str):
		return cur_server.exec('mset.RenderOutputOptions.set_outputPath', __handle, _outputPath)

	outputPath: str = property(__get_outputPath, __set_outputPath)
	"""This output directory."""
	
	def __get_overwrite(self) -> bool:
		return cur_server.exec('mset.RenderOutputOptions.get_overwrite', __handle)

	def __set_overwrite(self, _overwrite: bool):
		return cur_server.exec('mset.RenderOutputOptions.set_overwrite', __handle, _overwrite)

	overwrite: bool = property(__get_overwrite, __set_overwrite)
	"""Whether this output should overwrite the file by the same name."""
	
	def __get_rayTraceDenoiseMode(self) -> str:
		return cur_server.exec('mset.RenderOutputOptions.get_rayTraceDenoiseMode', __handle)

	def __set_rayTraceDenoiseMode(self, _rayTraceDenoiseMode: str):
		return cur_server.exec('mset.RenderOutputOptions.set_rayTraceDenoiseMode', __handle, _rayTraceDenoiseMode)

	rayTraceDenoiseMode: str = property(__get_rayTraceDenoiseMode, __set_rayTraceDenoiseMode)
	"""The current denoising mode for this output. Can be 'off', 'cpu', or 'gpu'."""
	
	def __get_rayTraceDenoiseQuality(self) -> str:
		return cur_server.exec('mset.RenderOutputOptions.get_rayTraceDenoiseQuality', __handle)

	def __set_rayTraceDenoiseQuality(self, _rayTraceDenoiseQuality: str):
		return cur_server.exec('mset.RenderOutputOptions.set_rayTraceDenoiseQuality', __handle, _rayTraceDenoiseQuality)

	rayTraceDenoiseQuality: str = property(__get_rayTraceDenoiseQuality, __set_rayTraceDenoiseQuality)
	"""The current level of denoising quality for this output. Can be 'low', 'medium', or 'high'."""
	
	def __get_rayTraceDenoiseStrength(self) -> bool:
		return cur_server.exec('mset.RenderOutputOptions.get_rayTraceDenoiseStrength', __handle)

	def __set_rayTraceDenoiseStrength(self, _rayTraceDenoiseStrength: bool):
		return cur_server.exec('mset.RenderOutputOptions.set_rayTraceDenoiseStrength', __handle, _rayTraceDenoiseStrength)

	rayTraceDenoiseStrength: bool = property(__get_rayTraceDenoiseStrength, __set_rayTraceDenoiseStrength)
	"""The level of contribution the denoiser should have on the final output. Can be any float between 0.0 and 1.0."""
	
	def __get_samples(self) -> int:
		return cur_server.exec('mset.RenderOutputOptions.get_samples', __handle)

	def __set_samples(self, _samples: int):
		return cur_server.exec('mset.RenderOutputOptions.set_samples', __handle, _samples)

	samples: int = property(__get_samples, __set_samples)
	"""The number of samples used for this output."""
	
	def __get_transparency(self) -> bool:
		return cur_server.exec('mset.RenderOutputOptions.get_transparency', __handle)

	def __set_transparency(self, _transparency: bool):
		return cur_server.exec('mset.RenderOutputOptions.set_transparency', __handle, _transparency)

	transparency: bool = property(__get_transparency, __set_transparency)
	"""Whether this output should be transparent or not."""
	
	def __get_width(self) -> int:
		return cur_server.exec('mset.RenderOutputOptions.get_width', __handle)

	def __set_width(self, _width: int):
		return cur_server.exec('mset.RenderOutputOptions.set_width', __handle, _width)

	width: int = property(__get_width, __set_width)
	"""The width of this output."""
	

class RenderPassOptions:
	"""
	Options when configuring a render pass to render with Toolbag.
	"""
	
	__handle = None
	def __get_enabled(self) -> bool:
		return cur_server.exec('mset.RenderPassOptions.get_enabled', __handle)

	def __set_enabled(self, _enabled: bool):
		return cur_server.exec('mset.RenderPassOptions.set_enabled', __handle, _enabled)

	enabled: bool = property(__get_enabled, __set_enabled)
	"""If this render pass is enabled when exporting images/videos."""
	
	def __get_renderPass(self) -> str:
		return cur_server.exec('mset.RenderPassOptions.get_renderPass', __handle)

	def __set_renderPass(self, _renderPass: str):
		return cur_server.exec('mset.RenderPassOptions.set_renderPass', __handle, _renderPass)

	renderPass: str = property(__get_renderPass, __set_renderPass)
	"""The render pass to be executed when rendering images/videos."""
	

class Spline:
	"""
	Spline Data, used with Texture Project layers to control various effects.
	"""
	
	__handle = None
	def addHandle(self, x: float, y: float):
		"""
		Add a point to this spline.
		"""
		return cur_server.exec('mset.Spline.addHandle', __handle, x,y)

	def getHandle(self, index: int) -> List[float]:
		"""
		Get the positional data of a given spline index.
		"""
		return cur_server.exec('mset.Spline.getHandle', __handle, index)

	def getHandleCount(self) -> int:
		"""
		Get the number of points on this spline.
		"""
		return cur_server.exec('mset.Spline.getHandleCount', __handle)

	def reset(self):
		"""
		Resets this spline to a default configuration.
		"""
		return cur_server.exec('mset.Spline.reset', __handle)

	def setHandle(self, index: int, x: float, y: float):
		"""
		Edit a point on this spline.
		"""
		return cur_server.exec('mset.Spline.setHandle', __handle, index,x,y)


class Texture:
	"""
	GPU Texture
	"""
	
	__handle = None
	def __get_anisotropicFiltering(self) -> bool:
		return cur_server.exec('mset.Texture.get_anisotropicFiltering', __handle)

	def __set_anisotropicFiltering(self, _anisotropicFiltering: bool):
		return cur_server.exec('mset.Texture.set_anisotropicFiltering', __handle, _anisotropicFiltering)

	anisotropicFiltering: bool = property(__get_anisotropicFiltering, __set_anisotropicFiltering)
	"""Sets the degree of anisotropic filtering applied to this texture."""
	
	def __get_path(self) -> str:
		return cur_server.exec('mset.Texture.get_path', __handle)

	def __set_path(self, _path: str):
		return cur_server.exec('mset.Texture.set_path', __handle, _path)

	path: str = property(__get_path, __set_path)
	"""The file path of the texture. Note: You cannot set the path of a mset.Texture, only get it."""
	
	def __get_sRGB(self) -> bool:
		return cur_server.exec('mset.Texture.get_sRGB', __handle)

	def __set_sRGB(self, _sRGB: bool):
		return cur_server.exec('mset.Texture.set_sRGB', __handle, _sRGB)

	sRGB: bool = property(__get_sRGB, __set_sRGB)
	"""Determines whether the texture is sampled in sRGB color space."""
	
	def __get_useFiltering(self) -> bool:
		return cur_server.exec('mset.Texture.get_useFiltering', __handle)

	def __set_useFiltering(self, _useFiltering: bool):
		return cur_server.exec('mset.Texture.set_useFiltering', __handle, _useFiltering)

	useFiltering: bool = property(__get_useFiltering, __set_useFiltering)
	"""Determines whether the texture is filtered bilinearly (smooth) or by nearest neighbor (pixelated)."""
	
	def __get_useMipmaps(self) -> bool:
		return cur_server.exec('mset.Texture.get_useMipmaps', __handle)

	def __set_useMipmaps(self, _useMipmaps: bool):
		return cur_server.exec('mset.Texture.set_useMipmaps', __handle, _useMipmaps)

	useMipmaps: bool = property(__get_useMipmaps, __set_useMipmaps)
	"""Determines whether mipmaps are used on the texture."""
	
	def __get_wrapping(self) -> str:
		return cur_server.exec('mset.Texture.get_wrapping', __handle)

	def __set_wrapping(self, _wrapping: str):
		return cur_server.exec('mset.Texture.set_wrapping', __handle, _wrapping)

	wrapping: str = property(__get_wrapping, __set_wrapping)
	"""Sets the type of texture wrapping applied to this texture."""
	
	def renderPreview(self, width: int, height: int):
		"""
		Renders a preview of the texture, at the given resolution. Returns an mset.Image instance.
		"""
		return cur_server.exec('mset.Texture.renderPreview', __handle, width,height)


class TextureProjectLayerMaps:
	"""
	Per map settings for layers/brushes.
	"""
	
	__handle = None
	def __get_albedo(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_albedo', __handle)

	def __set_albedo(self, _albedo: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_albedo', __handle, _albedo)

	albedo: Any = property(__get_albedo, __set_albedo)
	"""The Albedo project map of this surface."""
	
	def __get_ambientOcclusion(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_ambientOcclusion', __handle)

	def __set_ambientOcclusion(self, _ambientOcclusion: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_ambientOcclusion', __handle, _ambientOcclusion)

	ambientOcclusion: Any = property(__get_ambientOcclusion, __set_ambientOcclusion)
	"""The Ambient Occlusion project map of this surface."""
	
	def __get_anisoDir(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_anisoDir', __handle)

	def __set_anisoDir(self, _anisoDir: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_anisoDir', __handle, _anisoDir)

	anisoDir: Any = property(__get_anisoDir, __set_anisoDir)
	"""The Anisotropic Direction project map of this surface."""
	
	def __get_bump(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_bump', __handle)

	def __set_bump(self, _bump: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_bump', __handle, _bump)

	bump: Any = property(__get_bump, __set_bump)
	"""The Bump project map of this surface."""
	
	def __get_cavity(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_cavity', __handle)

	def __set_cavity(self, _cavity: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_cavity', __handle, _cavity)

	cavity: Any = property(__get_cavity, __set_cavity)
	"""The Cavity project map of this surface."""
	
	def __get_displacement(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_displacement', __handle)

	def __set_displacement(self, _displacement: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_displacement', __handle, _displacement)

	displacement: Any = property(__get_displacement, __set_displacement)
	"""The Gloss project map of this surface."""
	
	def __get_emissive(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_emissive', __handle)

	def __set_emissive(self, _emissive: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_emissive', __handle, _emissive)

	emissive: Any = property(__get_emissive, __set_emissive)
	"""The Emissive project map of this surface."""
	
	def __get_fuzz(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_fuzz', __handle)

	def __set_fuzz(self, _fuzz: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_fuzz', __handle, _fuzz)

	fuzz: Any = property(__get_fuzz, __set_fuzz)
	"""The Fuzz project map of this surface."""
	
	def __get_gloss(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_gloss', __handle)

	def __set_gloss(self, _gloss: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_gloss', __handle, _gloss)

	gloss: Any = property(__get_gloss, __set_gloss)
	"""The Gloss project map of this surface."""
	
	def __get_mask(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_mask', __handle)

	def __set_mask(self, _mask: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_mask', __handle, _mask)

	mask: Any = property(__get_mask, __set_mask)
	"""The Mask project map of this surface."""
	
	def __get_metalness(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_metalness', __handle)

	def __set_metalness(self, _metalness: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_metalness', __handle, _metalness)

	metalness: Any = property(__get_metalness, __set_metalness)
	"""The Metalness project map of this surface."""
	
	def __get_normal(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_normal', __handle)

	def __set_normal(self, _normal: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_normal', __handle, _normal)

	normal: Any = property(__get_normal, __set_normal)
	"""The Normal project map of this surface."""
	
	def __get_roughness(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_roughness', __handle)

	def __set_roughness(self, _roughness: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_roughness', __handle, _roughness)

	roughness: Any = property(__get_roughness, __set_roughness)
	"""The Roughness project map of this surface."""
	
	def __get_scatter(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_scatter', __handle)

	def __set_scatter(self, _scatter: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_scatter', __handle, _scatter)

	scatter: Any = property(__get_scatter, __set_scatter)
	"""The Scatter project map of this surface."""
	
	def __get_sheen(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_sheen', __handle)

	def __set_sheen(self, _sheen: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_sheen', __handle, _sheen)

	sheen: Any = property(__get_sheen, __set_sheen)
	"""The Sheen project map of this surface."""
	
	def __get_sheenRoughness(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_sheenRoughness', __handle)

	def __set_sheenRoughness(self, _sheenRoughness: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_sheenRoughness', __handle, _sheenRoughness)

	sheenRoughness: Any = property(__get_sheenRoughness, __set_sheenRoughness)
	"""The Sheen (Roughness) project map of this surface."""
	
	def __get_specular(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_specular', __handle)

	def __set_specular(self, _specular: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_specular', __handle, _specular)

	specular: Any = property(__get_specular, __set_specular)
	"""The Specular project map of this surface."""
	
	def __get_transmissionMask(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_transmissionMask', __handle)

	def __set_transmissionMask(self, _transmissionMask: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_transmissionMask', __handle, _transmissionMask)

	transmissionMask: Any = property(__get_transmissionMask, __set_transmissionMask)
	"""The Transmission Mask project map of this surface."""
	
	def __get_transparency(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerMaps.get_transparency', __handle)

	def __set_transparency(self, _transparency: Any):
		return cur_server.exec('mset.TextureProjectLayerMaps.set_transparency', __handle, _transparency)

	transparency: Any = property(__get_transparency, __set_transparency)
	"""The Transparency project map of this surface."""
	

class TextureProjectOutputMap:
	"""
	A Texture Project Output Map
	"""
	
	__handle = None
	def __get_a(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_a', __handle)

	def __set_a(self, _a: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_a', __handle, _a)

	a: str = property(__get_a, __set_a)
	"""The project map type for the A output channel."""
	
	def __get_b(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_b', __handle)

	def __set_b(self, _b: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_b', __handle, _b)

	b: str = property(__get_b, __set_b)
	"""The project map type for the B output channel."""
	
	def __get_bitrate(self) -> int:
		return cur_server.exec('mset.TextureProjectOutputMap.get_bitrate', __handle)

	def __set_bitrate(self, _bitrate: int):
		return cur_server.exec('mset.TextureProjectOutputMap.set_bitrate', __handle, _bitrate)

	bitrate: int = property(__get_bitrate, __set_bitrate)
	"""The bitrate for this output map. Can be 8 or 16."""
	
	def __get_format(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_format', __handle)

	def __set_format(self, _format: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_format', __handle, _format)

	format: str = property(__get_format, __set_format)
	"""The type of output map, RGB+A or R+G+B+A."""
	
	def __get_g(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_g', __handle)

	def __set_g(self, _g: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_g', __handle, _g)

	g: str = property(__get_g, __set_g)
	"""The project map type for the G output channel."""
	
	def __get_r(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_r', __handle)

	def __set_r(self, _r: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_r', __handle, _r)

	r: str = property(__get_r, __set_r)
	"""The project map type for the R output channel."""
	
	def __get_rgb(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_rgb', __handle)

	def __set_rgb(self, _rgb: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_rgb', __handle, _rgb)

	rgb: str = property(__get_rgb, __set_rgb)
	"""The project map type for the RGB output channels."""
	
	def __get_sRGB(self) -> bool:
		return cur_server.exec('mset.TextureProjectOutputMap.get_sRGB', __handle)

	def __set_sRGB(self, _sRGB: bool):
		return cur_server.exec('mset.TextureProjectOutputMap.set_sRGB', __handle, _sRGB)

	sRGB: bool = property(__get_sRGB, __set_sRGB)
	"""Whether this map is exported with sRGB encoding."""
	
	def __get_suffix(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_suffix', __handle)

	def __set_suffix(self, _suffix: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_suffix', __handle, _suffix)

	suffix: str = property(__get_suffix, __set_suffix)
	"""The suffix appended to the output name of this map."""
	
	def __get_type(self) -> str:
		return cur_server.exec('mset.TextureProjectOutputMap.get_type', __handle)

	def __set_type(self, _type: str):
		return cur_server.exec('mset.TextureProjectOutputMap.set_type', __handle, _type)

	type: str = property(__get_type, __set_type)
	"""The extension type for this output map."""
	

class Timeline:
	"""
	Animation Timeline
	"""
	
	__handle = None
	def __get_currentFrame(self) -> int:
		return cur_server.exec('mset.Timeline.get_currentFrame', __handle)

	def __set_currentFrame(self, _currentFrame: int):
		return cur_server.exec('mset.Timeline.set_currentFrame', __handle, _currentFrame)

	currentFrame: int = property(__get_currentFrame, __set_currentFrame)
	"""Current animation frame. This value must be within the valid range of 0 to totalFrames."""
	
	def __get_playbackSpeed(self) -> float:
		return cur_server.exec('mset.Timeline.get_playbackSpeed', __handle)

	def __set_playbackSpeed(self, _playbackSpeed: float):
		return cur_server.exec('mset.Timeline.set_playbackSpeed', __handle, _playbackSpeed)

	playbackSpeed: float = property(__get_playbackSpeed, __set_playbackSpeed)
	"""The current playback speed. This value controls the apparent speed of playback in the viewport, but does not affect exported animation length."""
	
	def __get_selectionEnd(self) -> int:
		return cur_server.exec('mset.Timeline.get_selectionEnd', __handle)

	def __set_selectionEnd(self, _selectionEnd: int):
		return cur_server.exec('mset.Timeline.set_selectionEnd', __handle, _selectionEnd)

	selectionEnd: int = property(__get_selectionEnd, __set_selectionEnd)
	"""The last frame of the selected time range. Must be less than totalFrames and greater than zero."""
	
	def __get_selectionStart(self) -> int:
		return cur_server.exec('mset.Timeline.get_selectionStart', __handle)

	def __set_selectionStart(self, _selectionStart: int):
		return cur_server.exec('mset.Timeline.set_selectionStart', __handle, _selectionStart)

	selectionStart: int = property(__get_selectionStart, __set_selectionStart)
	"""The first frame of the selected time range. Must be less than totalFrames and greater than zero."""
	
	def __get_totalFrames(self) -> int:
		return cur_server.exec('mset.Timeline.get_totalFrames', __handle)

	def __set_totalFrames(self, _totalFrames: int):
		return cur_server.exec('mset.Timeline.set_totalFrames', __handle, _totalFrames)

	totalFrames: int = property(__get_totalFrames, __set_totalFrames)
	"""Total frame count for the animation. This value must be greater than zero."""
	
	def getFrameRate(self) -> int:
		"""
		Returns the scene's animation frame rate, in frames per second.
		"""
		return cur_server.exec('mset.Timeline.getFrameRate', __handle)

	def getTime(self) -> float:
		"""
		Returns the current animation time, in seconds.
		"""
		return cur_server.exec('mset.Timeline.getTime', __handle)

	def pause(self):
		"""
		Stops animation playback.
		"""
		return cur_server.exec('mset.Timeline.pause', __handle)

	def play(self):
		"""
		Activates animation playback.
		"""
		return cur_server.exec('mset.Timeline.play', __handle)

	def resample(self, frameRate: int):
		"""
		Alters the animation timeline's frame rate, in frames per second. This will resample existing keyframes to fit the new frame rate, and alter the appropriate frame counts.
		"""
		return cur_server.exec('mset.Timeline.resample', __handle, frameRate)

	def setTime(self, time: float):
		"""
		Sets the current animation time, in seconds. This time may be rounded to the nearest frame.
		"""
		return cur_server.exec('mset.Timeline.setTime', __handle, time)


class AOBakerMap(BakerMap):
	"""
	Bent Normal Baker Map Settings
	"""
	
	__handle = None
	def __get_cosineWeight(self) -> float:
		return cur_server.exec('mset.AOBakerMap.get_cosineWeight', __handle)

	def __set_cosineWeight(self, _cosineWeight: float):
		return cur_server.exec('mset.AOBakerMap.set_cosineWeight', __handle, _cosineWeight)

	cosineWeight: float = property(__get_cosineWeight, __set_cosineWeight)
	"""Weights from -1 to 1, increasing values result in more 'cavity' shadows."""
	
	def __get_dither(self) -> bool:
		return cur_server.exec('mset.AOBakerMap.get_dither', __handle)

	def __set_dither(self, _dither: bool):
		return cur_server.exec('mset.AOBakerMap.set_dither', __handle, _dither)

	dither: bool = property(__get_dither, __set_dither)
	"""Determines whether this map output will be dithered."""
	
	def __get_floor(self) -> float:
		return cur_server.exec('mset.AOBakerMap.get_floor', __handle)

	def __set_floor(self, _floor: float):
		return cur_server.exec('mset.AOBakerMap.set_floor', __handle, _floor)

	floor: float = property(__get_floor, __set_floor)
	"""The amount of floor occlusion."""
	
	def __get_floorOcclusion(self) -> float:
		return cur_server.exec('mset.AOBakerMap.get_floorOcclusion', __handle)

	def __set_floorOcclusion(self, _floorOcclusion: float):
		return cur_server.exec('mset.AOBakerMap.set_floorOcclusion', __handle, _floorOcclusion)

	floorOcclusion: float = property(__get_floorOcclusion, __set_floorOcclusion)
	"""Determines whether an artificial floor plane will be used for ambient occlusion baking."""
	
	def __get_ignoreGroups(self) -> bool:
		return cur_server.exec('mset.AOBakerMap.get_ignoreGroups', __handle)

	def __set_ignoreGroups(self, _ignoreGroups: bool):
		return cur_server.exec('mset.AOBakerMap.set_ignoreGroups', __handle, _ignoreGroups)

	ignoreGroups: bool = property(__get_ignoreGroups, __set_ignoreGroups)
	"""Determines whether bake groups will be ignored when baking ambient occlusion."""
	
	def __get_rayCount(self) -> int:
		return cur_server.exec('mset.AOBakerMap.get_rayCount', __handle)

	def __set_rayCount(self, _rayCount: int):
		return cur_server.exec('mset.AOBakerMap.set_rayCount', __handle, _rayCount)

	rayCount: int = property(__get_rayCount, __set_rayCount)
	"""The number of rays used for AO baking."""
	
	def __get_searchDistance(self) -> float:
		return cur_server.exec('mset.AOBakerMap.get_searchDistance', __handle)

	def __set_searchDistance(self, _searchDistance: float):
		return cur_server.exec('mset.AOBakerMap.set_searchDistance', __handle, _searchDistance)

	searchDistance: float = property(__get_searchDistance, __set_searchDistance)
	"""The maximum distance rays can go. 0 defaults to infinity."""
	
	def __get_twoSided(self) -> bool:
		return cur_server.exec('mset.AOBakerMap.get_twoSided', __handle)

	def __set_twoSided(self, _twoSided: bool):
		return cur_server.exec('mset.AOBakerMap.set_twoSided', __handle, _twoSided)

	twoSided: bool = property(__get_twoSided, __set_twoSided)
	"""Determines whether the ambient occlusion baking will also use back faces."""
	

class BackdropObject(SceneObject):
	"""
	Backdrop Object
	"""
	
	__handle = None
	def __get_alpha(self) -> float:
		return cur_server.exec('mset.BackdropObject.get_alpha', __handle)

	def __set_alpha(self, _alpha: float):
		return cur_server.exec('mset.BackdropObject.set_alpha', __handle, _alpha)

	alpha: float = property(__get_alpha, __set_alpha)
	"""The transparency of the backdrop image."""
	
	def __get_path(self) -> str:
		return cur_server.exec('mset.BackdropObject.get_path', __handle)

	def __set_path(self, _path: str):
		return cur_server.exec('mset.BackdropObject.set_path', __handle, _path)

	path: str = property(__get_path, __set_path)
	"""The file path to the backdrop image."""
	
	def __get_useAlpha(self) -> bool:
		return cur_server.exec('mset.BackdropObject.get_useAlpha', __handle)

	def __set_useAlpha(self, _useAlpha: bool):
		return cur_server.exec('mset.BackdropObject.set_useAlpha', __handle, _useAlpha)

	useAlpha: bool = property(__get_useAlpha, __set_useAlpha)
	"""Specifies whether or not to use the image's alpha channel."""
	

class BakerObject(SceneObject):
	"""
	Baker Object
	"""
	
	__handle = None
	def __get_edgePadding(self) -> str:
		return cur_server.exec('mset.BakerObject.get_edgePadding', __handle)

	def __set_edgePadding(self, _edgePadding: str):
		return cur_server.exec('mset.BakerObject.set_edgePadding', __handle, _edgePadding)

	edgePadding: str = property(__get_edgePadding, __set_edgePadding)
	"""Edge padding amount. Must be one of the following values: 'None', 'Moderate', 'Extreme'."""
	
	def __get_edgePaddingSize(self) -> float:
		return cur_server.exec('mset.BakerObject.get_edgePaddingSize', __handle)

	def __set_edgePaddingSize(self, _edgePaddingSize: float):
		return cur_server.exec('mset.BakerObject.set_edgePaddingSize', __handle, _edgePaddingSize)

	edgePaddingSize: float = property(__get_edgePaddingSize, __set_edgePaddingSize)
	"""Edge padding size in pixels."""
	
	def __get_fixMirroredTangents(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_fixMirroredTangents', __handle)

	def __set_fixMirroredTangents(self, _fixMirroredTangents: bool):
		return cur_server.exec('mset.BakerObject.set_fixMirroredTangents', __handle, _fixMirroredTangents)

	fixMirroredTangents: bool = property(__get_fixMirroredTangents, __set_fixMirroredTangents)
	"""Fixes mirrored tangents, use this setting if you're seeing artifacts in your normal map bakes from your tangent space."""
	
	def __get_ignoreBackfaces(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_ignoreBackfaces', __handle)

	def __set_ignoreBackfaces(self, _ignoreBackfaces: bool):
		return cur_server.exec('mset.BakerObject.set_ignoreBackfaces', __handle, _ignoreBackfaces)

	ignoreBackfaces: bool = property(__get_ignoreBackfaces, __set_ignoreBackfaces)
	"""Determines whether back sides of faces will be ignored when baking."""
	
	def __get_ignoreTransforms(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_ignoreTransforms', __handle)

	def __set_ignoreTransforms(self, _ignoreTransforms: bool):
		return cur_server.exec('mset.BakerObject.set_ignoreTransforms', __handle, _ignoreTransforms)

	ignoreTransforms: bool = property(__get_ignoreTransforms, __set_ignoreTransforms)
	"""Determines whether transforms on meshes will be used when baking."""
	
	def __get_multipleTextureSets(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_multipleTextureSets', __handle)

	def __set_multipleTextureSets(self, _multipleTextureSets: bool):
		return cur_server.exec('mset.BakerObject.set_multipleTextureSets', __handle, _multipleTextureSets)

	multipleTextureSets: bool = property(__get_multipleTextureSets, __set_multipleTextureSets)
	"""Enables the use of Texture Sets when baking."""
	
	def __get_outputBits(self) -> int:
		return cur_server.exec('mset.BakerObject.get_outputBits', __handle)

	def __set_outputBits(self, _outputBits: int):
		return cur_server.exec('mset.BakerObject.set_outputBits', __handle, _outputBits)

	outputBits: int = property(__get_outputBits, __set_outputBits)
	"""Bit depth of the output format; must be one of the following values: 8, 16, 32."""
	
	def __get_outputHeight(self) -> int:
		return cur_server.exec('mset.BakerObject.get_outputHeight', __handle)

	def __set_outputHeight(self, _outputHeight: int):
		return cur_server.exec('mset.BakerObject.set_outputHeight', __handle, _outputHeight)

	outputHeight: int = property(__get_outputHeight, __set_outputHeight)
	"""The height in pixels of the baked textures."""
	
	def __get_outputPath(self) -> str:
		return cur_server.exec('mset.BakerObject.get_outputPath', __handle)

	def __set_outputPath(self, _outputPath: str):
		return cur_server.exec('mset.BakerObject.set_outputPath', __handle, _outputPath)

	outputPath: str = property(__get_outputPath, __set_outputPath)
	"""The file path where the baked textures will be stored."""
	
	def __get_outputSamples(self) -> int:
		return cur_server.exec('mset.BakerObject.get_outputSamples', __handle)

	def __set_outputSamples(self, _outputSamples: int):
		return cur_server.exec('mset.BakerObject.set_outputSamples', __handle, _outputSamples)

	outputSamples: int = property(__get_outputSamples, __set_outputSamples)
	"""Sample count of the bake output; must be one of the following values: 1, 4, 16."""
	
	def __get_outputSinglePsd(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_outputSinglePsd', __handle)

	def __set_outputSinglePsd(self, _outputSinglePsd: bool):
		return cur_server.exec('mset.BakerObject.set_outputSinglePsd', __handle, _outputSinglePsd)

	outputSinglePsd: bool = property(__get_outputSinglePsd, __set_outputSinglePsd)
	"""Determines whether the baked maps will be stored inside a single PSD file, or multiple files."""
	
	def __get_outputSoften(self) -> float:
		return cur_server.exec('mset.BakerObject.get_outputSoften', __handle)

	def __set_outputSoften(self, _outputSoften: float):
		return cur_server.exec('mset.BakerObject.set_outputSoften', __handle, _outputSoften)

	outputSoften: float = property(__get_outputSoften, __set_outputSoften)
	"""Determines how much the baked result will be softened; must be between 0.0 and 1.0."""
	
	def __get_outputWidth(self) -> int:
		return cur_server.exec('mset.BakerObject.get_outputWidth', __handle)

	def __set_outputWidth(self, _outputWidth: int):
		return cur_server.exec('mset.BakerObject.set_outputWidth', __handle, _outputWidth)

	outputWidth: int = property(__get_outputWidth, __set_outputWidth)
	"""The width in pixels of the baked textures."""
	
	def __get_smoothCage(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_smoothCage', __handle)

	def __set_smoothCage(self, _smoothCage: bool):
		return cur_server.exec('mset.BakerObject.set_smoothCage', __handle, _smoothCage)

	smoothCage: bool = property(__get_smoothCage, __set_smoothCage)
	"""Determines whether the cage mesh will use smooth vertex normals, ignoring any hard edges."""
	
	def __get_useHiddenMeshes(self) -> bool:
		return cur_server.exec('mset.BakerObject.get_useHiddenMeshes', __handle)

	def __set_useHiddenMeshes(self, _useHiddenMeshes: bool):
		return cur_server.exec('mset.BakerObject.set_useHiddenMeshes', __handle, _useHiddenMeshes)

	useHiddenMeshes: bool = property(__get_useHiddenMeshes, __set_useHiddenMeshes)
	"""Determines whether hidden meshes will be used when baking."""
	
	def addGroup(self, name: str):
		"""
		Adds a BakeGroup to the BakerObject.name: The Name of the BakeGroupreturns: The BakeGroup
		"""
		return cur_server.exec('mset.BakerObject.addGroup', __handle, name)

	def bake(self):
		"""
		Bakes with the current configuration.
		"""
		return cur_server.exec('mset.BakerObject.bake', __handle)

	def getAllMaps(self) -> List[BakerMap]:
		"""
		Gets a list of all baker maps.returns: A list of all baker map handles
		"""
		return cur_server.exec('mset.BakerObject.getAllMaps', __handle)

	def getMap(self, name: str) -> BakerMap:
		"""
		Gets a baker map handle.name: The Name of the Map you wantreturns: A handle to the Baker Output Map
		"""
		return cur_server.exec('mset.BakerObject.getMap', __handle, name)

	def getTextureSetCount(self) -> int:
		"""
		Gets the number of texture sets in the current BakerObject.returns: integer number of texture sets.
		"""
		return cur_server.exec('mset.BakerObject.getTextureSetCount', __handle)

	def getTextureSetEnabled(self, i: int) -> bool:
		"""
		Gets the enabled status of a texture set.i: The index of the texture set you wantreturns: True if the texture set is enabled False if not.
		"""
		return cur_server.exec('mset.BakerObject.getTextureSetEnabled', __handle, i)

	def getTextureSetHeight(self, i: int) -> int:
		"""
		Gets the height of a texture set.i: The index of the texture set you wantreturns: Height of the texture set.
		"""
		return cur_server.exec('mset.BakerObject.getTextureSetHeight', __handle, i)

	def getTextureSetName(self, i: int) -> str:
		"""
		Gets the name of a given texture set.i: The index of the Texture Set you wantreturns: the string name of the texture set.
		"""
		return cur_server.exec('mset.BakerObject.getTextureSetName', __handle, i)

	def getTextureSetWidth(self, i: int) -> int:
		"""
		Gets the width of a texture set.i: The index of the texture set you wantreturns: Width of texture set.
		"""
		return cur_server.exec('mset.BakerObject.getTextureSetWidth', __handle, i)

	def importModel(self, path: str):
		"""
		Imports a model file via the Baker's quick loader.path: string path to model file
		"""
		return cur_server.exec('mset.BakerObject.importModel', __handle, path)

	def loadPreset(self, name: str):
		"""
		loads a given preset for the BakerObject.name: The Name of the Preset
		"""
		return cur_server.exec('mset.BakerObject.loadPreset', __handle, name)

	def savePreset(self, name: str):
		"""
		saves the current configuration of the BakerObject.name: The Name of the Preset
		"""
		return cur_server.exec('mset.BakerObject.savePreset', __handle, name)

	def setTextureSetEnabled(self, i: int, enabled: bool):
		"""
		Sets whether or the texture set specified is enabled or disabled.i: The index of the Texture Set you wantenabled: if the texture set should bake or not.
		"""
		return cur_server.exec('mset.BakerObject.setTextureSetEnabled', __handle, i,enabled)

	def setTextureSetHeight(self, i: int, height: int):
		"""
		Sets the height of a given texture set.i: The index of the Texture Set you wantheight: your desired height of the texture set.
		"""
		return cur_server.exec('mset.BakerObject.setTextureSetHeight', __handle, i,height)

	def setTextureSetWidth(self, i: int, width: int):
		"""
		Sets the width of a given texture set.i: The index of the Texture Set you wantwidth: your desired width of the texture set.
		"""
		return cur_server.exec('mset.BakerObject.setTextureSetWidth', __handle, i,width)


class BakerTargetObject(SceneObject):
	"""
	Baker Target Object
	"""
	
	__handle = None
	def __get_cageAlpha(self) -> float:
		return cur_server.exec('mset.BakerTargetObject.get_cageAlpha', __handle)

	def __set_cageAlpha(self, _cageAlpha: float):
		return cur_server.exec('mset.BakerTargetObject.set_cageAlpha', __handle, _cageAlpha)

	cageAlpha: float = property(__get_cageAlpha, __set_cageAlpha)
	"""The opacity of the cage."""
	
	def __get_excludeWhenIgnoringGroups(self) -> bool:
		return cur_server.exec('mset.BakerTargetObject.get_excludeWhenIgnoringGroups', __handle)

	def __set_excludeWhenIgnoringGroups(self, _excludeWhenIgnoringGroups: bool):
		return cur_server.exec('mset.BakerTargetObject.set_excludeWhenIgnoringGroups', __handle, _excludeWhenIgnoringGroups)

	excludeWhenIgnoringGroups: bool = property(__get_excludeWhenIgnoringGroups, __set_excludeWhenIgnoringGroups)
	"""Whether this target will be used when ignoring groups in cone based ray passes (AO, Bent Normals)."""
	
	def __get_maxOffset(self) -> float:
		return cur_server.exec('mset.BakerTargetObject.get_maxOffset', __handle)

	def __set_maxOffset(self, _maxOffset: float):
		return cur_server.exec('mset.BakerTargetObject.set_maxOffset', __handle, _maxOffset)

	maxOffset: float = property(__get_maxOffset, __set_maxOffset)
	"""The maximum offset of the cage mask."""
	
	def __get_minOffset(self) -> float:
		return cur_server.exec('mset.BakerTargetObject.get_minOffset', __handle)

	def __set_minOffset(self, _minOffset: float):
		return cur_server.exec('mset.BakerTargetObject.set_minOffset', __handle, _minOffset)

	minOffset: float = property(__get_minOffset, __set_minOffset)
	"""The minimum offset of the cage mask."""
	
	def estimateOffset(self):
		"""
		Estimates the Cage Offsets.
		"""
		return cur_server.exec('mset.BakerTargetObject.estimateOffset', __handle)


class BentNormalBakerMap(BakerMap):
	"""
	Bent Normal Baker Map Settings
	"""
	
	__handle = None
	def __get_dither(self) -> bool:
		return cur_server.exec('mset.BentNormalBakerMap.get_dither', __handle)

	def __set_dither(self, _dither: bool):
		return cur_server.exec('mset.BentNormalBakerMap.set_dither', __handle, _dither)

	dither: bool = property(__get_dither, __set_dither)
	"""Determines whether this map output will be dithered."""
	
	def __get_flipX(self) -> bool:
		return cur_server.exec('mset.BentNormalBakerMap.get_flipX', __handle)

	def __set_flipX(self, _flipX: bool):
		return cur_server.exec('mset.BentNormalBakerMap.set_flipX', __handle, _flipX)

	flipX: bool = property(__get_flipX, __set_flipX)
	"""Determines whether the normal map's X channel will be flipped."""
	
	def __get_flipY(self) -> bool:
		return cur_server.exec('mset.BentNormalBakerMap.get_flipY', __handle)

	def __set_flipY(self, _flipY: bool):
		return cur_server.exec('mset.BentNormalBakerMap.set_flipY', __handle, _flipY)

	flipY: bool = property(__get_flipY, __set_flipY)
	"""Determines whether the normal map's Y channel will be flipped."""
	
	def __get_flipZ(self) -> bool:
		return cur_server.exec('mset.BentNormalBakerMap.get_flipZ', __handle)

	def __set_flipZ(self, _flipZ: bool):
		return cur_server.exec('mset.BentNormalBakerMap.set_flipZ', __handle, _flipZ)

	flipZ: bool = property(__get_flipZ, __set_flipZ)
	"""Determines whether the normal map's Z channel will be flipped."""
	
	def __get_ignoreGroups(self) -> bool:
		return cur_server.exec('mset.BentNormalBakerMap.get_ignoreGroups', __handle)

	def __set_ignoreGroups(self, _ignoreGroups: bool):
		return cur_server.exec('mset.BentNormalBakerMap.set_ignoreGroups', __handle, _ignoreGroups)

	ignoreGroups: bool = property(__get_ignoreGroups, __set_ignoreGroups)
	"""Determines whether bake groups will be ignored when baking bent normals."""
	
	def __get_rayCount(self) -> int:
		return cur_server.exec('mset.BentNormalBakerMap.get_rayCount', __handle)

	def __set_rayCount(self, _rayCount: int):
		return cur_server.exec('mset.BentNormalBakerMap.set_rayCount', __handle, _rayCount)

	rayCount: int = property(__get_rayCount, __set_rayCount)
	"""The number of rays used for Bent Normal baking."""
	
	def __get_searchDistance(self) -> float:
		return cur_server.exec('mset.BentNormalBakerMap.get_searchDistance', __handle)

	def __set_searchDistance(self, _searchDistance: float):
		return cur_server.exec('mset.BentNormalBakerMap.set_searchDistance', __handle, _searchDistance)

	searchDistance: float = property(__get_searchDistance, __set_searchDistance)
	"""The maximum distance rays can go. 0 defaults to infinity."""
	

class CurvatureBakerMap(BakerMap):
	"""
	Curvature Baker Map Settings
	"""
	
	__handle = None
	def __get_dither(self) -> bool:
		return cur_server.exec('mset.CurvatureBakerMap.get_dither', __handle)

	def __set_dither(self, _dither: bool):
		return cur_server.exec('mset.CurvatureBakerMap.set_dither', __handle, _dither)

	dither: bool = property(__get_dither, __set_dither)
	"""Determines whether this map output will be dithered."""
	
	def __get_strength(self) -> float:
		return cur_server.exec('mset.CurvatureBakerMap.get_strength', __handle)

	def __set_strength(self, _strength: float):
		return cur_server.exec('mset.CurvatureBakerMap.set_strength', __handle, _strength)

	strength: float = property(__get_strength, __set_strength)
	"""Determines the strength of the curvature output."""
	

class FogObject(SceneObject):
	"""
	Fog Object
	"""
	
	__handle = None
	def __get_color(self) -> List[float]:
		return cur_server.exec('mset.FogObject.get_color', __handle)

	def __set_color(self, _color: List[float]):
		return cur_server.exec('mset.FogObject.set_color', __handle, _color)

	color: List[float] = property(__get_color, __set_color)
	"""The color of the fog effect, as a list of 3 floats for RGB color."""
	
	def __get_dispersion(self) -> float:
		return cur_server.exec('mset.FogObject.get_dispersion', __handle)

	def __set_dispersion(self, _dispersion: float):
		return cur_server.exec('mset.FogObject.set_dispersion', __handle, _dispersion)

	dispersion: float = property(__get_dispersion, __set_dispersion)
	"""A scalar specifying the dispersion, or light scatter, property of the fog effect."""
	
	def __get_distance(self) -> float:
		return cur_server.exec('mset.FogObject.get_distance', __handle)

	def __set_distance(self, _distance: float):
		return cur_server.exec('mset.FogObject.set_distance', __handle, _distance)

	distance: float = property(__get_distance, __set_distance)
	"""The distance of the fog effect."""
	
	def __get_lightIllum(self) -> float:
		return cur_server.exec('mset.FogObject.get_lightIllum', __handle)

	def __set_lightIllum(self, _lightIllum: float):
		return cur_server.exec('mset.FogObject.set_lightIllum', __handle, _lightIllum)

	lightIllum: float = property(__get_lightIllum, __set_lightIllum)
	"""A scalar specifying the degree to which lights affect the fog."""
	
	def __get_opacity(self) -> float:
		return cur_server.exec('mset.FogObject.get_opacity', __handle)

	def __set_opacity(self, _opacity: float):
		return cur_server.exec('mset.FogObject.set_opacity', __handle, _opacity)

	opacity: float = property(__get_opacity, __set_opacity)
	"""The maximum opacity of the fog effect."""
	
	def __get_skyIllum(self) -> float:
		return cur_server.exec('mset.FogObject.get_skyIllum', __handle)

	def __set_skyIllum(self, _skyIllum: float):
		return cur_server.exec('mset.FogObject.set_skyIllum', __handle, _skyIllum)

	skyIllum: float = property(__get_skyIllum, __set_skyIllum)
	"""A scalar specifying the degree to which sky illumination affects the fog."""
	
	def __get_type(self) -> str:
		return cur_server.exec('mset.FogObject.get_type', __handle)

	def __set_type(self, _type: str):
		return cur_server.exec('mset.FogObject.set_type', __handle, _type)

	type: str = property(__get_type, __set_type)
	"""The falloff type of the fog effect. Must be one of the following values: 'Linear' 'Distance Squared' 'Exponential'."""
	

class HeightBakerMap(BakerMap):
	"""
	Height Baker Map Settings
	"""
	
	__handle = None
	def __get_dither(self) -> bool:
		return cur_server.exec('mset.HeightBakerMap.get_dither', __handle)

	def __set_dither(self, _dither: bool):
		return cur_server.exec('mset.HeightBakerMap.set_dither', __handle, _dither)

	dither: bool = property(__get_dither, __set_dither)
	"""Determines whether this map output will be dithered."""
	
	def __get_innerDistance(self) -> float:
		return cur_server.exec('mset.HeightBakerMap.get_innerDistance', __handle)

	def __set_innerDistance(self, _innerDistance: float):
		return cur_server.exec('mset.HeightBakerMap.set_innerDistance', __handle, _innerDistance)

	innerDistance: float = property(__get_innerDistance, __set_innerDistance)
	"""Inner height map distance from the low poly mesh, in world units. This value maps to black in the height map."""
	
	def __get_outerDistance(self) -> float:
		return cur_server.exec('mset.HeightBakerMap.get_outerDistance', __handle)

	def __set_outerDistance(self, _outerDistance: float):
		return cur_server.exec('mset.HeightBakerMap.set_outerDistance', __handle, _outerDistance)

	outerDistance: float = property(__get_outerDistance, __set_outerDistance)
	"""Outer height map distance from the low poly mesh, in world units. This value maps to white in the height map."""
	

class MetalnessBakerMap(BakerMap):
	"""
	Metalness Baker Map Settings
	"""
	
	__handle = None
	def __get_metalnessThreshold(self) -> float:
		return cur_server.exec('mset.MetalnessBakerMap.get_metalnessThreshold', __handle)

	def __set_metalnessThreshold(self, _metalnessThreshold: float):
		return cur_server.exec('mset.MetalnessBakerMap.set_metalnessThreshold', __handle, _metalnessThreshold)

	metalnessThreshold: float = property(__get_metalnessThreshold, __set_metalnessThreshold)
	"""Any specular value above this threshold will be considered metal."""
	

class NormalBakerMap(BakerMap):
	"""
	Normal Baker Map Settings
	"""
	
	__handle = None
	def __get_dither(self) -> bool:
		return cur_server.exec('mset.NormalBakerMap.get_dither', __handle)

	def __set_dither(self, _dither: bool):
		return cur_server.exec('mset.NormalBakerMap.set_dither', __handle, _dither)

	dither: bool = property(__get_dither, __set_dither)
	"""Determines whether this map output will be dithered."""
	
	def __get_flipX(self) -> bool:
		return cur_server.exec('mset.NormalBakerMap.get_flipX', __handle)

	def __set_flipX(self, _flipX: bool):
		return cur_server.exec('mset.NormalBakerMap.set_flipX', __handle, _flipX)

	flipX: bool = property(__get_flipX, __set_flipX)
	"""Determines whether the normal map's X channel will be flipped."""
	
	def __get_flipY(self) -> bool:
		return cur_server.exec('mset.NormalBakerMap.get_flipY', __handle)

	def __set_flipY(self, _flipY: bool):
		return cur_server.exec('mset.NormalBakerMap.set_flipY', __handle, _flipY)

	flipY: bool = property(__get_flipY, __set_flipY)
	"""Determines whether the normal map's Y channel will be flipped."""
	
	def __get_flipZ(self) -> bool:
		return cur_server.exec('mset.NormalBakerMap.get_flipZ', __handle)

	def __set_flipZ(self, _flipZ: bool):
		return cur_server.exec('mset.NormalBakerMap.set_flipZ', __handle, _flipZ)

	flipZ: bool = property(__get_flipZ, __set_flipZ)
	"""Determines whether the normal map's Z channel will be flipped."""
	

class PositionBakerMap(BakerMap):
	"""
	Position Baker Map Settings
	"""
	
	__handle = None
	def __get_normalization(self) -> str:
		return cur_server.exec('mset.PositionBakerMap.get_normalization', __handle)

	def __set_normalization(self, _normalization: str):
		return cur_server.exec('mset.PositionBakerMap.set_normalization', __handle, _normalization)

	normalization: str = property(__get_normalization, __set_normalization)
	"""The method by which you normalize position data."""
	

class RenderObject(SceneObject):
	"""
	Render Object in scene. Manages render configuration can render images/videos.
	"""
	
	__handle = None
	def __get_cameras(self) -> List[RenderCamera]:
		return cur_server.exec('mset.RenderObject.get_cameras', __handle)

	def __set_cameras(self, _cameras: List[RenderCamera]):
		return cur_server.exec('mset.RenderObject.set_cameras', __handle, _cameras)

	cameras: List[RenderCamera] = property(__get_cameras, __set_cameras)
	"""Cameras configured to render with Toolbag."""
	
	def __get_images(self) -> RenderOutputOptions:
		return cur_server.exec('mset.RenderObject.get_images', __handle)

	def __set_images(self, _images: RenderOutputOptions):
		return cur_server.exec('mset.RenderObject.set_images', __handle, _images)

	images: RenderOutputOptions = property(__get_images, __set_images)
	"""Output configuration for image outputs."""
	
	def __get_options(self) -> RenderOptions:
		return cur_server.exec('mset.RenderObject.get_options', __handle)

	def __set_options(self, _options: RenderOptions):
		return cur_server.exec('mset.RenderObject.set_options', __handle, _options)

	options: RenderOptions = property(__get_options, __set_options)
	"""Render settings for Full Composite configurations of Toolbag."""
	
	def __get_renderPasses(self) -> List[RenderPass]:
		return cur_server.exec('mset.RenderObject.get_renderPasses', __handle)

	def __set_renderPasses(self, _renderPasses: List[RenderPass]):
		return cur_server.exec('mset.RenderObject.set_renderPasses', __handle, _renderPasses)

	renderPasses: List[RenderPass] = property(__get_renderPasses, __set_renderPasses)
	"""Cameras configured to render with Toolbag."""
	
	def __get_videos(self) -> RenderOutputOptions:
		return cur_server.exec('mset.RenderObject.get_videos', __handle)

	def __set_videos(self, _videos: RenderOutputOptions):
		return cur_server.exec('mset.RenderObject.set_videos', __handle, _videos)

	videos: RenderOutputOptions = property(__get_videos, __set_videos)
	"""Output configuration for video outputs."""
	
	def renderImages(self):
		"""
		Render all enabled images in this render object.
		"""
		return cur_server.exec('mset.RenderObject.renderImages', __handle)

	def renderVideos(self):
		"""
		Render all enabled videos in this render object.
		"""
		return cur_server.exec('mset.RenderObject.renderVideos', __handle)


class SkyBoxObject(SceneObject):
	"""
	Skybox Scene Object
	"""
	
	__handle = None
	def __get_backgroundBrightness(self) -> float:
		return cur_server.exec('mset.SkyBoxObject.get_backgroundBrightness', __handle)

	def __set_backgroundBrightness(self, _backgroundBrightness: float):
		return cur_server.exec('mset.SkyBoxObject.set_backgroundBrightness', __handle, _backgroundBrightness)

	backgroundBrightness: float = property(__get_backgroundBrightness, __set_backgroundBrightness)
	"""The brightness of the skybox background."""
	
	def __get_blur(self) -> float:
		return cur_server.exec('mset.SkyBoxObject.get_blur', __handle)

	def __set_blur(self, _blur: float):
		return cur_server.exec('mset.SkyBoxObject.set_blur', __handle, _blur)

	blur: float = property(__get_blur, __set_blur)
	"""The amount of blurring for the background."""
	
	def __get_brightness(self) -> float:
		return cur_server.exec('mset.SkyBoxObject.get_brightness', __handle)

	def __set_brightness(self, _brightness: float):
		return cur_server.exec('mset.SkyBoxObject.set_brightness', __handle, _brightness)

	brightness: float = property(__get_brightness, __set_brightness)
	"""The brightness of the skybox."""
	
	def __get_mode(self) -> str:
		return cur_server.exec('mset.SkyBoxObject.get_mode', __handle)

	def __set_mode(self, _mode: str):
		return cur_server.exec('mset.SkyBoxObject.set_mode', __handle, _mode)

	mode: str = property(__get_mode, __set_mode)
	"""The background mode. Can be 'color', 'sky', 'blurred sky', or 'ambient sky'."""
	
	def __get_rotation(self) -> float:
		return cur_server.exec('mset.SkyBoxObject.get_rotation', __handle)

	def __set_rotation(self, _rotation: float):
		return cur_server.exec('mset.SkyBoxObject.set_rotation', __handle, _rotation)

	rotation: float = property(__get_rotation, __set_rotation)
	"""The current rotation angle of the skybox."""
	
	def clearLightChildren(self):
		"""
		Clears all light children of this skybox.
		"""
		return cur_server.exec('mset.SkyBoxObject.clearLightChildren', __handle)

	def importImage(self, path: str):
		"""
		Imports an image to use for this skybox.
		"""
		return cur_server.exec('mset.SkyBoxObject.importImage', __handle, path)

	def loadSky(self, path: str):
		"""
		Loads a .tbsky file in place of the current sky.
		"""
		return cur_server.exec('mset.SkyBoxObject.loadSky', __handle, path)

	def renderPreview(self, width: int, height: int) -> Image:
		"""
		Renders the sky background, in latitude-longitude format, to a preview image. Returns an mset.Image instance.
		"""
		return cur_server.exec('mset.SkyBoxObject.renderPreview', __handle, width,height)

	def saveSky(self, path: str):
		"""
		Saves the current sky to the specified file path as a .tbsky archive.
		"""
		return cur_server.exec('mset.SkyBoxObject.saveSky', __handle, path)


class SubMeshObject(SceneObject):
	"""
	Sub Mesh Object
	"""
	
	__handle = None
	def __get_indexCount(self) -> int:
		return cur_server.exec('mset.SubMeshObject.get_indexCount', __handle)

	def __set_indexCount(self, _indexCount: int):
		return cur_server.exec('mset.SubMeshObject.set_indexCount', __handle, _indexCount)

	indexCount: int = property(__get_indexCount, __set_indexCount)
	"""The index count of the submesh."""
	
	def __get_material(self) -> Material:
		return cur_server.exec('mset.SubMeshObject.get_material', __handle)

	def __set_material(self, _material: Material):
		return cur_server.exec('mset.SubMeshObject.set_material', __handle, _material)

	material: Material = property(__get_material, __set_material)
	"""The material assigned to the submesh."""
	
	def __get_startIndex(self) -> int:
		return cur_server.exec('mset.SubMeshObject.get_startIndex', __handle)

	def __set_startIndex(self, _startIndex: int):
		return cur_server.exec('mset.SubMeshObject.set_startIndex', __handle, _startIndex)

	startIndex: int = property(__get_startIndex, __set_startIndex)
	"""The first index of the submesh."""
	

class TextureProjectLayerBlur(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_px(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerBlur.get_px', __handle)

	def __set_px(self, _px: int):
		return cur_server.exec('mset.TextureProjectLayerBlur.set_px', __handle, _px)

	px: int = property(__get_px, __set_px)
	"""A property of a layer."""
	

class TextureProjectLayerCellular(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_invert(self) -> bool:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_invert', __handle)

	def __set_invert(self, _invert: bool):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_invert', __handle, _invert)

	invert: bool = property(__get_invert, __set_invert)
	"""A property of a layer."""
	
	def __get_jitter(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_jitter', __handle)

	def __set_jitter(self, _jitter: float):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_jitter', __handle, _jitter)

	jitter: float = property(__get_jitter, __set_jitter)
	"""A property of a layer."""
	
	def __get_phase(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_phase', __handle)

	def __set_phase(self, _phase: float):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_phase', __handle, _phase)

	phase: float = property(__get_phase, __set_phase)
	"""A property of a layer."""
	
	def __get_randomSeed(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_randomSeed', __handle)

	def __set_randomSeed(self, _randomSeed: int):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_randomSeed', __handle, _randomSeed)

	randomSeed: int = property(__get_randomSeed, __set_randomSeed)
	"""A property of a layer."""
	
	def __get_scale(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_scale', __handle)

	def __set_scale(self, _scale: int):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_scale', __handle, _scale)

	scale: int = property(__get_scale, __set_scale)
	"""A property of a layer."""
	
	def __get_smoothing(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_smoothing', __handle)

	def __set_smoothing(self, _smoothing: float):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_smoothing', __handle, _smoothing)

	smoothing: float = property(__get_smoothing, __set_smoothing)
	"""A property of a layer."""
	
	def __get_warpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_warpAmount', __handle)

	def __set_warpAmount(self, _warpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_warpAmount', __handle, _warpAmount)

	warpAmount: float = property(__get_warpAmount, __set_warpAmount)
	"""A property of a layer."""
	
	def __get_warpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCellular.get_warpDetail', __handle)

	def __set_warpDetail(self, _warpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerCellular.set_warpDetail', __handle, _warpDetail)

	warpDetail: float = property(__get_warpDetail, __set_warpDetail)
	"""A property of a layer."""
	

class TextureProjectLayerCheckered(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_A(self) -> List[float]:
		return cur_server.exec('mset.TextureProjectLayerCheckered.get_A', __handle)

	def __set_A(self, _A: List[float]):
		return cur_server.exec('mset.TextureProjectLayerCheckered.set_A', __handle, _A)

	A: List[float] = property(__get_A, __set_A)
	"""A property of a layer."""
	
	def __get_B(self) -> List[float]:
		return cur_server.exec('mset.TextureProjectLayerCheckered.get_B', __handle)

	def __set_B(self, _B: List[float]):
		return cur_server.exec('mset.TextureProjectLayerCheckered.set_B', __handle, _B)

	B: List[float] = property(__get_B, __set_B)
	"""A property of a layer."""
	
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCheckered.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerCheckered.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_tileCount(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerCheckered.get_tileCount', __handle)

	def __set_tileCount(self, _tileCount: int):
		return cur_server.exec('mset.TextureProjectLayerCheckered.set_tileCount', __handle, _tileCount)

	tileCount: int = property(__get_tileCount, __set_tileCount)
	"""A property of a layer."""
	
	def __get_warpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCheckered.get_warpAmount', __handle)

	def __set_warpAmount(self, _warpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerCheckered.set_warpAmount', __handle, _warpAmount)

	warpAmount: float = property(__get_warpAmount, __set_warpAmount)
	"""A property of a layer."""
	
	def __get_warpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerCheckered.get_warpDetail', __handle)

	def __set_warpDetail(self, _warpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerCheckered.set_warpDetail', __handle, _warpDetail)

	warpDetail: float = property(__get_warpDetail, __set_warpDetail)
	"""A property of a layer."""
	

class TextureProjectLayerClouds(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_granularity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerClouds.get_granularity', __handle)

	def __set_granularity(self, _granularity: float):
		return cur_server.exec('mset.TextureProjectLayerClouds.set_granularity', __handle, _granularity)

	granularity: float = property(__get_granularity, __set_granularity)
	"""A property of a layer."""
	
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerClouds.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerClouds.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_randomSeed(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerClouds.get_randomSeed', __handle)

	def __set_randomSeed(self, _randomSeed: int):
		return cur_server.exec('mset.TextureProjectLayerClouds.set_randomSeed', __handle, _randomSeed)

	randomSeed: int = property(__get_randomSeed, __set_randomSeed)
	"""A property of a layer."""
	
	def __get_scale(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerClouds.get_scale', __handle)

	def __set_scale(self, _scale: float):
		return cur_server.exec('mset.TextureProjectLayerClouds.set_scale', __handle, _scale)

	scale: float = property(__get_scale, __set_scale)
	"""A property of a layer."""
	
	def __get_warpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerClouds.get_warpAmount', __handle)

	def __set_warpAmount(self, _warpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerClouds.set_warpAmount', __handle, _warpAmount)

	warpAmount: float = property(__get_warpAmount, __set_warpAmount)
	"""A property of a layer."""
	
	def __get_warpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerClouds.get_warpDetail', __handle)

	def __set_warpDetail(self, _warpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerClouds.set_warpDetail', __handle, _warpDetail)

	warpDetail: float = property(__get_warpDetail, __set_warpDetail)
	"""A property of a layer."""
	

class TextureProjectLayerColorSelection(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_source(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerColorSelection.get_source', __handle)

	def __set_source(self, _source: int):
		return cur_server.exec('mset.TextureProjectLayerColorSelection.set_source', __handle, _source)

	source: int = property(__get_source, __set_source)
	"""A property of a layer."""
	

class TextureProjectLayerCurvature(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerCurves(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_spline(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerCurves.get_spline', __handle)

	def __set_spline(self, _spline: Any):
		return cur_server.exec('mset.TextureProjectLayerCurves.set_spline', __handle, _spline)

	spline: Any = property(__get_spline, __set_spline)
	"""A property of a layer."""
	

class TextureProjectLayerDirection(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerDirt(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_brightness(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_brightness', __handle)

	def __set_brightness(self, _brightness: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_brightness', __handle, _brightness)

	brightness: float = property(__get_brightness, __set_brightness)
	"""A property of a layer."""
	
	def __get_contrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_contrast', __handle)

	def __set_contrast(self, _contrast: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_contrast', __handle, _contrast)

	contrast: float = property(__get_contrast, __set_contrast)
	"""A property of a layer."""
	
	def __get_creviceContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_creviceContrast', __handle)

	def __set_creviceContrast(self, _creviceContrast: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_creviceContrast', __handle, _creviceContrast)

	creviceContrast: float = property(__get_creviceContrast, __set_creviceContrast)
	"""A property of a layer."""
	
	def __get_creviceIntensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_creviceIntensity', __handle)

	def __set_creviceIntensity(self, _creviceIntensity: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_creviceIntensity', __handle, _creviceIntensity)

	creviceIntensity: float = property(__get_creviceIntensity, __set_creviceIntensity)
	"""A property of a layer."""
	
	def __get_creviceThickness(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_creviceThickness', __handle)

	def __set_creviceThickness(self, _creviceThickness: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_creviceThickness', __handle, _creviceThickness)

	creviceThickness: float = property(__get_creviceThickness, __set_creviceThickness)
	"""A property of a layer."""
	
	def __get_directionContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_directionContrast', __handle)

	def __set_directionContrast(self, _directionContrast: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_directionContrast', __handle, _directionContrast)

	directionContrast: float = property(__get_directionContrast, __set_directionContrast)
	"""A property of a layer."""
	
	def __get_directionIntensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_directionIntensity', __handle)

	def __set_directionIntensity(self, _directionIntensity: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_directionIntensity', __handle, _directionIntensity)

	directionIntensity: float = property(__get_directionIntensity, __set_directionIntensity)
	"""A property of a layer."""
	
	def __get_grungeContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_grungeContrast', __handle)

	def __set_grungeContrast(self, _grungeContrast: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_grungeContrast', __handle, _grungeContrast)

	grungeContrast: float = property(__get_grungeContrast, __set_grungeContrast)
	"""A property of a layer."""
	
	def __get_grungeIntensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_grungeIntensity', __handle)

	def __set_grungeIntensity(self, _grungeIntensity: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_grungeIntensity', __handle, _grungeIntensity)

	grungeIntensity: float = property(__get_grungeIntensity, __set_grungeIntensity)
	"""A property of a layer."""
	
	def __get_grungeScale(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_grungeScale', __handle)

	def __set_grungeScale(self, _grungeScale: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_grungeScale', __handle, _grungeScale)

	grungeScale: float = property(__get_grungeScale, __set_grungeScale)
	"""A property of a layer."""
	
	def __get_occlusionContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_occlusionContrast', __handle)

	def __set_occlusionContrast(self, _occlusionContrast: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_occlusionContrast', __handle, _occlusionContrast)

	occlusionContrast: float = property(__get_occlusionContrast, __set_occlusionContrast)
	"""A property of a layer."""
	
	def __get_occlusionIntensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_occlusionIntensity', __handle)

	def __set_occlusionIntensity(self, _occlusionIntensity: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_occlusionIntensity', __handle, _occlusionIntensity)

	occlusionIntensity: float = property(__get_occlusionIntensity, __set_occlusionIntensity)
	"""A property of a layer."""
	
	def __get_sharpness(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerDirt.get_sharpness', __handle)

	def __set_sharpness(self, _sharpness: float):
		return cur_server.exec('mset.TextureProjectLayerDirt.set_sharpness', __handle, _sharpness)

	sharpness: float = property(__get_sharpness, __set_sharpness)
	"""A property of a layer."""
	

class TextureProjectLayerFill(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_material(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerFill.get_material', __handle)

	def __set_material(self, _material: Any):
		return cur_server.exec('mset.TextureProjectLayerFill.set_material', __handle, _material)

	material: Any = property(__get_material, __set_material)
	"""Property of a layer."""
	
	def __get_projection(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerFill.get_projection', __handle)

	def __set_projection(self, _projection: Any):
		return cur_server.exec('mset.TextureProjectLayerFill.set_projection', __handle, _projection)

	projection: Any = property(__get_projection, __set_projection)
	"""A property of a layer."""
	

class TextureProjectLayerGradient(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerGradient.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerGradient.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_scale(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerGradient.get_scale', __handle)

	def __set_scale(self, _scale: float):
		return cur_server.exec('mset.TextureProjectLayerGradient.set_scale', __handle, _scale)

	scale: float = property(__get_scale, __set_scale)
	"""A property of a layer."""
	

class TextureProjectLayerGradientMap(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerHueSaturation(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerInvert(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerLevels(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerOcclusion(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_contrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerOcclusion.get_contrast', __handle)

	def __set_contrast(self, _contrast: float):
		return cur_server.exec('mset.TextureProjectLayerOcclusion.set_contrast', __handle, _contrast)

	contrast: float = property(__get_contrast, __set_contrast)
	"""A property of a layer."""
	
	def __get_contrastCenter(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerOcclusion.get_contrastCenter', __handle)

	def __set_contrastCenter(self, _contrastCenter: float):
		return cur_server.exec('mset.TextureProjectLayerOcclusion.set_contrastCenter', __handle, _contrastCenter)

	contrastCenter: float = property(__get_contrastCenter, __set_contrastCenter)
	"""A property of a layer."""
	
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerOcclusion.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerOcclusion.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_smoothing(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerOcclusion.get_smoothing', __handle)

	def __set_smoothing(self, _smoothing: float):
		return cur_server.exec('mset.TextureProjectLayerOcclusion.set_smoothing', __handle, _smoothing)

	smoothing: float = property(__get_smoothing, __set_smoothing)
	"""A property of a layer."""
	

class TextureProjectLayerPaint(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None

class TextureProjectLayerPerlin(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_contrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_contrast', __handle)

	def __set_contrast(self, _contrast: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_contrast', __handle, _contrast)

	contrast: float = property(__get_contrast, __set_contrast)
	"""A property of a layer."""
	
	def __get_invert(self) -> bool:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_invert', __handle)

	def __set_invert(self, _invert: bool):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_invert', __handle, _invert)

	invert: bool = property(__get_invert, __set_invert)
	"""A property of a layer."""
	
	def __get_macroContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_macroContrast', __handle)

	def __set_macroContrast(self, _macroContrast: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_macroContrast', __handle, _macroContrast)

	macroContrast: float = property(__get_macroContrast, __set_macroContrast)
	"""A property of a layer."""
	
	def __get_macroWarpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_macroWarpAmount', __handle)

	def __set_macroWarpAmount(self, _macroWarpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_macroWarpAmount', __handle, _macroWarpAmount)

	macroWarpAmount: float = property(__get_macroWarpAmount, __set_macroWarpAmount)
	"""A property of a layer."""
	
	def __get_macroWarpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_macroWarpDetail', __handle)

	def __set_macroWarpDetail(self, _macroWarpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_macroWarpDetail', __handle, _macroWarpDetail)

	macroWarpDetail: float = property(__get_macroWarpDetail, __set_macroWarpDetail)
	"""A property of a layer."""
	
	def __get_microContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_microContrast', __handle)

	def __set_microContrast(self, _microContrast: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_microContrast', __handle, _microContrast)

	microContrast: float = property(__get_microContrast, __set_microContrast)
	"""A property of a layer."""
	
	def __get_microWarpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_microWarpAmount', __handle)

	def __set_microWarpAmount(self, _microWarpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_microWarpAmount', __handle, _microWarpAmount)

	microWarpAmount: float = property(__get_microWarpAmount, __set_microWarpAmount)
	"""A property of a layer."""
	
	def __get_microWarpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_microWarpDetail', __handle)

	def __set_microWarpDetail(self, _microWarpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_microWarpDetail', __handle, _microWarpDetail)

	microWarpDetail: float = property(__get_microWarpDetail, __set_microWarpDetail)
	"""A property of a layer."""
	
	def __get_noisePasses(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_noisePasses', __handle)

	def __set_noisePasses(self, _noisePasses: int):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_noisePasses', __handle, _noisePasses)

	noisePasses: int = property(__get_noisePasses, __set_noisePasses)
	"""A property of a layer."""
	
	def __get_sampling(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_sampling', __handle)

	def __set_sampling(self, _sampling: int):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_sampling', __handle, _sampling)

	sampling: int = property(__get_sampling, __set_sampling)
	"""A property of a layer."""
	
	def __get_scale(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_scale', __handle)

	def __set_scale(self, _scale: float):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_scale', __handle, _scale)

	scale: float = property(__get_scale, __set_scale)
	"""A property of a layer."""
	
	def __get_seed(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_seed', __handle)

	def __set_seed(self, _seed: int):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_seed', __handle, _seed)

	seed: int = property(__get_seed, __set_seed)
	"""A property of a layer."""
	
	def __get_unitCount(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerPerlin.get_unitCount', __handle)

	def __set_unitCount(self, _unitCount: int):
		return cur_server.exec('mset.TextureProjectLayerPerlin.set_unitCount', __handle, _unitCount)

	unitCount: int = property(__get_unitCount, __set_unitCount)
	"""A property of a layer."""
	

class TextureProjectLayerScratch(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_grungeContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerScratch.get_grungeContrast', __handle)

	def __set_grungeContrast(self, _grungeContrast: float):
		return cur_server.exec('mset.TextureProjectLayerScratch.set_grungeContrast', __handle, _grungeContrast)

	grungeContrast: float = property(__get_grungeContrast, __set_grungeContrast)
	"""A property of a layer."""
	
	def __get_grungeIntensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerScratch.get_grungeIntensity', __handle)

	def __set_grungeIntensity(self, _grungeIntensity: float):
		return cur_server.exec('mset.TextureProjectLayerScratch.set_grungeIntensity', __handle, _grungeIntensity)

	grungeIntensity: float = property(__get_grungeIntensity, __set_grungeIntensity)
	"""A property of a layer."""
	

class TextureProjectLayerSharpen(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_amount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerSharpen.get_amount', __handle)

	def __set_amount(self, _amount: float):
		return cur_server.exec('mset.TextureProjectLayerSharpen.set_amount', __handle, _amount)

	amount: float = property(__get_amount, __set_amount)
	"""A property of a layer."""
	
	def __get_radius(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerSharpen.get_radius', __handle)

	def __set_radius(self, _radius: float):
		return cur_server.exec('mset.TextureProjectLayerSharpen.set_radius', __handle, _radius)

	radius: float = property(__get_radius, __set_radius)
	"""A property of a layer."""
	

class TextureProjectLayerThickness(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_contrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerThickness.get_contrast', __handle)

	def __set_contrast(self, _contrast: float):
		return cur_server.exec('mset.TextureProjectLayerThickness.set_contrast', __handle, _contrast)

	contrast: float = property(__get_contrast, __set_contrast)
	"""A property of a layer."""
	
	def __get_contrastCenter(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerThickness.get_contrastCenter', __handle)

	def __set_contrastCenter(self, _contrastCenter: float):
		return cur_server.exec('mset.TextureProjectLayerThickness.set_contrastCenter', __handle, _contrastCenter)

	contrastCenter: float = property(__get_contrastCenter, __set_contrastCenter)
	"""A property of a layer."""
	
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerThickness.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerThickness.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_smoothing(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerThickness.get_smoothing', __handle)

	def __set_smoothing(self, _smoothing: float):
		return cur_server.exec('mset.TextureProjectLayerThickness.set_smoothing', __handle, _smoothing)

	smoothing: float = property(__get_smoothing, __set_smoothing)
	"""A property of a layer."""
	

class TextureProjectLayerTiles(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_bevelDepth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_bevelDepth', __handle)

	def __set_bevelDepth(self, _bevelDepth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_bevelDepth', __handle, _bevelDepth)

	bevelDepth: float = property(__get_bevelDepth, __set_bevelDepth)
	"""A property of a layer."""
	
	def __get_bevelRoundness(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_bevelRoundness', __handle)

	def __set_bevelRoundness(self, _bevelRoundness: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_bevelRoundness', __handle, _bevelRoundness)

	bevelRoundness: float = property(__get_bevelRoundness, __set_bevelRoundness)
	"""A property of a layer."""
	
	def __get_bevelWidth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_bevelWidth', __handle)

	def __set_bevelWidth(self, _bevelWidth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_bevelWidth', __handle, _bevelWidth)

	bevelWidth: float = property(__get_bevelWidth, __set_bevelWidth)
	"""A property of a layer."""
	
	def __get_cornerRoundness(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_cornerRoundness', __handle)

	def __set_cornerRoundness(self, _cornerRoundness: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_cornerRoundness', __handle, _cornerRoundness)

	cornerRoundness: float = property(__get_cornerRoundness, __set_cornerRoundness)
	"""A property of a layer."""
	
	def __get_groutDepth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_groutDepth', __handle)

	def __set_groutDepth(self, _groutDepth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_groutDepth', __handle, _groutDepth)

	groutDepth: float = property(__get_groutDepth, __set_groutDepth)
	"""A property of a layer."""
	
	def __get_groutWidth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_groutWidth', __handle)

	def __set_groutWidth(self, _groutWidth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_groutWidth', __handle, _groutWidth)

	groutWidth: float = property(__get_groutWidth, __set_groutWidth)
	"""A property of a layer."""
	
	def __get_groutX(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_groutX', __handle)

	def __set_groutX(self, _groutX: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_groutX', __handle, _groutX)

	groutX: float = property(__get_groutX, __set_groutX)
	"""A property of a layer."""
	
	def __get_groutY(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_groutY', __handle)

	def __set_groutY(self, _groutY: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_groutY', __handle, _groutY)

	groutY: float = property(__get_groutY, __set_groutY)
	"""A property of a layer."""
	
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_invert(self) -> bool:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_invert', __handle)

	def __set_invert(self, _invert: bool):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_invert', __handle, _invert)

	invert: bool = property(__get_invert, __set_invert)
	"""A property of a layer."""
	
	def __get_maxX(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_maxX', __handle)

	def __set_maxX(self, _maxX: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_maxX', __handle, _maxX)

	maxX: float = property(__get_maxX, __set_maxX)
	"""A property of a layer."""
	
	def __get_maxY(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_maxY', __handle)

	def __set_maxY(self, _maxY: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_maxY', __handle, _maxY)

	maxY: float = property(__get_maxY, __set_maxY)
	"""A property of a layer."""
	
	def __get_maxZ(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_maxZ', __handle)

	def __set_maxZ(self, _maxZ: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_maxZ', __handle, _maxZ)

	maxZ: float = property(__get_maxZ, __set_maxZ)
	"""A property of a layer."""
	
	def __get_randomDepth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_randomDepth', __handle)

	def __set_randomDepth(self, _randomDepth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_randomDepth', __handle, _randomDepth)

	randomDepth: float = property(__get_randomDepth, __set_randomDepth)
	"""A property of a layer."""
	
	def __get_randomRotation(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_randomRotation', __handle)

	def __set_randomRotation(self, _randomRotation: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_randomRotation', __handle, _randomRotation)

	randomRotation: float = property(__get_randomRotation, __set_randomRotation)
	"""A property of a layer."""
	
	def __get_randomSeed(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_randomSeed', __handle)

	def __set_randomSeed(self, _randomSeed: int):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_randomSeed', __handle, _randomSeed)

	randomSeed: int = property(__get_randomSeed, __set_randomSeed)
	"""A property of a layer."""
	
	def __get_shadowDepth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_shadowDepth', __handle)

	def __set_shadowDepth(self, _shadowDepth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_shadowDepth', __handle, _shadowDepth)

	shadowDepth: float = property(__get_shadowDepth, __set_shadowDepth)
	"""A property of a layer."""
	
	def __get_shadowWidth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_shadowWidth', __handle)

	def __set_shadowWidth(self, _shadowWidth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_shadowWidth', __handle, _shadowWidth)

	shadowWidth: float = property(__get_shadowWidth, __set_shadowWidth)
	"""A property of a layer."""
	
	def __get_tileCount(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_tileCount', __handle)

	def __set_tileCount(self, _tileCount: int):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_tileCount', __handle, _tileCount)

	tileCount: int = property(__get_tileCount, __set_tileCount)
	"""A property of a layer."""
	
	def __get_tileDepth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_tileDepth', __handle)

	def __set_tileDepth(self, _tileDepth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_tileDepth', __handle, _tileDepth)

	tileDepth: float = property(__get_tileDepth, __set_tileDepth)
	"""A property of a layer."""
	
	def __get_tileHeight(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_tileHeight', __handle)

	def __set_tileHeight(self, _tileHeight: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_tileHeight', __handle, _tileHeight)

	tileHeight: float = property(__get_tileHeight, __set_tileHeight)
	"""A property of a layer."""
	
	def __get_tileOffset(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_tileOffset', __handle)

	def __set_tileOffset(self, _tileOffset: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_tileOffset', __handle, _tileOffset)

	tileOffset: float = property(__get_tileOffset, __set_tileOffset)
	"""A property of a layer."""
	
	def __get_tileWidth(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTiles.get_tileWidth', __handle)

	def __set_tileWidth(self, _tileWidth: float):
		return cur_server.exec('mset.TextureProjectLayerTiles.set_tileWidth', __handle, _tileWidth)

	tileWidth: float = property(__get_tileWidth, __set_tileWidth)
	"""A property of a layer."""
	

class TextureProjectLayerTurbulence(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_amplitude(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_amplitude', __handle)

	def __set_amplitude(self, _amplitude: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_amplitude', __handle, _amplitude)

	amplitude: float = property(__get_amplitude, __set_amplitude)
	"""A property of a layer."""
	
	def __get_frequency(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_frequency', __handle)

	def __set_frequency(self, _frequency: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_frequency', __handle, _frequency)

	frequency: float = property(__get_frequency, __set_frequency)
	"""A property of a layer."""
	
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_invert(self) -> bool:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_invert', __handle)

	def __set_invert(self, _invert: bool):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_invert', __handle, _invert)

	invert: bool = property(__get_invert, __set_invert)
	"""A property of a layer."""
	
	def __get_macroContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_macroContrast', __handle)

	def __set_macroContrast(self, _macroContrast: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_macroContrast', __handle, _macroContrast)

	macroContrast: float = property(__get_macroContrast, __set_macroContrast)
	"""A property of a layer."""
	
	def __get_macroWarpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_macroWarpAmount', __handle)

	def __set_macroWarpAmount(self, _macroWarpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_macroWarpAmount', __handle, _macroWarpAmount)

	macroWarpAmount: float = property(__get_macroWarpAmount, __set_macroWarpAmount)
	"""A property of a layer."""
	
	def __get_macroWarpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_macroWarpDetail', __handle)

	def __set_macroWarpDetail(self, _macroWarpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_macroWarpDetail', __handle, _macroWarpDetail)

	macroWarpDetail: float = property(__get_macroWarpDetail, __set_macroWarpDetail)
	"""A property of a layer."""
	
	def __get_microContrast(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_microContrast', __handle)

	def __set_microContrast(self, _microContrast: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_microContrast', __handle, _microContrast)

	microContrast: float = property(__get_microContrast, __set_microContrast)
	"""A property of a layer."""
	
	def __get_microWarpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_microWarpAmount', __handle)

	def __set_microWarpAmount(self, _microWarpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_microWarpAmount', __handle, _microWarpAmount)

	microWarpAmount: float = property(__get_microWarpAmount, __set_microWarpAmount)
	"""A property of a layer."""
	
	def __get_microWarpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_microWarpDetail', __handle)

	def __set_microWarpDetail(self, _microWarpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_microWarpDetail', __handle, _microWarpDetail)

	microWarpDetail: float = property(__get_microWarpDetail, __set_microWarpDetail)
	"""A property of a layer."""
	
	def __get_noisePasses(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_noisePasses', __handle)

	def __set_noisePasses(self, _noisePasses: int):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_noisePasses', __handle, _noisePasses)

	noisePasses: int = property(__get_noisePasses, __set_noisePasses)
	"""A property of a layer."""
	
	def __get_projection(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_projection', __handle)

	def __set_projection(self, _projection: Any):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_projection', __handle, _projection)

	projection: Any = property(__get_projection, __set_projection)
	"""A property of a layer."""
	
	def __get_scale(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_scale', __handle)

	def __set_scale(self, _scale: int):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_scale', __handle, _scale)

	scale: int = property(__get_scale, __set_scale)
	"""A property of a layer."""
	
	def __get_seed(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerTurbulence.get_seed', __handle)

	def __set_seed(self, _seed: int):
		return cur_server.exec('mset.TextureProjectLayerTurbulence.set_seed', __handle, _seed)

	seed: int = property(__get_seed, __set_seed)
	"""A property of a layer."""
	

class TextureProjectLayerVoronoi(TextureProjectLayer):
	"""
	A texture project layer. Used to configure a given layer.
	"""
	
	__handle = None
	def __get_intensity(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_intensity', __handle)

	def __set_intensity(self, _intensity: float):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_intensity', __handle, _intensity)

	intensity: float = property(__get_intensity, __set_intensity)
	"""A property of a layer."""
	
	def __get_jitter(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_jitter', __handle)

	def __set_jitter(self, _jitter: float):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_jitter', __handle, _jitter)

	jitter: float = property(__get_jitter, __set_jitter)
	"""A property of a layer."""
	
	def __get_phase(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_phase', __handle)

	def __set_phase(self, _phase: float):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_phase', __handle, _phase)

	phase: float = property(__get_phase, __set_phase)
	"""A property of a layer."""
	
	def __get_projection(self) -> Any:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_projection', __handle)

	def __set_projection(self, _projection: Any):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_projection', __handle, _projection)

	projection: Any = property(__get_projection, __set_projection)
	"""A property of a layer."""
	
	def __get_randomSeed(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_randomSeed', __handle)

	def __set_randomSeed(self, _randomSeed: int):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_randomSeed', __handle, _randomSeed)

	randomSeed: int = property(__get_randomSeed, __set_randomSeed)
	"""A property of a layer."""
	
	def __get_scale(self) -> int:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_scale', __handle)

	def __set_scale(self, _scale: int):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_scale', __handle, _scale)

	scale: int = property(__get_scale, __set_scale)
	"""A property of a layer."""
	
	def __get_smoothing(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_smoothing', __handle)

	def __set_smoothing(self, _smoothing: float):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_smoothing', __handle, _smoothing)

	smoothing: float = property(__get_smoothing, __set_smoothing)
	"""A property of a layer."""
	
	def __get_warpAmount(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_warpAmount', __handle)

	def __set_warpAmount(self, _warpAmount: float):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_warpAmount', __handle, _warpAmount)

	warpAmount: float = property(__get_warpAmount, __set_warpAmount)
	"""A property of a layer."""
	
	def __get_warpDetail(self) -> float:
		return cur_server.exec('mset.TextureProjectLayerVoronoi.get_warpDetail', __handle)

	def __set_warpDetail(self, _warpDetail: float):
		return cur_server.exec('mset.TextureProjectLayerVoronoi.set_warpDetail', __handle, _warpDetail)

	warpDetail: float = property(__get_warpDetail, __set_warpDetail)
	"""A property of a layer."""
	

class TextureProjectObject(SceneObject):
	"""
	Scene Object for Texture Projects.
	"""
	
	__handle = None
	def __get_bumpDetailWeight(self) -> float:
		return cur_server.exec('mset.TextureProjectObject.get_bumpDetailWeight', __handle)

	def __set_bumpDetailWeight(self, _bumpDetailWeight: float):
		return cur_server.exec('mset.TextureProjectObject.set_bumpDetailWeight', __handle, _bumpDetailWeight)

	bumpDetailWeight: float = property(__get_bumpDetailWeight, __set_bumpDetailWeight)
	"""The amount that bump maps contribute to normal details."""
	
	def __get_metalnessThresholdCenter(self) -> float:
		return cur_server.exec('mset.TextureProjectObject.get_metalnessThresholdCenter', __handle)

	def __set_metalnessThresholdCenter(self, _metalnessThresholdCenter: float):
		return cur_server.exec('mset.TextureProjectObject.set_metalnessThresholdCenter', __handle, _metalnessThresholdCenter)

	metalnessThresholdCenter: float = property(__get_metalnessThresholdCenter, __set_metalnessThresholdCenter)
	"""The center region where materials are defined as non-metal vs metal."""
	
	def __get_metalnessThresholdRange(self) -> float:
		return cur_server.exec('mset.TextureProjectObject.get_metalnessThresholdRange', __handle)

	def __set_metalnessThresholdRange(self, _metalnessThresholdRange: float):
		return cur_server.exec('mset.TextureProjectObject.set_metalnessThresholdRange', __handle, _metalnessThresholdRange)

	metalnessThresholdRange: float = property(__get_metalnessThresholdRange, __set_metalnessThresholdRange)
	"""The range of values that are interpolated between non-metal and metal."""
	
	def __get_outputHeight(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_outputHeight', __handle)

	def __set_outputHeight(self, _outputHeight: int):
		return cur_server.exec('mset.TextureProjectObject.set_outputHeight', __handle, _outputHeight)

	outputHeight: int = property(__get_outputHeight, __set_outputHeight)
	"""The height in pixels of exported texture project textures."""
	
	def __get_outputPath(self) -> str:
		return cur_server.exec('mset.TextureProjectObject.get_outputPath', __handle)

	def __set_outputPath(self, _outputPath: str):
		return cur_server.exec('mset.TextureProjectObject.set_outputPath', __handle, _outputPath)

	outputPath: str = property(__get_outputPath, __set_outputPath)
	"""The path of the texture project exports."""
	
	def __get_outputWidth(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_outputWidth', __handle)

	def __set_outputWidth(self, _outputWidth: int):
		return cur_server.exec('mset.TextureProjectObject.set_outputWidth', __handle, _outputWidth)

	outputWidth: int = property(__get_outputWidth, __set_outputWidth)
	"""The width in pixels of exported texture project textures."""
	
	def __get_paddingSize(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_paddingSize', __handle)

	def __set_paddingSize(self, _paddingSize: int):
		return cur_server.exec('mset.TextureProjectObject.set_paddingSize', __handle, _paddingSize)

	paddingSize: int = property(__get_paddingSize, __set_paddingSize)
	"""UV padding size in pixels."""
	
	def __get_previewUndersample(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_previewUndersample', __handle)

	def __set_previewUndersample(self, _previewUndersample: int):
		return cur_server.exec('mset.TextureProjectObject.set_previewUndersample', __handle, _previewUndersample)

	previewUndersample: int = property(__get_previewUndersample, __set_previewUndersample)
	"""The preview resolution undersampling scale, meant to improve performance at the cost of quality with the formula resolution / previewUndersample."""
	
	def __get_projectHeight(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_projectHeight', __handle)

	def __set_projectHeight(self, _projectHeight: int):
		return cur_server.exec('mset.TextureProjectObject.set_projectHeight', __handle, _projectHeight)

	projectHeight: int = property(__get_projectHeight, __set_projectHeight)
	"""The height in pixels of the texture project working resolution."""
	
	def __get_projectWidth(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_projectWidth', __handle)

	def __set_projectWidth(self, _projectWidth: int):
		return cur_server.exec('mset.TextureProjectObject.set_projectWidth', __handle, _projectWidth)

	projectWidth: int = property(__get_projectWidth, __set_projectWidth)
	"""The width in pixels of the texture project working resolution."""
	
	def __get_reflectionWorkflow(self) -> str:
		return cur_server.exec('mset.TextureProjectObject.get_reflectionWorkflow', __handle)

	def __set_reflectionWorkflow(self, _reflectionWorkflow: str):
		return cur_server.exec('mset.TextureProjectObject.set_reflectionWorkflow', __handle, _reflectionWorkflow)

	reflectionWorkflow: str = property(__get_reflectionWorkflow, __set_reflectionWorkflow)
	"""The current reflection workflow. Can be either 'metalness' or 'specular'"""
	
	def __get_useBumpAsDetailNormals(self) -> bool:
		return cur_server.exec('mset.TextureProjectObject.get_useBumpAsDetailNormals', __handle)

	def __set_useBumpAsDetailNormals(self, _useBumpAsDetailNormals: bool):
		return cur_server.exec('mset.TextureProjectObject.set_useBumpAsDetailNormals', __handle, _useBumpAsDetailNormals)

	useBumpAsDetailNormals: bool = property(__get_useBumpAsDetailNormals, __set_useBumpAsDetailNormals)
	"""Use bump channel as detail normals."""
	
	def __get_useHeightAsParallax(self) -> bool:
		return cur_server.exec('mset.TextureProjectObject.get_useHeightAsParallax', __handle)

	def __set_useHeightAsParallax(self, _useHeightAsParallax: bool):
		return cur_server.exec('mset.TextureProjectObject.set_useHeightAsParallax', __handle, _useHeightAsParallax)

	useHeightAsParallax: bool = property(__get_useHeightAsParallax, __set_useHeightAsParallax)
	"""Use height map in paralax subroutine with materials."""
	
	def __get_useThicknessAsScatter(self) -> bool:
		return cur_server.exec('mset.TextureProjectObject.get_useThicknessAsScatter', __handle)

	def __set_useThicknessAsScatter(self, _useThicknessAsScatter: bool):
		return cur_server.exec('mset.TextureProjectObject.set_useThicknessAsScatter', __handle, _useThicknessAsScatter)

	useThicknessAsScatter: bool = property(__get_useThicknessAsScatter, __set_useThicknessAsScatter)
	"""Use tickness as scatter subroutine with materials."""
	
	def __get_useUVPadding(self) -> bool:
		return cur_server.exec('mset.TextureProjectObject.get_useUVPadding', __handle)

	def __set_useUVPadding(self, _useUVPadding: bool):
		return cur_server.exec('mset.TextureProjectObject.set_useUVPadding', __handle, _useUVPadding)

	useUVPadding: bool = property(__get_useUVPadding, __set_useUVPadding)
	"""Whether to use UV padding when generating textures."""
	
	def __get_viewportQuality(self) -> str:
		return cur_server.exec('mset.TextureProjectObject.get_viewportQuality', __handle)

	def __set_viewportQuality(self, _viewportQuality: str):
		return cur_server.exec('mset.TextureProjectObject.set_viewportQuality', __handle, _viewportQuality)

	viewportQuality: str = property(__get_viewportQuality, __set_viewportQuality)
	"""The quality of the viewport, can be either 'Full' or 'Fast'."""
	
	def __get_viewportUndersample(self) -> int:
		return cur_server.exec('mset.TextureProjectObject.get_viewportUndersample', __handle)

	def __set_viewportUndersample(self, _viewportUndersample: int):
		return cur_server.exec('mset.TextureProjectObject.set_viewportUndersample', __handle, _viewportUndersample)

	viewportUndersample: int = property(__get_viewportUndersample, __set_viewportUndersample)
	"""The viewport resolution scale. meant to improve performance at the cost of quality with the formula resolution / previewUndersample."""
	
	def addDefaultProjectMaps(self):
		"""
		Convenience function, adds the default set of project maps (PBR Metalness + Normals, Occlusion, Bump) to this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.addDefaultProjectMaps', __handle)

	def addLayer(self, layerType: str) -> TextureProjectLayer:
		"""
		Add a layer to the top of this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.addLayer', __handle, layerType)

	def addLinkedMaterial(self, mat: Material):
		"""
		Add a linked material to this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.addLinkedMaterial', __handle, mat)

	def addOutputMap(self, suffix: str, type: str, format: str, rgb: str, a: str):
		"""
		Add a output map for this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.addOutputMap', __handle, suffix,type,format,rgb,a)

	def addProjectMap(self, name: str):
		"""
		Add a project map to this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.addProjectMap', __handle, name)

	def exportAllOutputMaps(self):
		"""
		Convenience function that exports all output maps for this painter project according to your export settings.
		"""
		return cur_server.exec('mset.TextureProjectObject.exportAllOutputMaps', __handle)

	def getActiveLayer(self) -> TextureProjectLayer:
		"""
		Gets the currently active layer selected in this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.getActiveLayer', __handle)

	def getAllLayerTypes(self) -> List[str]:
		"""
		Get all types of layers that can be created in a texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.getAllLayerTypes', __handle)

	def getAllLayers(self) -> List[TextureProjectLayer]:
		"""
		Get a list of all layers in this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.getAllLayers', __handle)

	def getAllProjectMaps(self) -> List[str]:
		"""
		Gets all project maps from this texture project to get/set any settings it might have.
		"""
		return cur_server.exec('mset.TextureProjectObject.getAllProjectMaps', __handle)

	def getInputMap(self, name: str) -> Texture:
		"""
		Sets an input map to this texture project to be used as base information during texture generation.
		"""
		return cur_server.exec('mset.TextureProjectObject.getInputMap', __handle, name)

	def getOutputMap(self, index: int) -> TextureProjectOutputMap:
		"""
		Get a outpu map coresponding to this index or name for this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.getOutputMap', __handle, index)

	def getOutputMapCount(self) -> int:
		"""
		Get the number of project maps in this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.getOutputMapCount', __handle)

	def getProjectMapFormat(self, name: str) -> str:
		"""
		Get the format of a given texture project map.
		"""
		return cur_server.exec('mset.TextureProjectObject.getProjectMapFormat', __handle, name)

	def getSelectedLayers(self) -> List[TextureProjectLayer]:
		"""
		Get a list of all selected layers in this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.getSelectedLayers', __handle)

	def recomposite(self):
		"""
		Rerender this texture project. Useful if you're having trouble seeing changes in your texture renders.
		"""
		return cur_server.exec('mset.TextureProjectObject.recomposite', __handle)

	def removeOutputMap(self, index: Union[int, TextureProjectOutputMap]):
		"""
		Remove a output map for this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.removeOutputMap', __handle, index)

	def removeProjectMap(self, name: str):
		"""
		Add a project map to this texture project.
		"""
		return cur_server.exec('mset.TextureProjectObject.removeProjectMap', __handle, name)

	def setInputMap(self, name: str, tex: Union[Texture, str]):
		"""
		Sets an input map to this texture project to be used as base information during texture generation.
		"""
		return cur_server.exec('mset.TextureProjectObject.setInputMap', __handle, name,tex)

	def setProjectMapFormat(self, name: str, format: str):
		"""
		Set the format of a given texture project map. Can be one of the following: 'RGB 8-bit (sRGB)', 'RGB 8-bit (Linear)', 'RGB 16-bit (sRGB)', 'RGB 16-bit (Linear)', 'Grayscale 8-bit (sRGB)', 'Grayscale 8-bit (Linear)', 'Grayscale 16-bit (sRGB)', 'Grayscale 16-bit (Linear)'
		"""
		return cur_server.exec('mset.TextureProjectObject.setProjectMapFormat', __handle, name,format)


class ThicknessBakerMap(BakerMap):
	"""
	Thickness Baker Map Settings
	"""
	
	__handle = None
	def __get_dither(self) -> bool:
		return cur_server.exec('mset.ThicknessBakerMap.get_dither', __handle)

	def __set_dither(self, _dither: bool):
		return cur_server.exec('mset.ThicknessBakerMap.set_dither', __handle, _dither)

	dither: bool = property(__get_dither, __set_dither)
	"""Determines whether this map output will be dithered."""
	
	def __get_rayCount(self) -> int:
		return cur_server.exec('mset.ThicknessBakerMap.get_rayCount', __handle)

	def __set_rayCount(self, _rayCount: int):
		return cur_server.exec('mset.ThicknessBakerMap.set_rayCount', __handle, _rayCount)

	rayCount: int = property(__get_rayCount, __set_rayCount)
	"""The number of rays used for thickness baking."""
	

class UIButton(UIControl):
	"""
	UIButton
	"""
	
	__handle = None
	def __get_frameless(self) -> bool:
		return cur_server.exec('mset.UIButton.get_frameless', __handle)

	def __set_frameless(self, _frameless: bool):
		return cur_server.exec('mset.UIButton.set_frameless', __handle, _frameless)

	frameless: bool = property(__get_frameless, __set_frameless)
	"""If the button has a frame."""
	
	def __get_lit(self) -> bool:
		return cur_server.exec('mset.UIButton.get_lit', __handle)

	def __set_lit(self, _lit: bool):
		return cur_server.exec('mset.UIButton.set_lit', __handle, _lit)

	lit: bool = property(__get_lit, __set_lit)
	"""If the button has a highlighted frame."""
	
	def __get_onClick(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIButton.get_onClick', __handle)

	def __set_onClick(self, _onClick: Callable[[], None]):
		return cur_server.exec('mset.UIButton.set_onClick', __handle, _onClick)

	onClick: Callable[[], None] = property(__get_onClick, __set_onClick)
	"""A callable, called when the button is clicked."""
	
	def __get_small(self) -> bool:
		return cur_server.exec('mset.UIButton.get_small', __handle)

	def __set_small(self, _small: bool):
		return cur_server.exec('mset.UIButton.set_small', __handle, _small)

	small: bool = property(__get_small, __set_small)
	"""If the button is small or not."""
	
	def __get_text(self) -> str:
		return cur_server.exec('mset.UIButton.get_text', __handle)

	def __set_text(self, _text: str):
		return cur_server.exec('mset.UIButton.set_text', __handle, _text)

	text: str = property(__get_text, __set_text)
	"""The text label of the button."""
	
	def setIcon(self, icon: str):
		"""
		Lets you set an image as the button icon.
		"""
		return cur_server.exec('mset.UIButton.setIcon', __handle, icon)

	def setIconPadding(self, left: float = 0, right: float = 0, top: float = 0, bottom: float = 0):
		"""
		Lets you set an image as the button icon.
		"""
		return cur_server.exec('mset.UIButton.setIconPadding', __handle, left,right,top,bottom)


class UICheckBox(UIControl):
	"""
	UICheckBox
	"""
	
	__handle = None
	def __get_label(self) -> str:
		return cur_server.exec('mset.UICheckBox.get_label', __handle)

	def __set_label(self, _label: str):
		return cur_server.exec('mset.UICheckBox.set_label', __handle, _label)

	label: str = property(__get_label, __set_label)
	"""The text label of the CheckBox."""
	
	def __get_onChange(self) -> Callable[[],None]:
		return cur_server.exec('mset.UICheckBox.get_onChange', __handle)

	def __set_onChange(self, _onChange: Callable[[], None]):
		return cur_server.exec('mset.UICheckBox.set_onChange', __handle, _onChange)

	onChange: Callable[[], None] = property(__get_onChange, __set_onChange)
	"""A callable, called when the CheckBox value is changed."""
	
	def __get_value(self) -> bool:
		return cur_server.exec('mset.UICheckBox.get_value', __handle)

	def __set_value(self, _value: bool):
		return cur_server.exec('mset.UICheckBox.set_value', __handle, _value)

	value: bool = property(__get_value, __set_value)
	"""The boolean value of the CheckBox."""
	

class UIColorPicker(UIControl):
	"""
	UIColorPicker
	"""
	
	__handle = None
	def __get_color(self) -> List[float]:
		return cur_server.exec('mset.UIColorPicker.get_color', __handle)

	def __set_color(self, _color: List[float]):
		return cur_server.exec('mset.UIColorPicker.set_color', __handle, _color)

	color: List[float] = property(__get_color, __set_color)
	"""The color of the color picker."""
	
	def __get_title(self) -> str:
		return cur_server.exec('mset.UIColorPicker.get_title', __handle)

	def __set_title(self, _title: str):
		return cur_server.exec('mset.UIColorPicker.set_title', __handle, _title)

	title: str = property(__get_title, __set_title)
	"""The text title of the color picker."""
	

class UIDrawer(UIControl):
	"""
	UIDrawer
	"""
	
	__handle = None
	def __get_containedControl(self) -> Control:
		return cur_server.exec('mset.UIDrawer.get_containedControl', __handle)

	def __set_containedControl(self, _containedControl: Control):
		return cur_server.exec('mset.UIDrawer.set_containedControl', __handle, _containedControl)

	containedControl: Control = property(__get_containedControl, __set_containedControl)
	"""The control contained by the drawer object, to which other elements may be added."""
	
	def __get_onOpenClose(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIDrawer.get_onOpenClose', __handle)

	def __set_onOpenClose(self, _onOpenClose: Callable[[], None]):
		return cur_server.exec('mset.UIDrawer.set_onOpenClose', __handle, _onOpenClose)

	onOpenClose: Callable[[], None] = property(__get_onOpenClose, __set_onOpenClose)
	"""A callable, called when opening/closing the drawer."""
	
	def __get_open(self) -> bool:
		return cur_server.exec('mset.UIDrawer.get_open', __handle)

	def __set_open(self, _open: bool):
		return cur_server.exec('mset.UIDrawer.set_open', __handle, _open)

	open: bool = property(__get_open, __set_open)
	"""The current open/closed state of the drawer."""
	
	def __get_title(self) -> str:
		return cur_server.exec('mset.UIDrawer.get_title', __handle)

	def __set_title(self, _title: str):
		return cur_server.exec('mset.UIDrawer.set_title', __handle, _title)

	title: str = property(__get_title, __set_title)
	"""The text title of the drawer."""
	
	def setMinor(self, minor: bool):
		"""
		Whether or not the drawer is dimmer.
		"""
		return cur_server.exec('mset.UIDrawer.setMinor', __handle, minor)


class UILabel(UIControl):
	"""
	UILabel
	"""
	
	__handle = None
	def __get_fixedWidth(self) -> float:
		return cur_server.exec('mset.UILabel.get_fixedWidth', __handle)

	def __set_fixedWidth(self, _fixedWidth: float):
		return cur_server.exec('mset.UILabel.set_fixedWidth', __handle, _fixedWidth)

	fixedWidth: float = property(__get_fixedWidth, __set_fixedWidth)
	"""The desired fixed width of the label."""
	
	def __get_text(self) -> str:
		return cur_server.exec('mset.UILabel.get_text', __handle)

	def __set_text(self, _text: str):
		return cur_server.exec('mset.UILabel.set_text', __handle, _text)

	text: str = property(__get_text, __set_text)
	"""The text of the label."""
	

class UIListBox(UIControl):
	"""
	UIListBox
	"""
	
	__handle = None
	def __get_onMenuOpen(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIListBox.get_onMenuOpen', __handle)

	def __set_onMenuOpen(self, _onMenuOpen: Callable[[], None]):
		return cur_server.exec('mset.UIListBox.set_onMenuOpen', __handle, _onMenuOpen)

	onMenuOpen: Callable[[], None] = property(__get_onMenuOpen, __set_onMenuOpen)
	"""A callable, called when opening the ListBox."""
	
	def __get_onSelect(self) -> Callable[[],None]:
		return cur_server.exec('mset.UIListBox.get_onSelect', __handle)

	def __set_onSelect(self, _onSelect: Callable[[], None]):
		return cur_server.exec('mset.UIListBox.set_onSelect', __handle, _onSelect)

	onSelect: Callable[[], None] = property(__get_onSelect, __set_onSelect)
	"""A callable, called when selecting an item in the ListBox."""
	
	def __get_selectedItem(self) -> int:
		return cur_server.exec('mset.UIListBox.get_selectedItem', __handle)

	def __set_selectedItem(self, _selectedItem: int):
		return cur_server.exec('mset.UIListBox.set_selectedItem', __handle, _selectedItem)

	selectedItem: int = property(__get_selectedItem, __set_selectedItem)
	"""The currently selected item in the ListBox."""
	
	def __get_title(self) -> str:
		return cur_server.exec('mset.UIListBox.get_title', __handle)

	def __set_title(self, _title: str):
		return cur_server.exec('mset.UIListBox.set_title', __handle, _title)

	title: str = property(__get_title, __set_title)
	"""The text title of the ListBox."""
	
	def addItem(self, item: str):
		"""
		Adds an item with the label specified to the ListBox.
		"""
		return cur_server.exec('mset.UIListBox.addItem', __handle, item)

	def clearItems(self):
		"""
		Removes all items from this ListBox.
		"""
		return cur_server.exec('mset.UIListBox.clearItems', __handle)

	def selectItemByName(self, name: str):
		"""
		Selects the item that matches the name specified.
		"""
		return cur_server.exec('mset.UIListBox.selectItemByName', __handle, name)

	def selectNone(self):
		"""
		Select no item on the list.
		"""
		return cur_server.exec('mset.UIListBox.selectNone', __handle)


class UIScrollBox(UIControl):
	"""
	UIScrollBox
	"""
	
	__handle = None
	def __get_containedControl(self) -> UIWindow:
		return cur_server.exec('mset.UIScrollBox.get_containedControl', __handle)

	def __set_containedControl(self, _containedControl: UIWindow):
		return cur_server.exec('mset.UIScrollBox.set_containedControl', __handle, _containedControl)

	containedControl: UIWindow = property(__get_containedControl, __set_containedControl)
	"""The control contained by the scrollbox object, to which other elements may be added."""
	

class UIWindow(UIControl):
	"""
	UIWindow
	"""
	
	__handle = None
	def __get_height(self) -> float:
		return cur_server.exec('mset.UIWindow.get_height', __handle)

	def __set_height(self, _height: float):
		return cur_server.exec('mset.UIWindow.set_height', __handle, _height)

	height: float = property(__get_height, __set_height)
	"""The height of the Window"""
	
	def __get_title(self) -> str:
		return cur_server.exec('mset.UIWindow.get_title', __handle)

	def __set_title(self, _title: str):
		return cur_server.exec('mset.UIWindow.set_title', __handle, _title)

	title: str = property(__get_title, __set_title)
	"""The title of the Window"""
	
	def __get_visible(self) -> bool:
		return cur_server.exec('mset.UIWindow.get_visible', __handle)

	def __set_visible(self, _visible: bool):
		return cur_server.exec('mset.UIWindow.set_visible', __handle, _visible)

	visible: bool = property(__get_visible, __set_visible)
	"""True if the Window is visible"""
	
	def __get_width(self) -> float:
		return cur_server.exec('mset.UIWindow.get_width', __handle)

	def __set_width(self, _width: float):
		return cur_server.exec('mset.UIWindow.set_width', __handle, _width)

	width: float = property(__get_width, __set_width)
	"""The width of the Window"""
	
	def addElement(self, child: UIControl):
		"""
		Adds a child control to the Window.
		"""
		return cur_server.exec('mset.UIWindow.addElement', __handle, child)

	def addReturn(self):
		"""
		Adds a line return to the window, placing all following elements on the next line
		"""
		return cur_server.exec('mset.UIWindow.addReturn', __handle)

	def addSpace(self, width: float):
		"""
		Adds a space of fixed width to the window, placing all following elements after it.
		"""
		return cur_server.exec('mset.UIWindow.addSpace', __handle, width)

	def addStretchSpace(self):
		"""
		Adds a stretchable space to the Window, placing all following elements after it at the end of the current line.
		"""
		return cur_server.exec('mset.UIWindow.addStretchSpace', __handle)

	def clearElements(self):
		"""
		Removes all elements from the window.
		"""
		return cur_server.exec('mset.UIWindow.clearElements', __handle)

	def close(self):
		"""
		Closes the current window.
		"""
		return cur_server.exec('mset.UIWindow.close', __handle)

	def getElements(self) -> List[UIControl]:
		"""
		Returns a list of all contained controls.
		"""
		return cur_server.exec('mset.UIWindow.getElements', __handle)


class UVIslandBakerMap(BakerMap):
	"""
	UVIsland Baker Map Settings
	"""
	
	__handle = None
	def __get_enableSVGUVIsland(self) -> bool:
		return cur_server.exec('mset.UVIslandBakerMap.get_enableSVGUVIsland', __handle)

	def __set_enableSVGUVIsland(self, _enableSVGUVIsland: bool):
		return cur_server.exec('mset.UVIslandBakerMap.set_enableSVGUVIsland', __handle, _enableSVGUVIsland)

	enableSVGUVIsland: bool = property(__get_enableSVGUVIsland, __set_enableSVGUVIsland)
	"""Enables the exporting of an SVG version of the UV Island map."""
	

class WireframeBakerMap(BakerMap):
	"""
	Wireframe Baker Map Settings
	"""
	
	__handle = None
	def __get_lineThickness(self) -> float:
		return cur_server.exec('mset.WireframeBakerMap.get_lineThickness', __handle)

	def __set_lineThickness(self, _lineThickness: float):
		return cur_server.exec('mset.WireframeBakerMap.set_lineThickness', __handle, _lineThickness)

	lineThickness: float = property(__get_lineThickness, __set_lineThickness)
	"""The thickness of the UV wireframe lines."""
	
	def __get_vertexRadius(self) -> float:
		return cur_server.exec('mset.WireframeBakerMap.get_vertexRadius', __handle)

	def __set_vertexRadius(self, _vertexRadius: float):
		return cur_server.exec('mset.WireframeBakerMap.set_vertexRadius', __handle, _vertexRadius)

	vertexRadius: float = property(__get_vertexRadius, __set_vertexRadius)
	"""The radius of each vertex of the UV wireframe."""
	
	def __get_wireframeColor(self) -> List[float]:
		return cur_server.exec('mset.WireframeBakerMap.get_wireframeColor', __handle)

	def __set_wireframeColor(self, _wireframeColor: List[float]):
		return cur_server.exec('mset.WireframeBakerMap.set_wireframeColor', __handle, _wireframeColor)

	wireframeColor: List[float] = property(__get_wireframeColor, __set_wireframeColor)
	"""Wireframe color as an RGB array."""
	

class CameraObject(TransformObject, SceneObject):
	"""
	Camera Object
	"""
	
	__handle = None
	def __get_focalLength(self) -> float:
		return cur_server.exec('mset.CameraObject.get_focalLength', __handle)

	def __set_focalLength(self, _focalLength: float):
		return cur_server.exec('mset.CameraObject.set_focalLength', __handle, _focalLength)

	focalLength: float = property(__get_focalLength, __set_focalLength)
	"""The focal length of the camera, in mm."""
	
	def __get_fov(self) -> float:
		return cur_server.exec('mset.CameraObject.get_fov', __handle)

	def __set_fov(self, _fov: float):
		return cur_server.exec('mset.CameraObject.set_fov', __handle, _fov)

	fov: float = property(__get_fov, __set_fov)
	"""The vertical field of view of the camera, in degrees."""
	
	def __get_lens(self) -> CameraLens:
		return cur_server.exec('mset.CameraObject.get_lens', __handle)

	def __set_lens(self, _lens: CameraLens):
		return cur_server.exec('mset.CameraObject.set_lens', __handle, _lens)

	lens: CameraLens = property(__get_lens, __set_lens)
	"""The camera lens settings."""
	
	def __get_limits(self) -> CameraLimits:
		return cur_server.exec('mset.CameraObject.get_limits', __handle)

	def __set_limits(self, _limits: CameraLimits):
		return cur_server.exec('mset.CameraObject.set_limits', __handle, _limits)

	limits: CameraLimits = property(__get_limits, __set_limits)
	"""The camera limits settings."""
	
	def __get_mode(self) -> str:
		return cur_server.exec('mset.CameraObject.get_mode', __handle)

	def __set_mode(self, _mode: str):
		return cur_server.exec('mset.CameraObject.set_mode', __handle, _mode)

	mode: str = property(__get_mode, __set_mode)
	"""The mode of this camera, can be 'perspective' or 'orthographic'."""
	
	def __get_nearPlaneScale(self) -> float:
		return cur_server.exec('mset.CameraObject.get_nearPlaneScale', __handle)

	def __set_nearPlaneScale(self, _nearPlaneScale: float):
		return cur_server.exec('mset.CameraObject.set_nearPlaneScale', __handle, _nearPlaneScale)

	nearPlaneScale: float = property(__get_nearPlaneScale, __set_nearPlaneScale)
	"""A scalar for adjusting the automatic near clipping plane. Lower values will bring the clipping closer to the camera, but can result in unstable depth for the rest of the scene."""
	
	def __get_orthoScale(self) -> float:
		return cur_server.exec('mset.CameraObject.get_orthoScale', __handle)

	def __set_orthoScale(self, _orthoScale: float):
		return cur_server.exec('mset.CameraObject.set_orthoScale', __handle, _orthoScale)

	orthoScale: float = property(__get_orthoScale, __set_orthoScale)
	"""The scale of this camera in orthographic mode. Measured in scene units."""
	
	def __get_postEffect(self) -> CameraPostEffect:
		return cur_server.exec('mset.CameraObject.get_postEffect', __handle)

	def __set_postEffect(self, _postEffect: CameraPostEffect):
		return cur_server.exec('mset.CameraObject.set_postEffect', __handle, _postEffect)

	postEffect: CameraPostEffect = property(__get_postEffect, __set_postEffect)
	"""The camera post effect settings."""
	
	def loadPostEffect(self, path: str):
		"""
		Load a camera post effect from a file.
		"""
		return cur_server.exec('mset.CameraObject.loadPostEffect', __handle, path)

	def savePostEffect(self, path: str):
		"""
		Save a camera post effect to a file.
		"""
		return cur_server.exec('mset.CameraObject.savePostEffect', __handle, path)


class ExternalObject(TransformObject, SceneObject):
	"""
	External Object
	"""
	
	__handle = None
	def __get_path(self) -> str:
		return cur_server.exec('mset.ExternalObject.get_path', __handle)

	def __set_path(self, _path: str):
		return cur_server.exec('mset.ExternalObject.set_path', __handle, _path)

	path: str = property(__get_path, __set_path)
	"""Path to a model file. If this path is altered, a new model will be loaded in place of the old one."""
	

class LightObject(TransformObject, SceneObject):
	"""
	Light Object
	"""
	
	__handle = None
	def __get_brightness(self) -> float:
		return cur_server.exec('mset.LightObject.get_brightness', __handle)

	def __set_brightness(self, _brightness: float):
		return cur_server.exec('mset.LightObject.set_brightness', __handle, _brightness)

	brightness: float = property(__get_brightness, __set_brightness)
	"""The brightness of the light."""
	
	def __get_castShadows(self) -> bool:
		return cur_server.exec('mset.LightObject.get_castShadows', __handle)

	def __set_castShadows(self, _castShadows: bool):
		return cur_server.exec('mset.LightObject.set_castShadows', __handle, _castShadows)

	castShadows: bool = property(__get_castShadows, __set_castShadows)
	"""Enables the casting of shadows by the light."""
	
	def __get_color(self) -> List[float]:
		return cur_server.exec('mset.LightObject.get_color', __handle)

	def __set_color(self, _color: List[float]):
		return cur_server.exec('mset.LightObject.set_color', __handle, _color)

	color: List[float] = property(__get_color, __set_color)
	"""The color of the light."""
	
	def __get_gelPath(self) -> str:
		return cur_server.exec('mset.LightObject.get_gelPath', __handle)

	def __set_gelPath(self, _gelPath: str):
		return cur_server.exec('mset.LightObject.set_gelPath', __handle, _gelPath)

	gelPath: str = property(__get_gelPath, __set_gelPath)
	"""Path of image to mask light shape."""
	
	def __get_gelTile(self) -> float:
		return cur_server.exec('mset.LightObject.get_gelTile', __handle)

	def __set_gelTile(self, _gelTile: float):
		return cur_server.exec('mset.LightObject.set_gelTile', __handle, _gelTile)

	gelTile: float = property(__get_gelTile, __set_gelTile)
	"""Tiling scalar for the gel texture."""
	
	def __get_lengthX(self) -> float:
		return cur_server.exec('mset.LightObject.get_lengthX', __handle)

	def __set_lengthX(self, _lengthX: float):
		return cur_server.exec('mset.LightObject.set_lengthX', __handle, _lengthX)

	lengthX: float = property(__get_lengthX, __set_lengthX)
	"""The length along the X axis of the light source."""
	
	def __get_lengthY(self) -> float:
		return cur_server.exec('mset.LightObject.get_lengthY', __handle)

	def __set_lengthY(self, _lengthY: float):
		return cur_server.exec('mset.LightObject.set_lengthY', __handle, _lengthY)

	lengthY: float = property(__get_lengthY, __set_lengthY)
	"""The length along the Y axis of the light source."""
	
	def __get_lightType(self) -> str:
		return cur_server.exec('mset.LightObject.get_lightType', __handle)

	def __set_lightType(self, _lightType: str):
		return cur_server.exec('mset.LightObject.set_lightType', __handle, _lightType)

	lightType: str = property(__get_lightType, __set_lightType)
	"""The type of the light (valid values are 'directional', 'spot', 'omni'"""
	
	def __get_spotAngle(self) -> float:
		return cur_server.exec('mset.LightObject.get_spotAngle', __handle)

	def __set_spotAngle(self, _spotAngle: float):
		return cur_server.exec('mset.LightObject.set_spotAngle', __handle, _spotAngle)

	spotAngle: float = property(__get_spotAngle, __set_spotAngle)
	"""The spot angle, in degrees, for use by spot lights only."""
	
	def __get_spotSharpness(self) -> float:
		return cur_server.exec('mset.LightObject.get_spotSharpness', __handle)

	def __set_spotSharpness(self, _spotSharpness: float):
		return cur_server.exec('mset.LightObject.set_spotSharpness', __handle, _spotSharpness)

	spotSharpness: float = property(__get_spotSharpness, __set_spotSharpness)
	"""The sharpness of the spotlight shape, for use by spot lights only."""
	
	def __get_spotVignette(self) -> float:
		return cur_server.exec('mset.LightObject.get_spotVignette', __handle)

	def __set_spotVignette(self, _spotVignette: float):
		return cur_server.exec('mset.LightObject.set_spotVignette', __handle, _spotVignette)

	spotVignette: float = property(__get_spotVignette, __set_spotVignette)
	"""The degree of spotlight vignette, for use by spot lights only."""
	
	def __get_visibleShape(self) -> bool:
		return cur_server.exec('mset.LightObject.get_visibleShape', __handle)

	def __set_visibleShape(self, _visibleShape: bool):
		return cur_server.exec('mset.LightObject.set_visibleShape', __handle, _visibleShape)

	visibleShape: bool = property(__get_visibleShape, __set_visibleShape)
	"""Makes the light source shape visible in final renders."""
	
	def __get_width(self) -> float:
		return cur_server.exec('mset.LightObject.get_width', __handle)

	def __set_width(self, _width: float):
		return cur_server.exec('mset.LightObject.set_width', __handle, _width)

	width: float = property(__get_width, __set_width)
	"""The radius of the light source."""
	

class MeshObject(TransformObject, SceneObject):
	"""
	Mesh Object
	"""
	
	__handle = None
	def __get_castShadows(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_castShadows', __handle)

	def __set_castShadows(self, _castShadows: bool):
		return cur_server.exec('mset.MeshObject.set_castShadows', __handle, _castShadows)

	castShadows: bool = property(__get_castShadows, __set_castShadows)
	"""Enables casting of shadows from the mesh."""
	
	def __get_cullBackFaces(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_cullBackFaces', __handle)

	def __set_cullBackFaces(self, _cullBackFaces: bool):
		return cur_server.exec('mset.MeshObject.set_cullBackFaces', __handle, _cullBackFaces)

	cullBackFaces: bool = property(__get_cullBackFaces, __set_cullBackFaces)
	"""Enables the culling of back faces during render."""
	
	def __get_fixMirroredTangents(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_fixMirroredTangents', __handle)

	def __set_fixMirroredTangents(self, _fixMirroredTangents: bool):
		return cur_server.exec('mset.MeshObject.set_fixMirroredTangents', __handle, _fixMirroredTangents)

	fixMirroredTangents: bool = property(__get_fixMirroredTangents, __set_fixMirroredTangents)
	"""Fix tangent issues that arise with mirrored UVs in certain tangent spaces."""
	
	def __get_invisibleToCamera(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_invisibleToCamera', __handle)

	def __set_invisibleToCamera(self, _invisibleToCamera: bool):
		return cur_server.exec('mset.MeshObject.set_invisibleToCamera', __handle, _invisibleToCamera)

	invisibleToCamera: bool = property(__get_invisibleToCamera, __set_invisibleToCamera)
	"""If this object isn't visible to the camera. Useful for emissive surfaces you may want hidden."""
	
	def __get_mesh(self) -> Mesh:
		return cur_server.exec('mset.MeshObject.get_mesh', __handle)

	def __set_mesh(self, _mesh: Mesh):
		return cur_server.exec('mset.MeshObject.set_mesh', __handle, _mesh)

	mesh: Mesh = property(__get_mesh, __set_mesh)
	"""The mesh containing vertex data."""
	
	def __get_subdivisionEnabled(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_subdivisionEnabled', __handle)

	def __set_subdivisionEnabled(self, _subdivisionEnabled: bool):
		return cur_server.exec('mset.MeshObject.set_subdivisionEnabled', __handle, _subdivisionEnabled)

	subdivisionEnabled: bool = property(__get_subdivisionEnabled, __set_subdivisionEnabled)
	"""If subdivisions are enabled or not."""
	
	def __get_subdivisionGeometryReduction(self) -> str:
		return cur_server.exec('mset.MeshObject.get_subdivisionGeometryReduction', __handle)

	def __set_subdivisionGeometryReduction(self, _subdivisionGeometryReduction: str):
		return cur_server.exec('mset.MeshObject.set_subdivisionGeometryReduction', __handle, _subdivisionGeometryReduction)

	subdivisionGeometryReduction: str = property(__get_subdivisionGeometryReduction, __set_subdivisionGeometryReduction)
	"""The level of geometry decimation that should be done while subdividing. Helps with real time performance."""
	
	def __get_subdivisionLevel(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_subdivisionLevel', __handle)

	def __set_subdivisionLevel(self, _subdivisionLevel: bool):
		return cur_server.exec('mset.MeshObject.set_subdivisionLevel', __handle, _subdivisionLevel)

	subdivisionLevel: bool = property(__get_subdivisionLevel, __set_subdivisionLevel)
	"""If this object isn't visible to the camera. Useful for emissive surfaces you may want hidden."""
	
	def __get_subdivisionMode(self) -> str:
		return cur_server.exec('mset.MeshObject.get_subdivisionMode', __handle)

	def __set_subdivisionMode(self, _subdivisionMode: str):
		return cur_server.exec('mset.MeshObject.set_subdivisionMode', __handle, _subdivisionMode)

	subdivisionMode: str = property(__get_subdivisionMode, __set_subdivisionMode)
	"""The method used for subdivision. Can be 'Catmull-Clark', 'Regular', or 'PN Triangles'."""
	
	def __get_subdivisionSharpenCorners(self) -> bool:
		return cur_server.exec('mset.MeshObject.get_subdivisionSharpenCorners', __handle)

	def __set_subdivisionSharpenCorners(self, _subdivisionSharpenCorners: bool):
		return cur_server.exec('mset.MeshObject.set_subdivisionSharpenCorners', __handle, _subdivisionSharpenCorners)

	subdivisionSharpenCorners: bool = property(__get_subdivisionSharpenCorners, __set_subdivisionSharpenCorners)
	"""If corners should be sharp when subdividing. Helps keep the shape of your mesh with catmull-clark subdivisions."""
	
	def __get_subdivisionSmoothing(self) -> float:
		return cur_server.exec('mset.MeshObject.get_subdivisionSmoothing', __handle)

	def __set_subdivisionSmoothing(self, _subdivisionSmoothing: float):
		return cur_server.exec('mset.MeshObject.set_subdivisionSmoothing', __handle, _subdivisionSmoothing)

	subdivisionSmoothing: float = property(__get_subdivisionSmoothing, __set_subdivisionSmoothing)
	"""The level of smoothing that should be done with PN Triangle subdivision."""
	
	def __get_subdivisionWireframeMode(self) -> str:
		return cur_server.exec('mset.MeshObject.get_subdivisionWireframeMode', __handle)

	def __set_subdivisionWireframeMode(self, _subdivisionWireframeMode: str):
		return cur_server.exec('mset.MeshObject.set_subdivisionWireframeMode', __handle, _subdivisionWireframeMode)

	subdivisionWireframeMode: str = property(__get_subdivisionWireframeMode, __set_subdivisionWireframeMode)
	"""How wireframes should look with subdivisions. Can be 'Isolines' or 'Polygons'."""
	
	def __get_tangentSpace(self) -> str:
		return cur_server.exec('mset.MeshObject.get_tangentSpace', __handle)

	def __set_tangentSpace(self, _tangentSpace: str):
		return cur_server.exec('mset.MeshObject.set_tangentSpace', __handle, _tangentSpace)

	tangentSpace: str = property(__get_tangentSpace, __set_tangentSpace)
	"""Mesh tangent space for normal mapping. This must be one of the following values: 'Custom' 'Marmoset', 'Mikk', 'Maya', '3D Studio Max', 'Unity'"""
	
	def addSubmesh(self, name: str, material: Material = sys.stdin, startIndex: int = 0, indexCount: int = -1):
		"""
		addSubmesh(name: str, material: mset.Material = None, startIndex: int = 0, indexCount: int = -1)Adds and returns a SubMeshObject to the MeshObject, rendering the specified range of indices.name: Name of the SubMeshObjectmaterial: The Material assigned to the submesh.startIndex: The index of the first vertex of the submesh.indexCount: The number of indices following 'startIndex', or -1 to cover all remaining indices in the mesh.
		"""
		return cur_server.exec('mset.MeshObject.addSubmesh', __handle, name,material,startIndex,indexCount)


class PyTurntableObject(TransformObject, SceneObject):
	"""
	Turntable Object
	"""
	
	__handle = None
	def __get_enabled(self) -> bool:
		return cur_server.exec('mset.PyTurntableObject.get_enabled', __handle)

	def __set_enabled(self, _enabled: bool):
		return cur_server.exec('mset.PyTurntableObject.set_enabled', __handle, _enabled)

	enabled: bool = property(__get_enabled, __set_enabled)
	"""Enables the active motion of the turntable object."""
	
	def __get_spinRate(self) -> float:
		return cur_server.exec('mset.PyTurntableObject.get_spinRate', __handle)

	def __set_spinRate(self, _spinRate: float):
		return cur_server.exec('mset.PyTurntableObject.set_spinRate', __handle, _spinRate)

	spinRate: float = property(__get_spinRate, __set_spinRate)
	"""The rate at which the turntable object rotates, in degrees per second."""
	

class ShadowCatcherObject(TransformObject, SceneObject):
	"""
	Shadow Catcher Object
	"""
	
	__handle = None
	def __get_edgeFade(self) -> bool:
		return cur_server.exec('mset.ShadowCatcherObject.get_edgeFade', __handle)

	def __set_edgeFade(self, _edgeFade: bool):
		return cur_server.exec('mset.ShadowCatcherObject.set_edgeFade', __handle, _edgeFade)

	edgeFade: bool = property(__get_edgeFade, __set_edgeFade)
	"""Enables a fading of shadow opacity towards the edges of the shadow catcher plane."""
	
	def __get_fadeTexturePath(self) -> str:
		return cur_server.exec('mset.ShadowCatcherObject.get_fadeTexturePath', __handle)

	def __set_fadeTexturePath(self, _fadeTexturePath: str):
		return cur_server.exec('mset.ShadowCatcherObject.set_fadeTexturePath', __handle, _fadeTexturePath)

	fadeTexturePath: str = property(__get_fadeTexturePath, __set_fadeTexturePath)
	"""File path of the fade texture, which is used to control the shadow fade pattern."""
	
	def __get_opacity(self) -> float:
		return cur_server.exec('mset.ShadowCatcherObject.get_opacity', __handle)

	def __set_opacity(self, _opacity: float):
		return cur_server.exec('mset.ShadowCatcherObject.set_opacity', __handle, _opacity)

	opacity: float = property(__get_opacity, __set_opacity)
	"""The opacity of the shadow catcher."""
	
	def __get_skyShadow(self) -> bool:
		return cur_server.exec('mset.ShadowCatcherObject.get_skyShadow', __handle)

	def __set_skyShadow(self, _skyShadow: bool):
		return cur_server.exec('mset.ShadowCatcherObject.set_skyShadow', __handle, _skyShadow)

	skyShadow: bool = property(__get_skyShadow, __set_skyShadow)
	"""Enables receiving shadow from the sky light (ray tracing only)."""
	
	def __get_textureChannel(self) -> str:
		return cur_server.exec('mset.ShadowCatcherObject.get_textureChannel', __handle)

	def __set_textureChannel(self, _textureChannel: str):
		return cur_server.exec('mset.ShadowCatcherObject.set_textureChannel', __handle, _textureChannel)

	textureChannel: str = property(__get_textureChannel, __set_textureChannel)
	"""The active channel in the fade texture (must be one of: 'R', 'G', 'B', 'A')."""
	

class UISliderFloat(UIBaseSlider, UIControl):
	"""
	UI slider that exclusively works with float values.
	"""
	
	__handle = None
	def __get_logScale(self) -> float:
		return cur_server.exec('mset.UISliderFloat.get_logScale', __handle)

	def __set_logScale(self, _logScale: float):
		return cur_server.exec('mset.UISliderFloat.set_logScale', __handle, _logScale)

	logScale: float = property(__get_logScale, __set_logScale)
	"""The logarithmic exponent scale of the slider."""
	
	def __get_logScaleCenter(self) -> float:
		return cur_server.exec('mset.UISliderFloat.get_logScaleCenter', __handle)

	def __set_logScaleCenter(self, _logScaleCenter: float):
		return cur_server.exec('mset.UISliderFloat.set_logScaleCenter', __handle, _logScaleCenter)

	logScaleCenter: float = property(__get_logScaleCenter, __set_logScaleCenter)
	"""The center of the logarithmic scale of the slider."""
	
	def __get_max(self) -> float:
		return cur_server.exec('mset.UISliderFloat.get_max', __handle)

	def __set_max(self, _max: float):
		return cur_server.exec('mset.UISliderFloat.set_max', __handle, _max)

	max: float = property(__get_max, __set_max)
	"""The maximum of the slider range."""
	
	def __get_min(self) -> float:
		return cur_server.exec('mset.UISliderFloat.get_min', __handle)

	def __set_min(self, _min: float):
		return cur_server.exec('mset.UISliderFloat.set_min', __handle, _min)

	min: float = property(__get_min, __set_min)
	"""The minimum of the slider range."""
	
	def __get_value(self) -> float:
		return cur_server.exec('mset.UISliderFloat.get_value', __handle)

	def __set_value(self, _value: float):
		return cur_server.exec('mset.UISliderFloat.set_value', __handle, _value)

	value: float = property(__get_value, __set_value)
	"""The value of the slider."""
	

class UISliderInt(UIBaseSlider, UIControl):
	"""
	UI slider that exclusively works with int values.
	"""
	
	__handle = None
	def __get_logScale(self) -> int:
		return cur_server.exec('mset.UISliderInt.get_logScale', __handle)

	def __set_logScale(self, _logScale: int):
		return cur_server.exec('mset.UISliderInt.set_logScale', __handle, _logScale)

	logScale: int = property(__get_logScale, __set_logScale)
	"""The logarithmic exponent of the slider."""
	
	def __get_logScaleCenter(self) -> int:
		return cur_server.exec('mset.UISliderInt.get_logScaleCenter', __handle)

	def __set_logScaleCenter(self, _logScaleCenter: int):
		return cur_server.exec('mset.UISliderInt.set_logScaleCenter', __handle, _logScaleCenter)

	logScaleCenter: int = property(__get_logScaleCenter, __set_logScaleCenter)
	"""The center of the logarithmic scale of the slider."""
	
	def __get_max(self) -> int:
		return cur_server.exec('mset.UISliderInt.get_max', __handle)

	def __set_max(self, _max: int):
		return cur_server.exec('mset.UISliderInt.set_max', __handle, _max)

	max: int = property(__get_max, __set_max)
	"""The maximum value of the slider range."""
	
	def __get_min(self) -> int:
		return cur_server.exec('mset.UISliderInt.get_min', __handle)

	def __set_min(self, _min: int):
		return cur_server.exec('mset.UISliderInt.set_min', __handle, _min)

	min: int = property(__get_min, __set_min)
	"""The minimum value of the slider range."""
	
	def __get_value(self) -> int:
		return cur_server.exec('mset.UISliderInt.get_value', __handle)

	def __set_value(self, _value: int):
		return cur_server.exec('mset.UISliderInt.set_value', __handle, _value)

	value: int = property(__get_value, __set_value)
	"""The value of the slider."""
	

class UITextField(UIBaseTextField, UIControl):
	"""
	UI text field, useful for entering in text data.
	"""
	
	__handle = None
	def __get_value(self) -> str:
		return cur_server.exec('mset.UITextField.get_value', __handle)

	def __set_value(self, _value: str):
		return cur_server.exec('mset.UITextField.set_value', __handle, _value)

	value: str = property(__get_value, __set_value)
	"""The contents of the text field."""
	

class UITextFieldFloat(UIBaseTextField, UIControl):
	"""
	UI text field that exclusively works with floating point values.
	"""
	
	__handle = None
	def __get_value(self) -> float:
		return cur_server.exec('mset.UITextFieldFloat.get_value', __handle)

	def __set_value(self, _value: float):
		return cur_server.exec('mset.UITextFieldFloat.set_value', __handle, _value)

	value: float = property(__get_value, __set_value)
	"""The numerical value of the text field."""
	

class UITextFieldInt(UIBaseTextField, UIControl):
	"""
	UI text field that exclusively works with int values.
	"""
	
	__handle = None
	def __get_value(self) -> int:
		return cur_server.exec('mset.UITextFieldInt.get_value', __handle)

	def __set_value(self, _value: int):
		return cur_server.exec('mset.UITextFieldInt.set_value', __handle, _value)

	value: int = property(__get_value, __set_value)
	"""The numerical value of the text field."""
	

def bakeAll():
	"""
	Bakes all objects in the scene.
	"""
	return cur_server.exec('mset.bakeAll', __handle)

def compressFile(filePath: str, archiveOutputPath: str):
	"""
	Compresses a file on disk into a gzipped tarball archive (tgz).
	"""
	return cur_server.exec('mset.compressFile', __handle, filePath,archiveOutputPath)

def compressFolder(folderPath: str, archiveOutputPath: str):
	"""
	Compresses a folder, including all subdirectories, into a gzipped tarball archive (tgz).
	"""
	return cur_server.exec('mset.compressFolder', __handle, folderPath,archiveOutputPath)

def err(msg: str):
	"""
	Prints text to the application log, as an error. No return will be appended.
	"""
	return cur_server.exec('mset.err', __handle, msg)

def exportGLTF(path: str = '', quality: int = 3, metalnessThreshold: float = 0.8):
	"""
	Exports a WebGL-ready glTF (.glb) archive. This file will be written to the file path specified, or to the scene's default location if no path is specified. Texture quality is set from 0 to 3, with 3 being the highest. The specular metalness conversion threshold is a value above which materials will be converted to metalness.
	"""
	return cur_server.exec('mset.exportGLTF', __handle, path,quality,metalnessThreshold)

def exportViewer(path: str = '', title: str = '', author: str = '', authorURL: str = '', textureQuality: str = 'high', highResThumbnail: bool = False, html: bool = False, autoStartHTML: bool = False, fullframeHTML=False, presetHTML: bool = False, width: int = -1, height: int = -1, exportAnimations: bool = False, exportModelShowcase: bool = False, autoPlayAnimations: bool = False, showPlaybackControls: bool = False):
	"""
	Exports a Marmoset Viewer (.mview) archive. This file will be written to the file path specified, or to the scene's default location if no path is specified.
	"""
	return cur_server.exec('mset.exportViewer', __handle, path,title,author,authorURL,textureQuality,highResThumbnail,html,autoStartHTML,fullframeHTML,presetHTML,width,height,exportAnimations,exportModelShowcase,autoPlayAnimations,showPlaybackControls)

def fail(msg: str):
	"""
	Generates a failure message to an automated testing log. Mainly for internal use.
	"""
	return cur_server.exec('mset.fail', __handle, msg)

def findMaterial(name: str) -> Material:
	"""
	Finds a Material by string name.
	"""
	return cur_server.exec('mset.findMaterial', __handle, name)

def findObject(searchString: str):
	"""
	Finds an Object in the scene by string name.
	"""
	return cur_server.exec('mset.findObject', __handle, searchString)

def frameObject(object: SceneObject):
	"""
	Centers and frames the given object in the current camera.
	"""
	return cur_server.exec('mset.frameObject', __handle, object)

def frameScene():
	"""
	Centers and frames the entire scene in the current camera.
	"""
	return cur_server.exec('mset.frameScene', __handle)

def freeUnusedResources():
	"""
	Frees from memory any retained but unused resources (such as textures). Generally this function is unnecessary, but it can be useful to keep total memory use lower in scripts that batch process large numbers of resources. Called automatically whenever a new scene is created or loaded.
	"""
	return cur_server.exec('mset.freeUnusedResources', __handle)

def getAllMaterials() -> List[Material]:
	"""
	Returns all materials as a list.
	"""
	return cur_server.exec('mset.getAllMaterials', __handle)

def getAllObjects() -> List[SceneObject]:
	"""
	Returns all scene Objects as a list.
	"""
	return cur_server.exec('mset.getAllObjects', __handle)

def getLibrary() -> Library:
	"""
	Returns your current installation's library. Used to configure your library with custom assets.
	"""
	return cur_server.exec('mset.getLibrary', __handle)

def getPluginPath() -> str:
	"""
	Returns the current plugin path (eg. "C:/Program Files/Marmoset Toolbag 4/data/plugins/Example.py").
	"""
	return cur_server.exec('mset.getPluginPath', __handle)

def getSceneBounds() -> List[List[float]]:
	"""
	Gets the bounds of the entire scene. Formatted as [min_xyz, max_xyz]
	"""
	return cur_server.exec('mset.getSceneBounds', __handle)

def getScenePath() -> str:
	"""
	Returns the path of the current scene file.
	"""
	return cur_server.exec('mset.getScenePath', __handle)

def getSceneUnitScale() -> float:
	"""
	Returns the current unit size of the scene, in meters. For example, a scene working in centimeters will return 0.01.
	"""
	return cur_server.exec('mset.getSceneUnitScale', __handle)

def getSelectedMaterial() -> Material:
	"""
	Returns the currently selected Material.
	"""
	return cur_server.exec('mset.getSelectedMaterial', __handle)

def getSelectedMaterialGroup() -> List[Material]:
	"""
	Returns the currently selected Material group as an array of materials.
	"""
	return cur_server.exec('mset.getSelectedMaterialGroup', __handle)

def getSelectedObject() -> SceneObject:
	"""
	Returns the currently selected Object. If multiple objects are selected this function will return the first selection. See also 'getSelectedObjects'.
	"""
	return cur_server.exec('mset.getSelectedObject', __handle)

def getSelectedObjects() -> List[SceneObject]:
	"""
	Returns all currently selected scene Objects as a list.
	"""
	return cur_server.exec('mset.getSelectedObjects', __handle)

def getStoreItem(key: str) -> Any:
	"""
	Get data in a shared persistent store that is accessable across plugins.
	"""
	return cur_server.exec('mset.getStoreItem', __handle, key)

def getTimeline() -> Timeline:
	"""
	Returns the current scene's timeline, for animation control.
	"""
	return cur_server.exec('mset.getTimeline', __handle)

def getToolbagVersion() -> int:
	"""
	Returns the current toolbag version, as an integer (e.g. 4033).
	"""
	return cur_server.exec('mset.getToolbagVersion', __handle)

def groupObjects(list: List[SceneObject]):
	"""
	Groups an array of SceneObjects.
	"""
	return cur_server.exec('mset.groupObjects', __handle, list)

def importMaterial(filePath: str, name: str = '') -> Material:
	"""
	Imports the specified material file into the scene. If no name is given, one will be automatically assigned.This function supports import from Toolbag materials, MTL files, Valve/Dota materials, and named texture files.Returns the imported material.
	"""
	return cur_server.exec('mset.importMaterial', __handle, filePath,name)

def importModel(filePath: str) -> SceneObject:
	"""
	Imports the specified model into the existing scene, using the scene's current import settings.Returns the imported object.
	"""
	return cur_server.exec('mset.importModel', __handle, filePath)

def loadScene(filePath: str):
	"""
	Loads a Marmoset Toolbag scene file.Unsaved changes to any currently open scenes are lost.
	"""
	return cur_server.exec('mset.loadScene', __handle, filePath)

def log(msg: str):
	"""
	Prints text to the application log, similar to print(). No return will be appended.
	"""
	return cur_server.exec('mset.log', __handle, msg)

def newScene():
	"""
	Creates a new empty scene.Any unsaved changes in the current scene will be lost.
	"""
	return cur_server.exec('mset.newScene', __handle)

def quit():
	"""
	Quits the application. Any unsaved changes will be lost.
	"""
	return cur_server.exec('mset.quit', __handle)

def readAndExportStamp(inputPath: str, outputPath: str):
	"""
	Marmoset internal use for stamp brush creation
	"""
	return cur_server.exec('mset.readAndExportStamp', __handle, inputPath,outputPath)

def renderCamera(path: str = '', width: int = -1, height: int = -1, sampling: int = -1, transparency: bool = False, camera: str = '') -> Image:
	"""
	Renders an image with the given camera, or the main camera if none is specified. This will use the current resolution/format settings from the render scene object. Returns an mset.Image instance. Optionally takes a path parameter, which specifies where to write the image. If no path is specified, no image file will be written.
	"""
	return cur_server.exec('mset.renderCamera', __handle, path,width,height,sampling,transparency,camera)

def renderImages(width: int = -1, height: int = -1, sampling: int = -1, transparency: bool = False):
	"""
	Renders images with the render scene object's current settings and cameras. To render a single image, see renderCamera().
	"""
	return cur_server.exec('mset.renderImages', __handle, width,height,sampling,transparency)

def renderVideos(width: int = -1, height: int = -1, sampling: int = -1, transparency: bool = False):
	"""
	Captures an animation into a video file or image sequence. The animation will be written into the file path(s) specified in the scene's render object.
	"""
	return cur_server.exec('mset.renderVideos', __handle, width,height,sampling,transparency)

def saveScene(filePath: str):
	"""
	Saves a Marmoset Toolbag scene file.If a scene file path is not specified, the scene will be saved to its existing location.
	"""
	return cur_server.exec('mset.saveScene', __handle, filePath)

def setCamera(camera: CameraObject):
	"""
	Sets the current active camera for viewport and screenshot rendering.
	"""
	return cur_server.exec('mset.setCamera', __handle, camera)

def setStoreItem(key: str, val: Any):
	"""
	Store data in a shared persistent store that is accessable across plugins.
	"""
	return cur_server.exec('mset.setStoreItem', __handle, key,val)

def showOkCancelDialog(title: str, prompt: str) -> bool:
	"""
	Prompts the user with a modal dialog box. The window is given a titlebar named 'title' and prompt text 'prompt'. Returns True or False depending on whether OK or Cancel is selected.
	"""
	return cur_server.exec('mset.showOkCancelDialog', __handle, title,prompt)

def showOpenFileDialog(fileTypes: List[str] = [], multiple: bool = False) -> str:
	"""
	Prompts the user with a file open dialog box, and resumes after the user selects a file.Returns the selected file path, or an empty string if the user canceled the dialog.Permitted file extensions can be optionally specified by the fileTypes array, which can contain one or more of: 'images', 'models', 'materials', which specify categories of file types, individual file extensions supported by Marmoset Toolbag (such as 'jpg', 'fbx', etc.), or at most one custom file extension. Specify extension names in lower case without the '.' character.Multiple files my be selected, and paths will be returned as an array, if 'multiple' is set to True.
	"""
	return cur_server.exec('mset.showOpenFileDialog', __handle, fileTypes,multiple)

def showOpenFolderDialog() -> str:
	"""
	Prompts the user with a folder open dialog box, and resumes after the user selects a folder.Returns the selected file path, or an empty string if the user canceled the dialog.
	"""
	return cur_server.exec('mset.showOpenFolderDialog', __handle)

def showSaveFileDialog(fileTypes: List[str] = []) -> str:
	"""
	Prompts the user with a file save dialog box, and resumes after the user selects a file destination.Returns the selected file path, or an empty string if the user canceled the dialog.Permitted file extensions can be optionally specified by the fileTypes array, which can contain one or more of: 'images', 'models', 'materials', which specify categories of file types, individual file extensions supported by Marmoset Toolbag (such as 'jpg', 'fbx', etc.), or at most one custom file extension. Specify extension names in lower case without the '.' character.
	"""
	return cur_server.exec('mset.showSaveFileDialog', __handle, fileTypes=[])

def shutdownPlugin():
	"""
	Halts execution and shuts down the currently running plugin.
	"""
	return cur_server.exec('mset.shutdownPlugin', __handle)

callbacks = Callbacks()
"""Global callbacks that you can assign for this plugin."""


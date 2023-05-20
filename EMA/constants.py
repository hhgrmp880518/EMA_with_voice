from manim import*

# constant
FRAME_WIDTH: float = config.frame_width
FRAME_HEIGHT: float = config.frame_height

# constant for Title-Formula-Animation (TFA) layout type
TFA_TITLE: np.ndarray = np.array((FRAME_WIDTH*0.5, FRAME_HEIGHT*0.09, 0))
TFA_TITLE_WIDTH: float = FRAME_WIDTH*0.8
TFA_TITLE_HEIGHT: float = FRAME_HEIGHT*0.12
TFA_FORMULA: list[np.ndarray] = [np.array((FRAME_WIDTH*0.05, FRAME_HEIGHT*(0.2775+0.085*x), 0)) for x in range(8)]
TFA_FORMULA_WIDTH: float = FRAME_WIDTH*0.4
TFA_FORMULA_HEIGHT: float = FRAME_HEIGHT*0.085
TFA_ANIMATION: np.ndarray = np.array((FRAME_WIDTH*0.55, FRAME_HEIGHT*0.507, 0))
TFA_ANIMATION_WIDTH: float = FRAME_WIDTH*0.4
TFA_ANIMATION_HEIGHT: float = FRAME_HEIGHT*0.544
TFA_ANSWER: np.ndarray = np.array((FRAME_WIDTH*0.55, FRAME_HEIGHT*0.847, 0))
TFA_ANSWER_WIDTH: float = FRAME_WIDTH*0.4
TFA_ANSWER_HEIGHT: float = FRAME_HEIGHT*0.136

#style
DEFAULT_FONT_TYPE: str = "Noto Sans TC Medium"
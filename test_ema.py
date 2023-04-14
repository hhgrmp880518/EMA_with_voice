from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

from explanatoryTool import *

# 執行方式
# namin test_ema.py


class EMA(explanatoryTools, VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="zh-TW-YunJheNeural",
                style="newscast-casual",  # global_speed=1.15
            )
        )

        # 以下三個 numberLineAdd 會展示在不同速度下的差別。
        #self.numberLineAdd(10.5, 5.2, 9.27, position=[1, 1.8, 0.0], length=5, speed=5) #高速
        #self.numberLineSub(102.5, 54.2, 11.27, position=[1, 4, 0.0], length=5)              #預設 = 1
        #self.numberLineMul(2, 3, position=[1, 6.2, 0.0], length=5, speed=0.5) #低速
        
        # 以下三個 numberLineAdd 會展示在不同的字體樣式和場景設定下的效果。
        #self.numberLineMul(4, 3, 2, position=[8, 1.8, 0], length=5, bold=True)            #粗體
        #self.numberLineAdd(5, 7.3, position=[8, 4, 0], length=5, slant=True)             #斜體
        #self.numberLineAdd(5, 7.3, position=[8, 6.2, 0], length=5, clear=True)           #清除

        #self.numberLineAdd(10.5, 5.2, 9.27, width=5, position=[1, 1.8, 0.0], length=5)
        #self.numberLineSub(102.5, 54.2, 11.27, width=5, position=[1, 4, 0.0], length=5)
        #self.numberLineMul(2, 3, width=5, position=[1, 6.2, 0.0], length=5)
        #self.numberLineMul(2, 3, 4, 3, 2, width=5, position=[8, 1.8, 0.0], length=5)

        #self.numberLineAdd(10.5, 5.2, 9.27, width=5, position=[1, 1.8, 0.0], length=5)
        #self.numberLineSub(102.5, 54.2, 11.27, width=5, position=[8, 1.8, 0.0], length=5)
        #self.numberLineMul(2, 3, width=5, position=[1, 4, 0.0], length=5)
        self.numberLineMul(2, 3, 4, 3, 2, width=5, position=[1, 1.8, 0.0], length=5)

        

        

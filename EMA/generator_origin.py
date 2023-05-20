from EMA.constants import*
from EMA.explanatoryTools.tool import*
import globals
from manim import*

# EMA 動畫產生器
class animation(explanatoryTools):
    def construct(self):
        self.layout(0)
        StepsText = list(globals.require_list.values())[0].StepsText
        question = list(globals.require_list.values())[0].text
        self.text(question, TFA_TITLE, TFA_TITLE_WIDTH, TFA_TITLE_HEIGHT, font_size=48, aligned_edge=ORIGIN)

        for i in range(len(StepsText)):
            command = StepsText[i][0]
            nums = StepsText[i][1]
            clear = {True:False, False:True}[i == len(StepsText)-2]

            if command == 'add':
                self.text(f'{nums[0]}+{nums[1]}=?', TFA_FORMULA[2*i], TFA_FORMULA_WIDTH, TFA_FORMULA_HEIGHT, font_size=32, aligned_edge=LEFT)
                self.numberLineAdd(
                    nums[0], nums[1], 
                    position=TFA_ANIMATION, 
                    width=TFA_ANIMATION_WIDTH, 
                    max_width=TFA_ANIMATION_WIDTH, 
                    max_height=TFA_ANIMATION_HEIGHT, 
                    aligned_edge=LEFT, 
                    clear=clear
                )
                self.text(f'{nums[0]}+{nums[1]}={nums[0]+nums[1]}', TFA_FORMULA[2*i+1], TFA_FORMULA_WIDTH, TFA_FORMULA_HEIGHT, font_size=32, aligned_edge=LEFT)
            
            elif command == 'sub':
                self.text(f'{nums[0]}-{nums[1]}=?', TFA_FORMULA[2*i], TFA_FORMULA_WIDTH, TFA_FORMULA_HEIGHT, font_size=32, aligned_edge=LEFT)
                self.numberLineSub(
                    nums[0], nums[1], 
                    position=TFA_ANIMATION, 
                    width=TFA_ANIMATION_WIDTH, 
                    max_width=TFA_ANIMATION_WIDTH, 
                    max_height=TFA_ANIMATION_HEIGHT, 
                    aligned_edge=LEFT, 
                    clear=clear
                )
                self.text(f'{nums[0]}-{nums[1]}={nums[0]-nums[1]}', TFA_FORMULA[2*i+1], TFA_FORMULA_WIDTH, TFA_FORMULA_HEIGHT, font_size=32, aligned_edge=LEFT)
            elif command == 'mul':
                if nums[1] <= 10:
                    self.text(f'{nums[0]}*{nums[1]}=?', TFA_FORMULA[2*i], TFA_FORMULA_WIDTH, TFA_FORMULA_HEIGHT, font_size=32, aligned_edge=LEFT)
                    self.numberLineMul(
                        nums[0], nums[1],
                        position=TFA_ANIMATION, 
                        width=TFA_ANIMATION_WIDTH, 
                        max_width=TFA_ANIMATION_WIDTH, 
                        max_height=TFA_ANIMATION_HEIGHT, 
                        aligned_edge=LEFT,
                        clear=clear
                    )
                    self.text(f'{nums[0]}*{nums[1]}={nums[0]*nums[1]}', TFA_FORMULA[2*i+1], TFA_FORMULA_WIDTH, TFA_FORMULA_HEIGHT, font_size=32, aligned_edge=LEFT)
                else:
                    raise ValueError('Only can multiplicate when multiplicand no bigger than 10')
            elif command == 'ans':
                self.text(f'答案是：{nums[0]}', TFA_ANSWER, TFA_ANSWER_WIDTH, TFA_ANSWER_HEIGHT, font_size=24, aligned_edge=LEFT)
        self.wait(5)
        print('good')

# EMA 封面產生器
class image(explanatoryTools):
    def construct(self):
        title = list(globals.require_list.values())[0].text
        self.text(title, (FRAME_WIDTH*0.5, FRAME_HEIGHT*0.5, 0), FRAME_WIDTH*0.8, font_size=96, aligned_edge=ORIGIN, type='image')
        print('good')

def generator(user_id):

    # 設定 manim 的 config 選項
    config_dict = {
        'quality': 'medium_quality',
        'disable_caching': True,
        'video_dir': './Linebot/static',
        'images_dir': './Linebot/static',
        'output_file': user_id,
        'flush_cache': True,
    }

    # 使用指定的 manim 的 config 選項
    with tempconfig(config_dict):
        # 呼叫 image() 來產生 EMA 封面
        image1 = image()
        image1.render()  # 執行封面渲染

    # 使用指定的 manim 的 config 選項
    with tempconfig(config_dict):
        animation1 = animation()
        # 呼叫 animation() 來產生 EMA 動畫
        animation1.render()  # 執行動畫渲染
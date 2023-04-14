from random import choice

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

# 反轉位數
def toReverseDigit(num):
    result = [int(a) for a in str(num)]
    result.reverse()
    result += [0]*(MAX_DIGIT-len(str(num)))
    return result

# 將各位數的進位，轉成list儲存
def carry_list(list1, list2):
    sum_int_list=[]
    carry_int_list=[0]

    if len(list1) < len(list2):
        list1, list2 = list2, list1

    for i in range(len(list2)):
        sum_int_list.append(list1[i]+list2[i]+carry_int_list[i])
        carry_int_list.append({True:1,False:0}[sum_int_list[i]>=10])
        
    for i in range(len(list2),len(list1)):
        sum_int_list.append(list1[i]+carry_int_list[i])
        carry_int_list.append({True:1,False:0}[sum_int_list[i]>=10])

    carry_int_list.append(carry_int_list.pop(0))
    carry_str_list = list(map(str,carry_int_list))

    return carry_int_list

# 自動生成加法語音稿
# 示例語音稿： 10 加上 2 加上 51 會等於 63
def text_add_line(args, ans):

    # 加法中，每個數字的顯示都是一段動畫
    # 因此我們把每個數字的語音稿都作為一個獨立字串放入陣列中，後面就能依照動畫順序播放語音
    text_group = ["加上"+str(num) if num != args[0] else str(num) for num in args]
    text_group.append("會等於" + str(ans))
    return text_group

# 自動生成減法語音稿
# 示例語音稿： 100 減掉 2 減掉 51 會等於 47
def text_sub_line(args, ans):

    # 方法近似加法
    text_group = ["減掉"+str(num) if num != args[0] else str(num) for num in args]
    # 因為減法的答案動畫及答案標籤分開顯示，因此需要要兩段語音分開獨立
    text_group.append("會等於")
    text_group.append(str(ans))
    return text_group

# 自動生成乘法語音稿
'''
示例語音稿(因「乘」的讀音有問題，語音稿中使用「成」來代替)： 
    title:
        計算4成3成2，我們先看4成3，就是會有3個4加起來，我們先把4的數線畫下來
    count(repeat):
        第1個4，第2個4，第3個4
    middle(repeat):
        全部加起來，會等於12，也就是4成3的結果，接著，我們看4成3成2，相當於12成2，也就是2個12加起來，我們剩下的12的數線畫下來
    end:
        全部加起來，會等於24，也就是4成3成2的結果
 '''
def text_mul_line(args, nums):
    # nums 是階段性結果
    # 示例：[4, 12, 24]

    # 放解說語音稿
    text_group = []
    # 放數數語音稿
    for_group = []

    # text_group 1, title
    title = "計算"

    # 因為設計的語音稿中反覆出現題目，因此抓出來方便使用，增加自動性
    # 示例：[4, 4成3, 4成3成2]
    problems = []
    problem = ""

    for i in range(len(args)):
        if i == 0:
            problem += str(args[i])
        else:
            problem += "成" + str(args[i])
            problems.append(problem)

    title += problems[-1]

    # 做乘法的數字超過2個，才會有「先看」的行為
    if len(args) > 2:
        title += "，我們先看" + problems[0]

    title += "，也就是會有" + str(args[1])+"個"+str(args[0]) + "加起來，我們先把" + str(args[0]) + "的數線畫下來"
    text_group.append(title)

    # text_group 2 ~ -2, middle
    # 參數都是變數，此段 mid 會根據乘數數量反覆執行多次，自動生成語音稿
    for i in range(len(args)-2):
        mid = "全部加起來，會等於"+str(nums[i+1])+"，也就是"+problems[i]+"的結果，"+ \
            "接著，我們看"+ problems[i+1] +"，相當於"+str(nums[i+1])+"成"+str(args[i+2])+ \
            "，也就是"+str(args[i+2])+"個"+str(nums[i+1])+"加起來，我們來把剩下的"+str(nums[i+1])+"的數線畫下來"
        text_group.append(mid)

    # text_group -1, end
    end = "全部加起來，會等於" + str(nums[-1]) + "，也就是" + problem + "的結果"
    text_group.append(end)

    # for group
    # 有雙層陣列，原因在於有多個乘數時，要區分不同乘數產生的語音稿
    #示例：[[第1個4, 第2個4, 第3個4], [第1個12, 第2個12, 第3個12, 第4個12]]
    for i in range(len(args)-1):
        for_group.append(["第"+str(j+1)+"個"+str(nums[i]) for j in range(args[i+1])])

    return text_group, for_group

def toReverseDigit(num):
    x = [int(a) for a in str(num)]
    x.reverse()
    return x


class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # Initialize speech synthesis using Azure's TTS API
        self.set_speech_service(
            AzureService(
                voice="zh-TW-YunJheNeural",
                style="newscast-casual",  # global_speed=1.15
            )
        )
        
        text_group = text_add_line(10.5, 5.2, 9.27)

        for i in range(len(text_group)):
            
            with self.voiceover(text=text_group[i]):
                self.play(Create(Circle(radius=i*0.5+1,color=BLUE)))
                    
        self.wait()

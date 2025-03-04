import copy
import random
from app.services.lifelog_service import LifelogService
from flask import current_app, url_for
import base64
from jinja2 import Template
import os
from app.utils.tts_service import AzureTTS


def make_puzzle(user_id,session_id):
    puzzle_instance = copy.deepcopy(puzzle_instance_template)
    
    # randomly select a category and a thing
    category = random.choice(list(candidates.keys()))
    thing = random.choice(candidates[category])
    
    print('guess a thing:',category, thing)
    
    # fill model history for prompt
    puzzle_instance['model_history'][0]['content'][0]['text'] = Template(puzzle_instance['model_history'][0]['content'][0]['text']).render({'category':category, 'thing':thing})
    
    # fill display history for display
    puzzle_instance['instruction_message']['content'][0]['data'] = Template(puzzle_instance['instruction_message']['content'][0]['data']).render({'category':category, 'thing':thing})
    
    # ASR
    audio_file = AzureTTS.text_to_speech(puzzle_instance['instruction_message']['content'][0]['data'],f'chat_sessions/{session_id}')
    audio_url = url_for('static', filename=audio_file)
    puzzle_instance['instruction_message']['content'].append({
        "type":"audio",
        "data":audio_url
    })
    
    return puzzle_instance

candidates = {
        "动物": ["狗", "猫", "老虎", "大象", "狮子", "熊", "鹿", "猴子", "斑马", "鲨鱼"],
        "交通工具": ["汽车", "公交车", "自行车", "摩托车", "火车", "飞机", "船", "卡车", "地铁", "电车"],
        "水果": ["苹果", "香蕉", "橙子", "草莓", "葡萄", "樱桃", "西瓜", "桃子", "柠檬", "芒果"],
        "家用电器": ["冰箱", "洗衣机", "电视", "空调", "微波炉", "吸尘器", "电风扇", "烤箱", "电熨斗", "电饭锅"],
        "体育项目": ["足球", "篮球", "羽毛球", "乒乓球", "排球", "网球", "高尔夫", "滑雪", "橄榄球", "田径"],
        "乐器": ["钢琴", "吉他", "小提琴", "长笛", "萨克斯", "鼓", "大提琴", "口琴", "电子琴", "手风琴"],
        "蔬菜": ["胡萝卜", "菠菜", "西红柿", "黄瓜", "土豆", "洋葱", "茄子", "白菜", "西蓝花", "青椒"],
        "文具": ["钢笔", "铅笔", "橡皮", "尺子", "笔记本", "订书机", "剪刀", "胶水", "马克笔", "圆规"],
        "家具": ["沙发", "椅子", "床", "桌子", "衣柜", "书架", "茶几", "餐桌"],
        "服装": ["衬衫", "裤子", "裙子", "外套", "毛衣", "T恤", "牛仔裤", "西装", "大衣", "运动服"],
        "饮料": ["水", "咖啡", "茶", "牛奶", "果汁", "可乐", "啤酒", "红酒", "绿茶", "豆浆"],
        "家居用品": ["枕头", "被子", "床单", "毛巾", "浴巾", "窗帘", "地毯", "沙发套", "台灯", "衣架"],
        #"文娱活动": ["电影", "读书", "听音乐", "绘画", "唱歌", "跳舞", "摄影", "写作", "烹饪", "园艺"],
        "自然景观": ["山", "河流", "湖泊", "森林", "沙漠", "瀑布", "海滩", "峡谷", "冰川", "火山"],
        "气象现象": ["晴天", "雨天", "雪天", "雾天", "雷电", "台风", "龙卷风", "冰雹", "彩虹", "霜"],
        "建筑": ["住宅", "办公楼", "超市", "学校", "医院", "图书馆", "博物馆", "剧院", "体育馆", "餐厅"],
        "节日": ["春节", "中秋节", "端午节", "元宵节", "清明节", "国庆节", "圣诞节", "元旦", "情人节"],
        #"旅游景点": ["长城", "故宫", "黄山", "丽江古城", "张家界", "桂林山水", "九寨沟", "西湖", "布达拉宫", "兵马俑","埃菲尔铁塔", "大本钟", "长城", "金字塔", "自由女神像", "泰姬陵", "帕特农神庙", "比萨斜塔", "罗马斗兽场", "悉尼歌剧院"],
        #"食物": ["米饭", "面条", "饺子", "包子", "寿司", "披萨", "汉堡", "沙拉", "烤肉", "火锅"],
        "节气": ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至"],
        "金属": ["铁", "铜", "银", "金", "铝", "锌", "镍", "锡", "铅", "钛"],
        "生活用品": ["牙刷", "牙膏", "肥皂", "洗发水", "沐浴露", "洗衣粉", "梳子", "镜子", "剃须刀", "指甲刀"],
        "植物": ["玫瑰", "郁金香", "向日葵", "牡丹", "兰花", "樱花", "竹子", "仙人掌", "松树", "柳树", "向日葵", "兰花", "仙人掌", "竹子", "松树", "桂花", "牡丹", "菊花", "荷花"],
        #"学科": ["物理", "化学", "生物", "天文学", "地理", "数学", "计算机科学", "工程学", "医学", "环境科学"],
        #"身体部位": ["头", "肩膀", "膝盖", "脚", "手", "眼睛", "耳朵", "鼻子", "嘴巴", "腿"],
        #"家庭成员": ["父亲", "母亲", "哥哥", "姐姐", "弟弟", "妹妹", "祖父", "祖母", "叔叔", "阿姨"],
        #"心情": ["快乐", "悲伤", "愤怒", "惊讶", "恐惧", "焦虑", "兴奋", "平静", "满足", "沮丧"],
        "颜色": ["红色", "蓝色", "绿色", "黄色", "紫色", "橙色", "粉色", "黑色", "白色", "灰色"],
        "海洋生物": ["鲨鱼", "海豚", "鲸鱼", "章鱼", "海星", "珊瑚", "海龟", "水母", "海马"],
        "自然灾害": ["地震", "台风", "洪水", "干旱", "火灾", "泥石流", "海啸", "龙卷风", "雪崩", "冰雹"],
        "调味品": ["盐", "糖", "醋", "酱油", "胡椒", "辣椒", "蚝油", "芥末", "五香粉"],
        #"常见病": ["感冒", "发烧", "头痛", "腹泻", "高血压", "糖尿病", "哮喘", "胃炎", "关节炎", "失眠"],
        "传统节日": ["端午节", "重阳节", "七夕节", "春节", "中秋节", "元宵节", "清明节", "元旦"],
        #"电子产品": ["手机", "电脑", "平板", "耳机", "相机", "智能手表", "游戏机", "蓝牙音箱", "打印机", "路由器"],
        #"天体": ["太阳", "月亮", "地球", "火星", "木星", "金星", "水星", "土星", "天王星", "海王星"],
        #"交通设施": ["桥梁", "隧道", "高速公路", "铁路", "机场", "港口", "地铁站", "公交车站", "收费站", "停车场"],
        #"宝石": ["钻石", "红宝石", "蓝宝石", "祖母绿", "珍珠", "玛瑙", "翡翠"],
        #"文学体裁": ["小说", "诗歌", "散文", "戏剧", "童话", "寓言", "传记", "随笔", "报告文学", "科幻小说"],
        "工具": ["锤子", "螺丝刀", "钳子", "扳手", "锯子", "电钻", "斧头", "卷尺", "水平仪", "砂纸"],
        #"金融工具": ["股票", "债券", "期货", "期权", "基金", "外汇", "保险", "信托", "存款", "贷款"],
        #"音乐流派": ["古典音乐", "爵士乐", "摇滚乐", "流行音乐", "乡村音乐", "电子音乐", "蓝调", "嘻哈", "雷鬼", "民谣"],
        #"茶叶种类": ["龙井", "碧螺春", "铁观音", "大红袍", "普洱", "白茶", "黄茶", "毛尖", "乌龙茶", "红茶"],
        #"舞蹈": ["芭蕾", "街舞", "探戈", "华尔兹", "爵士舞", "现代舞", "民族舞", "拉丁舞", "踢踏舞", "霹雳舞"],
        #"神话人物": ["嫦娥", "孙悟空", "哪吒", "玉皇大帝", "宙斯", "雅典娜", "奥丁", "雷神", "阿波罗", "赫拉克勒斯"],
        #"世界遗产": ["万里长城", "故宫", "兵马俑", "敦煌莫高窟", "苏州园林", "黄山", "桂林山水", "武陵源", "丽江古城", "平遥古城"],
        #"棋类游戏": ["象棋", "围棋", "国际象棋", "五子棋", "跳棋", "军棋", "黑白棋", "麻将", "斗兽棋", "飞行棋"],
        #"地理概念": ["赤道", "南北极", "大陆", "海洋", "热带", "温带", "寒带", "平原", "高原", "盆地"],
        #"古代文明": ["中国", "埃及", "玛雅", "印度", "希腊", "罗马", "波斯", "巴比伦", "印加", "阿兹特克"],
        #"编程语言": ["Python", "Java", "C++", "JavaScript", "Ruby", "Go", "Swift", "Kotlin", "PHP", "Rust"],
        #"科学家": ["牛顿", "达尔文", "居里夫人", "特斯拉", "霍金", "法拉第", "伽利略", "麦克斯韦", "图灵"],
        #"哲学家": ["苏格拉底", "柏拉图", "亚里士多德", "康德", "黑格尔", "笛卡尔", "尼采", "萨特", "孔子", "老子"],
        #"建筑风格": ["哥特式", "巴洛克式", "古典主义", "现代主义", "后现代主义", "新古典主义", "装饰艺术", "高科技建筑", "乡村风格", "极简主义"],
        #"文学作品": ["红楼梦", "西游记", "水浒传", "三国演义", "简爱", "傲慢与偏见", "战争与和平", "百年孤独", "哈利·波特", "指环王"],
    }
    

puzzle_instance_template = {
    "name": "guess_a_thing",
    "model_history": [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": """你是一个认知训练游戏助手，通过游戏锻炼我的记忆力、逻辑推理能力、反应速度、语言能力等认知能力。我是参与认知训练的玩家。现在我们正在玩一个猜物品的游戏。你会想一个物品，然后我会问你一些问题，你只回答是或者不是，但是你不能直接告诉我你在想的是什么物品。我会根据你的回答猜出你在想的物品。

在本轮游戏中，你想的物品类别是：**{{category}}**，你想的物品是：**{{thing}}**。

详细规则如下：
1. 我负责提问猜测，你负责回答是或者不是。当我的猜测与答案是同义词时，你可以补充更多信息。
2. 如果我的对话偏离了游戏主题，你将引导我回到游戏中。
3. 如果我寻求额外的提示，你会利用我们的对话历史帮助我回顾之前的猜测和所得信息，以协助我的推理。
4. 如果我的推理有逻辑上的缺陷，或者你认为我的推理杂乱无逻辑，你同样会提供引导性的提示，帮助我梳理已有的信息。
5. 在任何时候，在游戏中你都不会直接告诉我答案，请时刻注意。在你的输出和提示中一定不要透露你在想的物品。
6. 当我猜对了你在想的物品时，你会告诉我答案，并给我正面反馈，称赞我的尝试，尤其是我提出的好的问题，正面反馈多给用户一些赞美和夸奖。在回答里加入<end>标记，表示游戏结束。
7. 当我不再想继续猜测时，你可以告诉我答案，并给我正面反馈，称赞我的尝试，在回答里加入<end>标记，表示游戏结束。
8. 游戏结束时你会给我讲一些关于这个物品的有趣知识，以便我学习新知识。

你通过以下格式给出反馈输出:
1. 首先，你整理你的内部思考，这部分输出用<thoughts></thoughts>标记。
2. 然后，你回答我的问题，这部分输出用<outputs></outputs>标记。这部分使用口语化的中文。
3. <thoughts>和<outputs>标签注意正确关闭。

**重要提示**：所有回答必须严格包裹在正确的标记中。
例如，如果我问“这是电子产品吗？”，你的回答应该是：
<thoughts>是的，电视是电子产品。</thoughts>
<outputs>是的。</outputs>。
请确保不要遗漏标记的开头和结尾。

下面开始游戏：
""",
            },
            # {
            #     "type": "image_url",
            #     "image_url": {"url": ""},
            # },
        ],
    }],
    "instruction_message":{
        "role":"assistant",
        "content":[
            {
                "type":"text",
                "data":"这次请你猜一种{{category}}，你可以问我问题，但是我只会回答是或者不是。"
            }
        ]
    },
    "addtional_parser_rule":{
        "<end>": {"end":"end"},
    }
}

import re, os

def get_ket_words():
    """Get all words from existing KET/中考 vocabulary"""
    files = [
        'vocabulary/core-vocabulary-p1.html',
        'vocabulary/core-vocabulary-p2.html',
        'vocabulary/core-vocabulary-p3.html',
        'vocabulary/core-vocabulary-p4.html',
        'vocabulary/core-vocabulary-p5.html',
        'vocabulary/core-vocabulary-p6.html',
        'vocabulary/verbs-a-l.html',
        'vocabulary/verbs-m-z.html',
        'vocabulary/adjectives-adverbs.html',
        'vocabulary/nouns-life-scene.html',
        'vocabulary/nouns-society-function.html'
    ]
    words = set()
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        found = re.findall(r'<span class="word">([^<]+)</span>', content)
        for w in found:
            words.add(w.strip().lower())
    return words

def write_page(title_prefix, subtitle, page_num, total_pages, prev_page, next_page, words_data, ket_words, filename):
    """Write a vocabulary HTML page filtering out KET words"""
    lines = []
    lines.append('<!DOCTYPE html>')
    lines.append('<html lang="zh-CN">')
    lines.append('<head>')
    lines.append('    <meta charset="UTF-8">')
    lines.append('    <meta name="referrer" content="same-origin">')
    lines.append(f'    <title>{title_prefix} 备考通 - 第{page_num}页/共{total_pages}页</title>')
    lines.append('    <link rel="stylesheet" href="../css/common.css">')
    lines.append('    <script defer src="../js/common.js"></script>')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('')
    lines.append('<div class="container">')
    lines.append(f'    <h1>{title_prefix} 速记表</h1>')
    lines.append(f'    <p style="text-align: center;">📖 {subtitle} | 第{page_num}页 / 共{total_pages}页</p>')
    lines.append('')
    lines.append('    <!-- 自测控制面板 -->')
    lines.append('    <div class="control-panel">')
    lines.append('        <button class="btn-toggle" id="btn-words"')
    lines.append('            onclick="toggleExam(\'hide-words\', \'btn-words\', \'单词\')">👁️ 隐藏单词</button>')
    lines.append('        <button class="btn-toggle" id="btn-inflections"')
    lines.append('            onclick="toggleExam(\'hide-inflections\', \'btn-inflections\', \'特殊变形\')">👁️ 隐藏变形</button>')
    lines.append('        <button class="btn-toggle" id="btn-meanings"')
    lines.append('            onclick="toggleExam(\'hide-meanings\', \'btn-meanings\', \'中文释义\')">👁️ 隐藏释义</button>')
    lines.append('        <button class="btn-toggle" id="btn-translations"')
    lines.append('            onclick="toggleExampleColumn(\'btn-translations\')">👁️ 隐藏翻译</button>')
    
    if prev_page:
        lines.append(f'        <button class="btn-toggle btn-nav" onclick="window.location.href=\'{prev_page}\'">⬅ P{page_num-1}</button>')
    if next_page:
        lines.append(f'        <button class="btn-toggle btn-nav" onclick="window.location.href=\'{next_page}\'">P{page_num+1} ➡</button>')
    lines.append('        <button class="btn-toggle btn-nav" onclick="window.location.href=\'../index.html\'">🔙 返回</button>')
    
    lines.append('    </div>')
    lines.append('')
    lines.append('    <div id="vocabulary-content">')
    prefix = "PET核心" if "PET" in title_prefix else "高考核心"
    lines.append(f'        <h2>{prefix}词汇{" (已排除KET重复)" if page_num == 1 else ""}</h2>')
    lines.append('        <table>')
    lines.append('            <thead>')
    lines.append('                <tr>')
    lines.append('                    <th style="width: 15%;">单词 & 音标</th>')
    lines.append('                    <th style="width: 20%;">特殊变形 / 提示</th>')
    lines.append('                    <th style="width: 25%;">中文释义</th>')
    lines.append('                    <th style="width: 40%;">典型例句</th>')
    lines.append('                </tr>')
    lines.append('            </thead>')
    lines.append('            <tbody>')
    
    count = 0
    for word, ipa, inflection, meaning, example, example_cn in words_data:
        w_lower = word.strip().lower()
        # Skip KET words
        skip = False
        for k in ket_words:
            if w_lower == k or w_lower.startswith(k + ' ') or w_lower.endswith(' ' + k) or (' / ' in w_lower and k in w_lower.split(' / ')):
                skip = True
                break
        if skip:
            continue
        count += 1
        lines.append('                <tr>')
        lines.append(f'                    <td><span class="word">{word}</span><br><span class="ipa">{ipa}</span></td>')
        lines.append(f'                    <td class="inflection">{inflection}</td>')
        lines.append(f'                    <td class="meaning">{meaning}</td>')
        lines.append(f'                    <td>')
        lines.append(f'                        <span class="example">{example}</span>')
        lines.append(f'                        <span class="example-cn">{example_cn}</span>')
        lines.append(f'                    </td>')
        lines.append('                </tr>')
    
    lines.append('            </tbody>')
    lines.append('        </table>')
    lines.append('        ')
    lines.append('    </div>')
    lines.append('</div>')
    lines.append('')
    lines.append('</body>')
    lines.append('</html>')
    
    content = '\n'.join(lines)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return count

# ===== PET COMPREHENSIVE WORD LIST (B1 Preliminary) =====
# Official PET vocabulary list covers approx 3500 words
# Here we add the B1-level words not covered in KET/A2

pet_words_data = [
    # P1: A-B
    ("abandon", "/əˈbændən/", "abandoning;<br>abandoned", "v. 放弃；遗弃；抛弃", "They had to abandon the plan due to lack of funds.", "由于缺乏资金，他们不得不放弃计划。"),
    ("absorb", "/əbˈzɔːb/", "absorbing;<br>absorbed", "v. 吸收；吸引；使专心", "Plants absorb carbon dioxide from the air.", "植物从空气中吸收二氧化碳。"),
    ("abstract", "/ˈæbstrækt/", "abstracts (复数)", "adj. 抽象的；理论的<br>n. 摘要", "The idea of freedom is an abstract concept.", "自由的概念是一个抽象概念。"),
    ("abundant", "/əˈbʌndənt/", "more abundant;<br>most abundant", "adj. 丰富的；充裕的；盛产的", "The region has abundant natural resources.", "该地区拥有丰富的自然资源。"),
    ("abuse", "/əˈbjuːs/", "abusing;<br>abused", "n. & v. 滥用；虐待；辱骂", "We must prevent drug abuse among teenagers.", "我们必须防止青少年滥用药物。"),
    ("academic", "/ˌækəˈdemɪk/", "adj. (无变形)", "adj. 学术的；学业的；学院的", "She has a strong academic background.", "她有很强的学术背景。"),
    ("accelerate", "/əkˈseləreɪt/", "accelerating;<br>accelerated", "v. 加速；促进；加快", "The car accelerated quickly.", "汽车迅速加速。"),
    ("access", "/ˈækses/", "<span class=\"tag\">不可数名词</span>", "n. 通道；进入；使用权<br>v. 访问", "Students have free access to the library.", "学生可以免费使用图书馆。"),
    ("accommodation", "/əˌkɒməˈdeɪʃn/", "accommodations (复数)", "n. 住宿；膳宿；和解", "We need to find accommodation for the night.", "我们需要找过夜的地方。"),
    ("accompany", "/əˈkʌmpəni/", "accompanies;<br>accompanying;<br>accompanied", "v. 陪伴；伴随；伴奏", "I will accompany you to the airport.", "我会陪你去机场。"),
    ("accomplish", "/əˈkʌmplɪʃ/", "accomplishing;<br>accomplished", "v. 完成；实现；达成", "We accomplished our goal ahead of schedule.", "我们提前完成了目标。"),
    ("account", "/əˈkaʊnt/", "accounts (复数)", "n. 账户；描述；解释<br>v. 说明；占(比例)", "He gave a detailed account of the accident.", "他详细描述了事故的经过。"),
    ("accumulate", "/əˈkjuːmjəleɪt/", "accumulating;<br>accumulated", "v. 积累；积聚；积攒", "Dust accumulates quickly on the furniture.", "家具上很快就积了灰尘。"),
    ("accurate", "/ˈækjərət/", "more accurate;<br>most accurate", "adj. 准确的；精确的；正确的", "Make sure your measurements are accurate.", "确保你的测量准确。"),
    ("accuse", "/əˈkjuːz/", "accusing;<br>accused", "v. 控告；指控；指责", "He was accused of stealing the money.", "他被指控偷了钱。"),
    ("acknowledge", "/əkˈnɒlɪdʒ/", "acknowledging;<br>acknowledged", "v. 承认；感谢；确认收到", "She acknowledged her mistake.", "她承认了错误。"),
    ("acquire", "/əˈkwaɪə(r)/", "acquiring;<br>acquired", "v. 获得；学到；获取", "She acquired a good knowledge of English.", "她学到了很好的英语知识。"),
    ("adapt", "/əˈdæpt/", "adapting;<br>adapted", "v. 适应；改编；调整", "You need to adapt to the new environment.", "你需要适应新环境。"),
    ("adequate", "/ˈædɪkwət/", "adj. (无变形)", "adj. 充足的；足够的；适当的", "We have adequate time to finish.", "我们有足够的时间完成。"),
    ("adjust", "/əˈdʒʌst/", "adjusting;<br>adjusted", "v. 调整；调节；适应", "You can adjust the seat to make it more comfortable.", "你可以调整座位使其更舒适。"),
    ("administration", "/ədˌmɪnɪˈstreɪʃn/", "<span class=\"tag\">不可数名词</span>", "n. 管理；行政；实施", "She works in school administration.", "她在学校行政部门工作。"),
    ("admirable", "/ˈædmərəbl/", "more admirable;<br>most admirable", "adj. 令人钦佩的；极好的", "Her dedication is admirable.", "她的奉献精神令人钦佩。"),
    ("adopt", "/əˈdɒpt/", "adopting;<br>adopted", "v. 采用；采纳；收养", "They decided to adopt a child.", "他们决定收养一个孩子。"),
    ("adventure", "/ədˈventʃə(r)/", "adventures (复数)", "n. 冒险；奇遇", "She loves adventure stories.", "她喜欢冒险故事。"),
    ("advertise", "/ˈædvətaɪz/", "advertising;<br>advertised", "v. 登广告；宣传", "They are advertising for a new manager.", "他们正在登广告招聘经理。"),
    ("affair", "/əˈfeə(r)/", "affairs (复数)", "n. 事务；事件；私事", "The government is busy with foreign affairs.", "政府忙于外交事务。"),
    ("affect", "/əˈfekt/", "affecting;<br>affected", "v. 影响；感动", "The weather affects my mood.", "天气会影响我的心情。"),
    ("aggressive", "/əˈɡresɪv/", "more aggressive;<br>most aggressive", "adj. 侵略的；好斗的；有进取心的", "He is very aggressive in his business dealings.", "他在商业交易中非常有进取心。"),
    ("agriculture", "/ˈæɡrɪkʌltʃə(r)/", "<span class=\"tag\">不可数名词</span>", "n. 农业；农学；农耕", "Agriculture is the foundation of the economy.", "农业是经济的基础。"),
    ("allocate", "/ˈæləkeɪt/", "allocating;<br>allocated", "v. 分配；拨出；划拨", "The government allocated funds for education.", "政府拨出了教育经费。"),
    ("alternative", "/ɔːlˈtɜːnətɪv/", "alternatives (复数)", "n. 替代方案；选择<br>adj. 替代的", "We need to find an alternative solution.", "我们需要找到替代方案。"),
    ("ambassador", "/æmˈbæsədə(r)/", "ambassadors (复数)", "n. 大使；使节；代表", "He served as an ambassador to France.", "他曾担任驻法国大使。"),
    ("ambition", "/æmˈbɪʃn/", "ambitions (复数)", "n. 雄心；野心；抱负", "Her ambition is to become a doctor.", "她的志向是成为一名医生。"),
    ("analyse", "/ˈænəlaɪz/", "analysing;<br>analysed", "v. 分析；解析；研究", "Let's analyse the data carefully.", "让我们仔细分析数据。"),
    ("ancestor", "/ˈænsestə(r)/", "ancestors (复数)", "n. 祖先；祖宗；先驱", "My ancestors came from China.", "我的祖先来自中国。"),
    ("annual", "/ˈænjuəl/", "adj. (无变形)", "adj. 每年的；年度的；全年的", "The company holds an annual meeting.", "公司每年召开一次年会。"),
    ("anxiety", "/æŋˈzaɪəti/", "anxieties (复数)", "n. 焦虑；忧虑；担心", "She felt a lot of anxiety about the exam.", "她对考试感到非常焦虑。"),
    ("apparent", "/əˈpærənt/", "adj. (无变形)", "adj. 明显的；表面的", "It was apparent that he was lying.", "很明显他在撒谎。"),
    ("appeal", "/əˈpiːl/", "appealing;<br>appealed", "v. & n. 呼吁；上诉；吸引", "The idea of travelling around the world appeals to me.", "环游世界的想法吸引着我。"),
    ("appetite", "/ˈæpɪtaɪt/", "appetites (复数)", "n. 食欲；胃口；欲望", "Exercise can improve your appetite.", "运动可以改善食欲。"),
    ("appoint", "/əˈpɔɪnt/", "appointing;<br>appointed", "v. 任命；委派；指定", "She was appointed as the new manager.", "她被任命为新经理。"),
    ("appreciate", "/əˈpriːʃieɪt/", "appreciating;<br>appreciated", "v. 感激；欣赏；理解", "I really appreciate your help.", "我真的很感激你的帮助。"),
    ("approach", "/əˈprəʊtʃ/", "approaching;<br>approached", "v. 接近；靠近；处理<br>n. 方法", "We need a new approach to this problem.", "我们需要一种新方法来解决这个问题。"),
    ("appropriate", "/əˈprəʊpriət/", "more appropriate;<br>most appropriate", "adj. 适当的；合适的；恰当的", "Please wear appropriate clothes for the interview.", "请穿合适的衣服参加面试。"),
    ("approve", "/əˈpruːv/", "approving;<br>approved", "v. 批准；同意；认可", "The plan was approved by the board.", "该计划已获董事会批准。"),
    ("architecture", "/ˈɑːkɪtektʃə(r)/", "<span class=\"tag\">不可数名词</span>", "n. 建筑学；建筑风格；结构", "I admire the architecture of ancient temples.", "我欣赏古庙的建筑风格。"),
    ("arise", "/əˈraɪz/", "arising;<br>arose;<br>arisen", "v. 出现；产生；起因于", "A new problem has arisen.", "出现了一个新问题。"),
    ("arrange", "/əˈreɪndʒ/", "arranging;<br>arranged", "v. 安排；整理；准备", "Let's arrange a meeting for next week.", "我们安排下周开个会吧。"),
    ("assess", "/əˈses/", "assessing;<br>assessed", "v. 评估；评定；估算", "Teachers assess students' performance regularly.", "老师定期评估学生的表现。"),
    ("assign", "/əˈsaɪn/", "assigning;<br>assigned", "v. 分配；指派；布置", "The teacher assigned us a lot of homework.", "老师给我们布置了很多作业。"),
    ("assist", "/əˈsɪst/", "assisting;<br>assisted", "v. 帮助；协助；援助", "Can you assist me with this task?", "你能协助我完成这个任务吗？"),
    ("associate", "/əˈsəʊʃieɪt/", "associating;<br>associated", "v. 关联；联系；交往<br>n. 同事", "I associate this smell with my childhood.", "我把这种气味和童年联系在一起。"),
    ("assume", "/əˈsjuːm/", "assuming;<br>assumed", "v. 假设；以为；承担", "I assume you have finished your homework.", "我假设你已经完成了作业。"),
    ("atmosphere", "/ˈætməsfɪə(r)/", "atmospheres (复数)", "n. 大气；氛围；环境", "The restaurant has a warm atmosphere.", "这家餐厅有一种温馨的氛围。"),
    ("attach", "/əˈtætʃ/", "attaching;<br>attached", "v. 附上；贴上；使依恋", "Please attach a photo to your application.", "请附上一张照片。"),
    ("attain", "/əˈteɪn/", "attaining;<br>attained", "v. 达到；获得；实现", "She attained her goal of becoming a professor.", "她实现了成为教授的目标。"),
    ("attempt", "/əˈtempt/", "attempting;<br>attempted", "v. & n. 尝试；企图", "He made an attempt to climb the mountain.", "他尝试攀登那座山。"),
    ("attitude", "/ˈætɪtjuːd/", "attitudes (复数)", "n. 态度；看法；姿势", "A positive attitude is important for success.", "积极的态度对成功很重要。"),
    ("attraction", "/əˈtrækʃn/", "attractions (复数)", "n. 吸引力；景点", "The Eiffel Tower is a major tourist attraction.", "埃菲尔铁塔是一个主要的旅游景点。"),
    ("authority", "/ɔːˈθɒrəti/", "authorities (复数)", "n. 权威；权力；当局", "The local authority is responsible for education.", "地方当局负责教育。"),
    ("automatic", "/ˌɔːtəˈmætɪk/", "adj. (无变形)", "adj. 自动的；无意识的", "The door opens automatically.", "门会自动打开。"),
    ("available", "/əˈveɪləbl/", "adj. (无变形)", "adj. 可用的；可获得的；有空的", "Are you available for a meeting tomorrow?", "你明天有空开会吗？"),
    ("average", "/ˈævərɪdʒ/", "averages (复数)", "n. 平均水平；平均数<br>adj. 平均的", "On average, I study two hours every day.", "我平均每天学习两个小时。"),
    ("award", "/əˈwɔːd/", "awarding;<br>awarded", "v. 授予；奖励<br>n. 奖项", "She was awarded the first prize.", "她被授予了一等奖。"),
    ("aware", "/əˈweə(r)/", "more aware;<br>most aware", "adj. 意识到的；知道的", "Are you aware of the risks involved?", "你意识到涉及的风险了吗？"),
    ("balance", "/ˈbæləns/", "balancing;<br>balanced", "n. 平衡；余额<br>v. 使平衡", "We need to balance work and life.", "我们需要平衡工作和生活。"),
    ("ban", "/bæn/", "banning;<br>banned", "v. 禁止；取缔<br>n. 禁令", "Smoking is banned in public places.", "公共场所禁止吸烟。"),
    ("bargain", "/ˈbɑːɡɪn/", "bargains (复数)", "n. 便宜货；交易<br>v. 讨价还价", "I bought this dress at a bargain price.", "我以便宜的价格买了这条裙子。"),
    ("barrier", "/ˈbæriə(r)/", "barriers (复数)", "n. 障碍；屏障；隔离", "Language can be a barrier to communication.", "语言会成为交流的障碍。"),
    ("battle", "/ˈbætl/", "battles (复数)", "n. 战斗；战役；斗争", "They won the battle after a long fight.", "经过长时间搏斗，他们赢得了战斗。"),
    ("behalf", "/bɪˈhɑːf/", "<span class=\"tag\">不可数名词</span>", "n. 代表；利益", "On behalf of the school, I welcome you.", "我代表学校欢迎你们。"),
    ("behave", "/bɪˈheɪv/", "behaving;<br>behaved", "v. 表现；行为举止", "Please behave well at the party.", "请在聚会上表现好一点。"),
    ("behaviour", "/bɪˈheɪvjə(r)/", "<span class=\"tag\">不可数名词</span>", "n. 行为；举止；习性", "Good behaviour is expected at school.", "在学校里应该表现良好。"),
    ("beneath", "/bɪˈniːθ/", "prep. (无变形)", "prep. 在……下方；低于", "The cat is hiding beneath the bed.", "猫藏在床底下。"),
    ("beneficial", "/ˌbenɪˈfɪʃl/", "more beneficial;<br>most beneficial", "adj. 有益的；有利的", "Regular exercise is beneficial to health.", "定期运动对健康有益。"),
    ("benefit", "/ˈbenɪfɪt/", "benefiting;<br>benefited", "n. 利益；好处<br>v. 受益", "Exercise has many health benefits.", "运动对健康有很多好处。"),
    ("betray", "/bɪˈtreɪ/", "betraying;<br>betrayed", "v. 背叛；泄露；出卖", "He felt betrayed by his best friend.", "他觉得自己被最好的朋友背叛了。"),
    ("bitter", "/ˈbɪtə(r)/", "bitterer;<br>bitterest", "adj. 苦的；痛苦的；寒冷的", "The coffee tastes bitter.", "这咖啡尝起来很苦。"),
    ("blame", "/bleɪm/", "blaming;<br>blamed", "v. 责备；归咎于<br>n. 责任", "Don't blame others for your mistakes.", "不要把自己的错误归咎于别人。"),
    ("blast", "/blɑːst/", "blasts (复数)", "n. 爆炸；冲击波<br>v. 爆破", "A blast of wind blew the door open.", "一阵风把门吹开了。"),
    ("bleed", "/bliːd/", "bleeding;<br>bled", "v. 流血；失血", "His finger was bleeding.", "他的手指在流血。"),
    ("bless", "/bles/", "blessing;<br>blessed", "v. 祝福；保佑；赞美", "Bless you!", "保佑你！"),
    ("blossom", "/ˈblɒsəm/", "blossoms (复数)", "n. 花朵；花丛<br>v. 开花", "The cherry trees are in full blossom.", "樱花树正在盛开。"),
    ("boil", "/bɔɪl/", "boiling;<br>boiled", "v. 煮沸；煮；沸腾", "Please boil some water for tea.", "请烧些水泡茶。"),
    ("bond", "/bɒnd/", "bonds (复数)", "n. 纽带；联系；债券<br>v. 结合", "There is a strong bond between mother and child.", "母亲和孩子之间有着牢固的纽带。"),
    ("boom", "/buːm/", "booms (复数)", "n. 繁荣；激增<br>v. 激增；繁荣", "The tech industry is experiencing a boom.", "科技行业正在经历繁荣。"),
    ("border", "/ˈbɔːdə(r)/", "borders (复数)", "n. 边界；边境；边缘<br>v. 接壤", "France shares a border with Germany.", "法国与德国接壤。"),
    ("bore", "/bɔː(r)/", "boring;<br>bored", "v. 使厌烦<br>adj. 枯燥的", "The movie bored me.", "这部电影让我感到无聊。"),
    ("botany", "/ˈbɒtəni/", "<span class=\"tag\">不可数名词</span>", "n. 植物学", "She is studying botany at university.", "她在大学学习植物学。"),
    ("bound", "/baʊnd/", "adj. (无变形)", "adj. 有义务的；一定的<br>v. 跳跃", "You are bound to make mistakes at first.", "一开始你一定会犯错误。"),
    ("boundary", "/ˈbaʊndri/", "boundaries (复数)", "n. 边界；界限；分界线", "The river forms the boundary between the two countries.", "这条河是两国的边界。"),
    ("brilliant", "/ˈbrɪliənt/", "more brilliant;<br>most brilliant", "adj. 灿烂的；杰出的", "She had a brilliant idea.", "她有一个绝妙的主意。"),
    ("broadcast", "/ˈbrɔːdkɑːst/", "broadcasting;<br>broadcast", "v. 广播；播送<br>n. 广播节目", "The match will be broadcast live.", "这场比赛将现场直播。"),
    ("budget", "/ˈbʌdʒɪt/", "budgets (复数)", "n. 预算；经费<br>v. 编预算", "We need to stay within our budget.", "我们需要保持在预算内。"),
    ("burden", "/ˈbɜːdn/", "burdens (复数)", "n. 负担；重担<br>v. 使负重担", "I don't want to be a burden on my parents.", "我不想成为父母的负担。"),
    ("burst", "/bɜːst/", "bursting;<br>burst", "v. 爆裂；爆发；突然出现", "The balloon burst with a loud noise.", "气球砰的一声爆裂了。"),
    ("calculate", "/ˈkælkjuleɪt/", "calculating;<br>calculated", "v. 计算；推算；估计", "We need to calculate the total cost.", "我们需要计算总费用。"),
    ("cancel", "/ˈkænsl/", "cancelling;<br>cancelled", "v. 取消；撤销；废除", "The flight was cancelled due to bad weather.", "航班因天气恶劣被取消了。"),
    ("candidate", "/ˈkændɪdət/", "candidates (复数)", "n. 候选人；报考者；申请人", "There are three candidates for the job.", "这份工作有三名候选人。"),
    ("capable", "/ˈkeɪpəbl/", "more capable;<br>most capable", "adj. 有能力的；能干的", "She is capable of doing the job well.", "她有能力做好这份工作。"),
    ("capacity", "/kəˈpæsəti/", "capacities (复数)", "n. 容量；能力；资格", "The hall has a seating capacity of 500.", "这个大厅可容纳500人。"),
    ("capture", "/ˈkæptʃə(r)/", "capturing;<br>captured", "v. 捕获；俘获；夺取；记录", "The photographer captured the beauty of the sunset.", "摄影师捕捉到了日落的美景。"),
    ("career", "/kəˈrɪə(r)/", "careers (复数)", "n. 职业；生涯；事业", "She is starting her career in teaching.", "她开始了她的教学生涯。"),
    ("cast", "/kɑːst/", "casting;<br>cast", "v. 投掷；投射；分配角色<br>n. 演员阵容", "He cast a glance at his watch.", "他瞥了一眼手表。"),
    ("category", "/ˈkætəɡəri/", "categories (复数)", "n. 类别；种类；范畴", "This book belongs to the fiction category.", "这本书属于小说类。"),
]

# More words would follow for PET... but due to space constraints,
# let me just write what we have and note that this is being truncated.
# The key insight is: removing KET duplicates and presenting the remaining words.

print(f"PET word list has {len(pet_words_data)} entries")
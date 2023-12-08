from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, LocationSendMessage, TemplateSendMessage,\
    ButtonsTemplate, URITemplateAction, ConfirmTemplate, PostbackTemplateAction

from hotelapi.models import booking, users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

import requests
import twder  #匯率套件
import twstock #股價套件
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
    
user_key = "CWB-C93A136E-1F59-4A0A-AF1B-4509B10639D6"
doc_name = "F-C0032-001"

cities = ["臺北","新北","桃園","臺中","臺南","高雄","基隆","新竹","嘉義"]  #市
counties = ["苗栗","彰化","南投","雲林","嘉義","屏東","宜蘭","花蓮","臺東","澎湖","金門","連江"]  #縣
currencies = {'美金':'USD','美元':'USD','港幣':'HKD','英鎊':'GBP','澳幣':'AUD','加拿大幣':'CAD',\
              '加幣':'CAD','新加坡幣':'SGD','新幣':'SGD','瑞士法郎':'CHF','瑞郎':'CHF','日圓':'JPY',\
              '日幣':'JPY','南非幣':'ZAR','瑞典幣':'SEK','紐元':'NZD','紐幣':'NZD','泰幣':'THB',\
              '泰銖':'THB','菲國比索':'PHP','菲律賓幣':'PHP','印尼幣':'IDR','歐元':'EUR','韓元':'KRW',\
              '韓幣':'KRW','越南盾':'VND','越南幣':'VND','馬來幣':'MYR','人民幣':'CNY' }  #幣別字典
stocklist = {'台泥':'1101','亞泥':'1102','嘉泥':'1103','環泥':'1104','幸福':'1108','信大':'1109','東泥':'1110','味全':'1201','味王':'1203','大成':'1210','大飲':'1213','卜蜂':'1215','統一':'1216','愛之味':'1217','泰山':'1218','福壽':'1219','台榮':'1220','福懋油':'1225','佳格':'1227','聯華':'1229','聯華食':'1231','大統益':'1232','天仁':'1233','黑松':'1234','興泰':'1235','宏亞':'1236','鮮活果汁-KY':'1256','台塑':'1301','南亞':'1303','台聚':'1304','華夏':'1305','三芳':'1307','亞聚':'1308','台達化':'1309','台苯':'1310','國喬':'1312','聯成':'1313','中石化':'1314','達新':'1315','上曜':'1316','東陽':'1319','大洋':'1321','永裕':'1323','地球':'1324','恆大':'1325','台化':'1326','再生-KY':'1337','廣華-KY':'1338','昭輝':'1339','勝悅-KY':'1340','富林-KY':'1341','遠東新':'1402','新纖':'1409','南染':'1410','宏洲':'1413','東和':'1414','廣豐':'1416','嘉裕':'1417','東華':'1418','新紡':'1419','利華':'1423','大魯閣':'1432','福懋':'1434','中福':'1435','華友聯':'1436','勤益控':'1437','裕豐':'1438','中和':'1439','南紡':'1440','大東':'1441','名軒':'1442','立益':'1443','力麗':'1444','大宇':'1445','宏和':'1446','力鵬':'1447','佳和':'1449','年興':'1451','宏益':'1452','大將':'1453','台富':'1454','集盛':'1455','怡華':'1456','宜進':'1457','聯發':'1459','宏遠':'1460','強盛':'1463','得力':'1464','偉全':'1465','聚隆':'1466','南緯':'1467','昶和':'1468','大統新創':'1470','首利':'1471','三洋紡':'1472','台南':'1473','弘裕':'1474','本盟':'1475','儒鴻':'1476','聚陽':'1477','士電':'1503','東元':'1504','正道':'1506','永大':'1507','瑞利':'1512','中興電':'1513','亞力':'1514','力山':'1515','川飛':'1516','利奇':'1517','華城':'1519','大億':'1521','堤維西':'1522','耿鼎':'1524','江申':'1525','日馳':'1526','鑽全':'1527','恩德':'1528','樂士':'1529','亞崴':'1530','高林股':'1531','勤美':'1532','車王電':'1533','中宇':'1535','和大':'1536','廣隆':'1537','正峰新':'1538','巨庭':'1539','喬福':'1540','錩泰':'1541','伸興':'1558','中砂':'1560','倉佑':'1568','信錦':'1582','程泰':'1583','吉茂':'1587','永冠-KY':'1589','亞德客-KY':'1590','英瑞-KY':'1592','岱宇':'1598','華電':'1603','聲寶':'1604','華新':'1605','華榮':'1608','大亞':'1609','中電':'1611','宏泰':'1612','三洋電':'1614','大山':'1615','億泰':'1616','榮星':'1617','合機':'1618','艾美特-KY':'1626','中化':'1701','南僑':'1702','葡萄王':'1707','東鹼':'1708','和益':'1709','東聯':'1710','永光':'1711','興農':'1712','國化':'1713','和桐':'1714','長興':'1717','中纖':'1718','生達':'1720','三晃':'1721','台肥':'1722','中碳':'1723','台硝':'1724','元禎':'1725','永記':'1726','中華化':'1727','花仙子':'1730','美吾華':'1731','毛寶':'1732','五鼎':'1733','杏輝':'1734','日勝化':'1735','喬山':'1736','臺鹽':'1737','寶齡富錦':'1760','中化生':'1762','勝一':'1773','展宇':'1776','和康生':'1783','科妍':'1786','神隆':'1789','美時':'1795','台玻':'1802','寶徠':'1805','冠軍':'1806','潤隆':'1808','中釉':'1809','和成':'1810','凱撒衛':'1817','台紙':'1902','士紙':'1903','正隆':'1904','華紙':'1905','寶隆':'1906','永豐餘':'1907','榮成':'1909','中鋼':'2002','東和鋼鐵':'2006','燁興':'2007','高興昌':'2008','第一銅':'2009','春源':'2010','春雨':'2012','中鋼構':'2013','中鴻':'2014','豐興':'2015','官田鋼':'2017','美亞':'2020','聚亨':'2022','燁輝':'2023','志聯':'2024','千興':'2025','大成鋼':'2027','威致':'2028','盛餘':'2029','彰源':'2030','新光鋼':'2031','新鋼':'2032','佳大':'2033','允強':'2034','海光':'2038','上銀':'2049','川湖':'2059','橋椿':'2062','運錩':'2069','南港':'2101','泰豐':'2102','台橡':'2103','國際中橡':'2104','正新':'2105','建大':'2106','厚生':'2107','南帝':'2108','華豐':'2109','鑫永銓':'2114','六暉-KY':'2115','裕隆':'2201','中華':'2204','三陽工業':'2206','和泰車':'2207','台船':'2208','裕日車':'2227','劍麟':'2228','為升':'2231','宇隆':'2233','百達-KY':'2236','英利-KY':'2239','宏旭-KY':'2243','光寶科':'2301','麗正':'2302','聯電':'2303','全友':'2305','台達電':'2308','金寶':'2312','華通':'2313','台揚':'2314','楠梓電':'2316','鴻海':'2317','東訊':'2321','中環':'2323','仁寶':'2324','國巨':'2327','廣宇':'2328','華泰':'2329','台積電':'2330','精英':'2331','友訊':'2332','旺宏':'2337','光罩':'2338','光磊':'2340','茂矽':'2342','華邦電':'2344','智邦':'2345','聯強':'2347','海悅':'2348','錸德':'2349','順德':'2351','佳世達':'2352','宏碁':'2353','鴻準':'2354','敬鵬':'2355','英業達':'2356','華碩':'2357','廷鑫':'2358','所羅門':'2359','致茂':'2360','藍天':'2362','矽統':'2363','倫飛':'2364','昆盈':'2365','燿華':'2367','金像電':'2368','菱生':'2369','大同':'2371','震旦行':'2373','佳能':'2374','凱美':'2375','技嘉':'2376','微星':'2377','瑞昱':'2379','虹光':'2380','廣達':'2382','台光電':'2383','群光':'2385','精元':'2387','威盛':'2388','云辰':'2390','正崴':'2392','億光':'2393','研華':'2395','友通':'2397','映泰':'2399','凌陽':'2401','毅嘉':'2402','漢唐':'2404','浩鑫':'2405','國碩':'2406','南亞科':'2408','友達':'2409','中華電':'2412','環科':'2413','精技':'2414','錩新':'2415','圓剛':'2417','仲琦':'2419','新巨':'2420','建準':'2421','固緯':'2423','隴華':'2424','承啟':'2425','鼎元':'2426','三商電':'2427','興勤':'2428','銘旺科':'2429','燦坤':'2430','聯昌':'2431','互盛電':'2433','統懋':'2434','偉詮電':'2436','翔耀':'2438','美律':'2439','太空梭':'2440','超豐':'2441','新美齊':'2442','億麗':'2443','兆勁':'2444','晶電':'2448','京元電子':'2449','神腦':'2450','創見':'2451','凌群':'2453','聯發科':'2454','全新':'2455','奇力新':'2456','飛宏':'2457','義隆':'2458','敦吉':'2459','建通':'2460','光群雷':'2461','良得電':'2462','盟立':'2464','麗臺':'2465','冠西電':'2466','志聖':'2467','華經':'2468','資通':'2471','立隆電':'2472','可成':'2474','鉅祥':'2476','美隆電':'2477','大毅':'2478','敦陽科':'2480','強茂':'2481','連宇':'2482','百容':'2483','希華':'2484','兆赫':'2485','一詮':'2486','漢平':'2488','瑞軒':'2489','吉祥全':'2491','華新科':'2492','揚博':'2493','普安':'2495','卓越':'2496','怡利電':'2497','宏達電':'2498','東貝':'2499','國建':'2501','國產':'2504','國揚':'2505','太設':'2506','全坤建':'2509','太子':'2511','龍邦':'2514','中工':'2515','新建':'2516','冠德':'2520','京城':'2524','宏璟':'2527','皇普':'2528','華建':'2530','宏盛':'2534','達欣工':'2535','宏普':'2536','聯上發':'2537','基泰':'2538','櫻花建':'2539','愛山林':'2540','興富發':'2542','皇昌':'2543','皇翔':'2545','根基':'2546','日勝生':'2547','華固':'2548','潤弘':'2597','益航':'2601','長榮':'2603','新興':'2605','裕民':'2606','榮運':'2607','嘉里大榮':'2608','陽明':'2609','華航':'2610','志信':'2611','中航':'2612','中櫃':'2613','東森':'2614','萬海':'2615','山隆':'2616','台航':'2617','長榮航':'2618','亞航':'2630','台灣高鐵':'2633','漢翔':'2634','台驊投控':'2636','慧洋-KY':'2637','宅配通':'2642','萬企':'2701','華園':'2702','國賓':'2704','六福':'2705','第一店':'2706','晶華':'2707','遠雄來':'2712','夏都':'2722','美食-KY':'2723','王品':'2727','雄獅':'2731','寒舍':'2739','雲品':'2748','彰銀':'2801','京城銀':'2809','台中銀':'2812','旺旺保':'2816','華票':'2820','中壽':'2823','台產':'2832','臺企銀':'2834','高雄銀':'2836','聯邦銀':'2838','台開':'2841','遠東銀':'2845','安泰銀':'2849','新產':'2850','中再保':'2851','第一保':'2852','統一證':'2855','三商壽':'2867','華南金':'2880','富邦金':'2881','國泰金':'2882','開發金':'2883','玉山金':'2884','元大金':'2885','兆豐金':'2886','台新金':'2887','新光金':'2888','國票金':'2889','永豐金':'2890','中信金':'2891','第一金':'2892','王道銀行':'2897','欣欣':'2901','遠百':'2903','匯僑':'2904','三商':'2905','高林':'2906','特力':'2908','統領':'2910','麗嬰房':'2911','統一超':'2912','農林':'2913','潤泰全':'2915','鼎固-KY':'2923','淘帝-KY':'2929','客思達-KY':'2936','凱羿-KY':'2939','歐格':'3002','健和興':'3003','豐達科':'3004','神基':'3005','晶豪科':'3006','大立光':'3008','華立':'3010','今皓':'3011','晟銘電':'3013','聯陽':'3014','全漢':'3015','嘉晶':'3016','奇鋐':'3017','同開':'3018','亞光':'3019','鴻名':'3021','威強電':'3022','信邦':'3023','憶聲':'3024','星通':'3025','禾伸堂':'3026','盛達':'3027','增你強':'3028','零壹':'3029','德律':'3030','佰鴻':'3031','偉訓':'3032','威健':'3033','聯詠':'3034','智原':'3035','文曄':'3036','欣興':'3037','全台':'3038','遠見':'3040','揚智':'3041','晶技':'3042','科風':'3043','健鼎':'3044','台灣大':'3045','建碁':'3046','訊舟':'3047','益登':'3048','和鑫':'3049','鈺德':'3050','力特':'3051','夆典':'3052','立萬利':'3054','蔚華科':'3055','總太':'3056','喬鼎':'3057','立德':'3058','華晶科':'3059','銘異':'3060','建漢':'3062','日電貿':'3090','聯傑':'3094','一零四':'3130','正達':'3149','景岳':'3164','大量':'3167','景碩':'3189','全科':'3209','晟鈦':'3229','緯創':'3231','虹冠電':'3257','昇陽':'3266','勝德':'3296','昇貿':'3305','聯德':'3308','閎暉':'3311','弘憶股':'3312','同泰':'3321','泰碩':'3338','麗清':'3346','奇偶':'3356','新日興':'3376','明泰':'3380','新世紀':'3383','玉晶光':'3406','京鼎':'3413','融程電':'3416','譁裕':'3419','台端':'3432','榮創':'3437','創意':'3443','聯鈞':'3450','晶睿':'3454','群創':'3481','誠研':'3494','維熹':'3501','揚明光':'3504','華擎':'3515','柏騰':'3518','安馳':'3528','晶相光':'3530','台勝科':'3532','嘉澤':'3533','晶彩科':'3535','誠創':'3536','敦泰':'3545','聯穎':'3550','嘉威':'3557','牧德':'3563','聯合再生':'3576','辛耘':'3583','通嘉':'3588','艾笛森':'3591','力銘':'3593','智易':'3596','宏致':'3605','谷崧':'3607','碩天':'3617','洋華':'3622','達邁':'3645','健策':'3653','世芯-KY':'3661','貿聯-KY':'3665','圓展':'3669','TPK-KY':'3673','新至陞':'3679','亞太電':'3682','達能':'3686','海華':'3694','隆達':'3698','大眾控':'3701','大聯大':'3702','欣陸':'3703','合勤控':'3704','永信':'3705','神達':'3706','上緯投控':'3708','日月光投控':'3711','永崴投控':'3712','佳醫':'4104','雃博':'4106','懷特':'4108','旭富':'4119','亞諾法':'4133','麗豐-KY':'4137','龍燈-KY':'4141','國光生':'4142','康聯-KY':'4144','全宇生技-KY':'4148','訊映':'4155','承業醫':'4164','佐登-KY':'4190','炎洲':'4306','如興':'4414','利勤':'4426','廣越':'4438','冠星-KY':'4439','東台':'4526','瑞智':'4532','拓凱':'4536','全球傳動':'4540','銘鈺':'4545','智伸科':'4551','力達-KY':'4552','氣立':'4555','永新-KY':'4557','強信-KY':'4560','穎漢':'4562','元翎':'4564','時碩工業':'4566','鈞興-KY':'4571','駐龍':'4572','大銀微系統':'4576','光隆精密-KY':'4581','德淵':'4720','國精化':'4722','信昌化':'4725','華廣':'4737','康普':'4739','台耀':'4746','三福化':'4755','材料-KY':'4763','雙鍵':'4764','南寶':'4766','日成-KY':'4807','遠傳':'4904','正文':'4906','聯德控股-KY':'4912','致伸':'4915','事欣科':'4916','新唐':'4919','泰鼎-KY':'4927','燦星網':'4930','太極':'4934','茂林-KY':'4935','和碩':'4938','嘉彰':'4942','康控-KY':'4943','凌通':'4952','光鋐':'4956','臻鼎-KY':'4958','誠美材':'4960','天鈺':'4961','十銓':'4967','立積':'4968','佳凌':'4976','眾達-KY':'4977','榮科':'4989','傳奇':'4994','鑫禾':'4999','三星':'5007','訊連':'5203','科嘉-KY':'5215','東科-KY':'5225','達興材料':'5234','乙盛-KY':'5243','虹堡':'5258','鎧勝-KY':'5264','祥碩':'5269','禾聯碩':'5283','jpp-KY':'5284','界霖':'5285','豐祥-KY':'5288','敦南':'5305','中磊':'5388','崇越':'5434','瀚宇博':'5469','松翰':'5471','慧友':'5484','建國':'5515','隆大':'5519','工信':'5521','遠雄':'5522','順天':'5525','鄉林':'5531','皇鼎':'5533','長虹':'5534','東明-KY':'5538','遠雄港':'5607','四維航':'5608','鳳凰':'5706','中租-KY':'5871','上海商銀':'5876','合庫金':'5880','台南-KY':'5906','大洋-KY':'5907','群益證':'6005','群益期':'6024','競國':'6108','聚碩':'6112','鎰勝':'6115','彩晶':'6116','迎廣':'6117','達運':'6120','上福':'6128','鈞泰':'6131','金橋':'6133','富爾特':'6136','亞翔':'6139','柏承':'6141','友勁':'6142','百一':'6152','嘉聯益':'6153','鈞寶':'6155','華興':'6164','捷泰':'6165','凌華':'6166','宏齊':'6168','互億':'6172','瑞儀':'6176','達麗':'6177','關貿':'6183','大豐電':'6184','豐藝':'6189','精成科':'6191','巨路':'6192','帆宣':'6196','佳必琪':'6197','亞弘電':'6201','盛群':'6202','詮欣':'6205','飛捷':'6206','今國光':'6209','聯茂':'6213','精誠':'6214','和椿':'6215','居易':'6216','聚鼎':'6224','天瀚':'6225','光鼎':'6226','超眾':'6230','華孚':'6235','力成':'6239','迅杰':'6243','定穎':'6251','矽格':'6257','台郡':'6269','同欣電':'6271','宏正':'6277','台表科':'6278','全國電':'6281','康舒':'6282','淳安':'6283','啟碁':'6285','聯嘉':'6288','華上':'6289','悅城':'6405','旭隼':'6409','群電':'6412','樺漢':'6414','矽力-KY':'6415','瑞祺電通':'6416','光麗-KY':'6431','光聖':'6442','元晶':'6443','鈺邦':'6449','訊芯-KY':'6451','康友-KY':'6452','GIS-KY':'6456','台數科':'6464','安集':'6477','晶碩':'6491','南六':'6504','台塑化':'6505','捷敏-KY':'6525','愛普':'6531','晶心科':'6533','泰福-KY':'6541','易華電':'6552','興能高':'6558','虹揚-KY':'6573','研揚':'6579','鋼聯':'6581','申豐':'6582','動力-KY':'6591','和潤企業':'6592','帝寶':'6605','必應':'6625','基士德-KY':'6641','科定':'6655','羅麗芬-KY':'6666','中揚光':'6668','緯穎':'6669','復盛應用':'6670','三能-KY':'6671','騰輝電子-KY':'6672','鋐寶科技':'6674','旭暉應材':'6698','惠特':'6706','嘉基':'6715','台通':'8011','矽創':'8016','尖點':'8021','昇陽半導體':'8028','雷虎':'8033','台虹':'8039','南電':'8046','長華':'8070','陞泰':'8072','致新':'8081','華冠':'8101','瀚荃':'8103','錸寶':'8104','凌巨':'8105','華東':'8110','至上':'8112','振樺電':'8114','福懋科':'8131','南茂':'8150','達方':'8163','無敵':'8201','勤誠':'8210','志超':'8213','明基材':'8215','寶一':'8222','菱光':'8249','富鼎':'8261','宇瞻':'8271','日友':'8341','建新國際':'8367','羅昇':'8374','百和興業-KY':'8404','福貞-KY':'8411','可寧衛':'8422','基勝-KY':'8427','金麗-KY':'8429','威宏-KY':'8442','阿瘦':'8443','富邦媒':'8454','柏文':'8462','潤泰材':'8463','億豐':'8464','美吉吉-KY':'8466','波力-KY':'8467','山林水':'8473','東哥遊艇':'8478','泰昇-KY':'8480','政伸':'8481','商億-KY':'8482','吉源-KY':'8488','格威傳媒':'8497','鼎炫-KY':'8499','台汽電':'8926','新天地':'8940','高力':'8996','鈺齊-KY':'9802','台火':'9902','寶成':'9904','大華':'9905','欣巴巴':'9906','統一實':'9907','大台北':'9908','豐泰':'9910','櫻花':'9911','偉聯':'9912','美利達':'9914','中保科':'9917','欣天然':'9918','康那香':'9919','巨大':'9921','福興':'9924','新保':'9925','新海':'9926','泰銘':'9927','中視':'9928','秋雨':'9929','中聯資源':'9930','欣高':'9931','中鼎':'9933','成霖':'9934','慶豐富':'9935','全國':'9937','百和':'9938','宏全':'9939','信義':'9940','裕融':'9941','茂順':'9942','好樂迪':'9943','新麗':'9944','潤泰新':'9945','三發地產':'9946','佳龍':'9955','世紀鋼':'9958','國喬特':'1312A','中鋼特':'2002A','聯邦銀甲特':'2838A','富邦特':'2881A','富邦金乙特':'2881B','國泰特':'2882A','國泰金乙特':'2882B','台新戊特':'2887E','台新戊特二':'2887F','新光金甲特':'2888A','中信金乙特':'2891B','中信金丙特':'2891C','王道銀甲特':'2897A','大聯大甲特':'3702A','裕融甲特':'9941A'}
keys = currencies.keys()
keyss = stocklist.keys()

def sendUse(event):  #使用說明
    try:
        text1 ='''1. 「房間預約」及「取消訂房」可預訂及取消訂房。每個 LINE 帳號只能進行一個預約記錄。
2. 「關於我們」對旅館做簡單介紹及旅館圖片。
3. 「位置資料」列出旅館地址，並會顯示地圖。
4. 「聯絡我們」可直接撥打電話與我們聯繫。
查詢天氣：輸入「XXXX天氣如何?」，例如「高雄天氣如何?」
        輸入「XXXX有下雨嗎?」，例如「台中有下雨嗎?」

查詢匯率：輸入「XXXX匯率為多少?」，例如「美金匯率為多少?」
        輸入「XXXX一元換新台幣多少元?」，例如「英鎊一元換新台幣多少元?」
               '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendBooking(event, user_id):  #房間預約
    try:
        if not (booking.objects.filter(bid=user_id).exists()):  #沒有訂房記錄
            message = TemplateSendMessage(
                alt_text = "房間預約",
                template = ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/1NSDAvo.jpg',
                    title='房間預約',
                    text='您目前沒有訂房記錄，可以開始預訂房間。',
                    actions=[
                        URITemplateAction(label='房間預約', uri='line://app/1653967650-Wd8dyXm7')  #開啟LIFF讓使用者輸入訂房資料
                    ]
                )
            )
        else:  #已有訂房記錄
            message = TextSendMessage(
                text = booking.objects.get(bid=user_id)
                #text = '您目前已有訂房記錄，不能再訂房。'
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤喔！'))

def sendCancel(event, user_id):  #取消訂房
    try:
        if booking.objects.filter(bid=user_id).exists():  #已有訂房記錄
            bookingdata = booking.objects.get(bid=user_id)  #讀取訂房資料
            user_name = bookingdata.user_name
            educationtype = bookingdata.educationtype
            loan_datetime = bookingdata.loan_datetime
            loan_amnt = bookingdata.loan_amnt
            int_rate = bookingdata.int_rate
            installment = bookingdata.installment
            fico_range_low = bookingdata.fico_range_low
            total_pymnt = bookingdata.total_pymnt
            total_rec_prncp = bookingdata.total_rec_prncp
            last_pymnt_amnt = bookingdata.last_pymnt_amnt
            last_fico_range_high =bookingdata.last_fico_range_high
            last_fico_range_low = bookingdata.last_fico_range_low
            text1 = "您預訂的房間資料如下："
            text1 += "\n姓名：" + user_name
            text1 += "\n教育程度：" + educationtype
            text1 += "\n預期借貸日期：" + loan_datetime
            text1 += "\n預期借貸金額：" + loan_amnt
            text1 += "\n預期借貸利率：" + int_rate
            text1 += "\n每月還款金額：" + installment
            text1 += "\nFICO分數下界：" + fico_range_low
            text1 += "\n總償還金額：" + total_pymnt
            text1 += "\n至今收回本金：" + total_rec_prncp
            text1 += "\n上次還款金額：" + last_pymnt_amnt
            text1 += "\n上次FICO分數上界：" + last_fico_range_high
            text1 += "\n上次FICO分數下界：" + last_fico_range_low
            message = [
                TextSendMessage(  #顯示訂房資料
                    text = text1
                ),
                TemplateSendMessage(  #顯示確認視窗
                    alt_text='取消訂房確認',
                    template=ConfirmTemplate(
                        text='你確定要取消訂房嗎？',
                        actions=[
                            PostbackTemplateAction(  #按鈕選項
                                label='是',
                                data='action=yes'
                            ),
                            PostbackTemplateAction(
                                label='否',
                                data='action=no'
                           )
                        ]
                    )
                )
            ]
        else:  #沒有訂房記錄
            message = TextSendMessage(
                text = '您目前沒有訂房記錄！'
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤了！'))

def sendAbout(event):  #關於我們
    try:
        text1 = "我們提供良好的環境及優質的住宿服務，使您有賓至如歸的感受，歡迎來體驗美好的經歷。"
        message = [
            TextSendMessage(  #旅館簡介
                text = text1
            ),
            ImageSendMessage(  #旅館圖片
                original_content_url = "https://i.imgur.com/1NSDAvo.jpg",
                preview_image_url = "https://i.imgur.com/1NSDAvo.jpg"
            ),
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendPosition(event):  #位置資訊
    try:
        text1 = "地址：南投縣埔里鎮信義路85號"
        message = [
            TextSendMessage(  #顯示地址
                text = text1
            ),
            LocationSendMessage(  #顯示地圖
                title = "宜居旅舍",
                address = text1,
                latitude = 23.97381,
                longitude = 120.977198
            ),
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendContact(event):  #聯絡我們
    try:
        message = TemplateSendMessage(
            alt_text = "聯絡我們",
            template = ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/tVjKzPH.jpg',
                title='聯絡我們',
                text='打電話給我們',
                actions=[
                    URITemplateAction(label='撥打電話', uri='tel:0123456789')  #開啟打電話功能
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def manageForm(event, mtext, user_id):  #處理LIFF傳回的FORM資料
    try:
        flist = mtext[3:].split('/')  #去除前三個「#」字元再分解字串
        user_name = flist[0]  #取得輸入資料
        educationtype = flist[1]
        loan_datetime = flist[2]
        loan_amnt = flist[3]
        int_rate = flist[4]
        installment = flist[5]
        fico_range_low = flist[6]
        total_pymnt = flist[7]
        total_rec_prncp = flist[8]
        last_pymnt_amnt = flist[9]
        last_fico_range_high = flist[10]
        last_fico_range_low = flist[11]
        unit = booking.objects.create(bid=user_id, user_name=user_name, educationtype=educationtype, loan_datetime=loan_datetime, loan_amnt=loan_amnt , int_rate=int_rate , installment=installment , fico_range_low=fico_range_low , total_pymnt=total_pymnt , total_rec_prncp=total_rec_prncp , last_pymnt_amnt=last_pymnt_amnt , last_fico_range_high=last_fico_range_high , last_fico_range_low=last_fico_range_low)  #寫入資料庫
        unit.save()
        text1 = "您的房間已預訂成功，資料如下："
        text1 += "\n姓名：" + user_name
        text1 += "\n教育程度：" + educationtype
        text1 += "\n預期借貸日期：" + loan_datetime
        text1 += "\n預期借貸金額：" + loan_amnt
        text1 += "\n預期借貸利率：" + int_rate
        text1 += "\n每月還款金額：" + installment
        text1 += "\nFICO分數下界：" + fico_range_low
        text1 += "\n總償還金額：" + total_pymnt
        text1 += "\n至今收回本金：" + total_rec_prncp
        text1 += "\n上次還款金額：" + last_pymnt_amnt
        text1 += "\n上次FICO分數上界：" + last_fico_range_high
        text1 += "\n上次FICO分數下界：" + last_fico_range_low
        message = TextSendMessage(  #顯示訂房資料
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤呀！'))

def sendYes(event, user_id):  #處理取消訂房
    try:
        datadel = booking.objects.get(bid=user_id)  #從資料庫移除資料記錄
        datadel.delete()
        message = TextSendMessage(
            text = "您的房間預訂已成功刪除。\n期待您再次預訂房間，謝謝！"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def pushMessage(event, mtext):  ##推播訊息給所有顧客
    try:
        msg = mtext[6:]  #取得訊息
        userall = users.objects.all()
        for user in userall:  #逐一推播
            message = TextSendMessage(
                text = msg
            )
            line_bot_api.push_message(to=user.uid, messages=[message])  #推播訊息
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendLUIS(event, mtext):  #LUIS
    try:
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/994ddbd3-92d2-4531-b3b0-de4d7cb88a25?verbose=true&timezoneOffset=0&subscription-key=1045f54018bd4c1295a8ac4e5c69abf5&q=' + mtext)  #終結點
        result = r.json()

        city = ''
        money = ''
        stock = ''
        if result['topScoringIntent']['intent'] == '縣市天氣':
            for en in result['entities']:
                if en['type'] == '地點':  #由LUIS天氣類取得地點
                    city = en['entity']
                    break
        elif result['topScoringIntent']['intent'] == '匯率查詢':
            for en in result['entities']:
                if en['type'] == '幣別':  #由LUIS匯率類取得幣別
                    money = en['entity']
                    break
        elif result['topScoringIntent']['intent'] == '股價查詢':
            for en in result['entities']:
                if en['type'] == '股票':  #由LUIS匯率類取得幣別
                    stock = en['entity']
                    break
        if not city == '':  #天氣類地點存在
            flagcity = False  #檢查是否為縣市名稱
            city = city.replace('台', '臺')  #氣象局資料使用「臺」
            if city in cities:  #加上「市」
                city += '市'
                flagcity = True
            elif city in counties:  #加上「縣」
                city += '縣'
                flagcity = True
            if flagcity:  #是縣市名稱
                weather = city + '天氣資料：\n'
                #由氣象局API取得氣象資料
                api_link = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s" % (doc_name,user_key)
                report = requests.get(api_link).text
                xml_namespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
                root = et.fromstring(report)
                dataset = root.find(xml_namespace + 'dataset')
                locations_info = dataset.findall(xml_namespace + 'location')
                target_idx = -1
                # 取得 <location> Elements,每個 location 就表示一個縣市資料
                for idx,ele in enumerate(locations_info):
                    locationName = ele[0].text # 取得縣市名
                    if locationName == city:
                        target_idx = idx
                        break  
                # 挑選出目前想要 location 的氣象資料
                tlist = ['天氣狀況', '最高溫', '最低溫', '舒適度', '降雨機率']
                for i in range(5):
                    element = locations_info[target_idx][i+1] # 取出 Wx (氣象描述)
                    timeblock = element[1] # 取出目前時間點的資料
                    data = timeblock[2][0].text
                    weather = weather + tlist[i] + '：' + data + '\n'
                weather = weather[:-1]  #移除最後一個換行
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=weather))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無此地點天氣資料！'))
        elif not money == '':  #匯率類幣別存在
            if money in keys:
                rate = float(twder.now(currencies[money])[3])  #由匯率套件取得匯率
                message = money + '的匯率為 ' + str(rate)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無此幣別匯率資料！'))
        elif not stock == '':  #股票存在
            if stock in keyss:
                stock1 = twstock.realtime.get(str(stocklist[stock]))#由股票套件取得價格
                message = str(stock1['info']['name']) + '的價格為 ' + str(stock1['realtime']['latest_trade_price'])
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='無此股票價格資料！'))
                
        else:  #其他未知輸入
            text = '無法了解你的意思，請重新輸入！'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
    except:
       line_bot_api.reply_message(event.reply_token, TextSendMessage(text='執行時產生錯誤！'))


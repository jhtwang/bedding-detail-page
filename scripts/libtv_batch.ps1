# LibTV 批量出图（床品详情页）：建组→上传参考图→建节点→整组生成→解除→下载
# 用法：按需修改 <产品前缀>/<组名>/<参考图与提示词>，逐段执行
$pre = "电商详情页长图，高端家居床品品牌「乐优家」，产品「<产品名>」，<风格描述>，<配色>，<风格元素>，画面干净高级、留白充足、柔和自然光，8K质感。画面文字一律使用免费可商用字体，禁止使用商业字体。 "
$GROUP = "<组名>"
libtv group create $GROUP
libtv group use $GROUP
# 上传参考图（自动进组）
# libtv upload "<前缀>参考_首屏" -f <首屏参考.jpg>
# libtv upload "<前缀>参考_卖点1" -f <卖点1透明.png>
# ...
$common = @("-s","model=Lib Image 2.5 Pro","-s","count=1","-s","quality=high","-s","resolution=2K","-s","template=一键电商爆款产品详情页长图整套全案设计")
# 建节点（image2image 用 --left；规格/洗涤用 -s modeType=text2image）
# libtv node create "<前缀>模块1_首屏" -t image --prompt $pre + "首屏主视觉..." @common -s modeType=image2image -s ratio=3:4 --left "<前缀>参考_首屏"
# libtv node create "<前缀>模块8_规格材质" -t image --prompt $pre + "规格材质模块..." @common -s modeType=text2image -s ratio=3:4
# 整组生成
libtv group $GROUP --run
libtv group unuse
# 下载（必带去水印参数）
# libtv download -n "<前缀>模块1_首屏" -o <输出目录> --without-ai-watermark --vip
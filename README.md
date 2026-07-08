# Py2EXE Builder

涓€涓熀浜?tkinter 鐨?Python 鍥惧舰鍖栨墦鍖呭伐鍏凤紝灏?Python 鑴氭湰鎵撳寘涓虹嫭绔嬪彲鎵ц鐨?EXE 鏂囦欢銆?
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/)

## 鍔熻兘鐗规€?
- **涓ょ鎵撳寘妯″紡**
  - 鍗曟枃浠舵ā寮?(onefile) 鈥?鎵€鏈夊唴瀹瑰悎骞朵负涓€涓?EXE 鏂囦欢
  - 鏂囦欢澶规ā寮?(onedir) 鈥?杈撳嚭鍖呭惈鎵€鏈変緷璧栫殑鏂囦欢澶?
- **鎵撳寘閫夐」**
  - 闅愯棌鎺у埗鍙扮獥鍙?鈥?鍚姩 EXE 鏃朵笉寮瑰嚭榛戣壊 CMD 绐楀彛
  - 绠＄悊鍛樻潈闄?(UAC) 鈥?璇锋眰绠＄悊鍛樻潈闄愯繍琛?
- **鑷畾涔夊浘鏍?*
  - 鏀寔涓烘墦鍖呭悗鐨?EXE 璁剧疆鑷畾涔夊浘鏍?(.ico 鏍煎紡)
  - 涓嶈缃垯浣跨敤榛樿鍥炬爣

- **鐩綍绠＄悊**
  - 鑷畾涔夎緭鍑虹洰褰?  - 鑷畾涔夌紦瀛樼洰褰曪紙鏋勫缓涓存椂鏂囦欢锛?
- **渚濊禆绠＄悊**
  - 涓€閿畨瑁?鏇存柊 PyInstaller
  - 鑷姩妫€娴?PyInstaller 鐗堟湰

- **鐢ㄦ埛浣撻獙**
  - 娣辫壊涓婚鐣岄潰
  - 瀹炴椂鏋勫缓鏃ュ織
  - 鎵撳寘杩涘害鏄剧ず
  - 鍏ㄥ眬寮傚父鎹曡幏涓庢棩蹇楄褰?
## 蹇€熷紑濮?
### 鏂瑰紡涓€锛氱洿鎺ヨ繍琛?EXE

1. 涓嬭浇 [Releases](https://github.com/Honest16888/py2exe_builder/releases) 涓殑 `Py2EXE_Builder.exe`
2. 鍙屽嚮杩愯
3. 閫夋嫨 Python 鑴氭湰锛岀偣鍑?寮€濮嬫墦鍖?

### 鏂瑰紡浜岋細浠庢簮鐮佽繍琛?
```bash
# 鍏嬮殕浠撳簱
git clone https://github.com/Honest16888/py2exe_builder.git
cd py2exe_builder

# 瀹夎渚濊禆
pip install pyinstaller

# 杩愯
python py2exe_builder.pyw
```

## 浣跨敤璇存槑

1. **閫夋嫨鑴氭湰** 鈥?鐐瑰嚮"娴忚"閫夋嫨瑕佹墦鍖呯殑 `.py` 鏂囦欢
2. **閫夋嫨妯″紡** 鈥?鍗曟枃浠舵垨鏂囦欢澶规ā寮?3. **璁剧疆閫夐」** 鈥?闅愯棌鎺у埗鍙般€佺鐞嗗憳鏉冮檺绛?4. **璁剧疆鍥炬爣** 鈥?鍙€夛紝涓?EXE 璁剧疆鑷畾涔夊浘鏍?5. **璁剧疆鐩綍** 鈥?杈撳嚭鐩綍鍜岀紦瀛樼洰褰?6. **瀹夎渚濊禆** 鈥?棣栨浣跨敤鐐瑰嚮"瀹夎/鏇存柊 PyInstaller"
7. **寮€濮嬫墦鍖?* 鈥?鐐瑰嚮"寮€濮嬫墦鍖?鎸夐挳

## 绯荤粺瑕佹眰

- Windows 10/11
- Python 3.9 鎴栨洿楂樼増鏈?- PyInstaller锛堝伐鍏蜂細鑷姩妫€娴嬪拰瀹夎锛?
## 鏋勫缓 EXE

濡傛灉浣犳兂灏嗘湰宸ュ叿涔熸墦鍖呬负 EXE锛?
```bash
pip install pyinstaller

pyinstaller --noconfirm --clean --onefile --windowed ^
  --icon=app_icon.ico ^
  --name Py2EXE_Builder ^
  py2exe_builder.pyw
```

鐢熸垚鐨?EXE 鏂囦欢浣嶄簬 `dist/` 鐩綍銆?
## 椤圭洰缁撴瀯

```
py2exe_builder/
鈹溾攢鈹€ py2exe_builder.pyw    # 涓荤▼搴忔簮鐮?鈹溾攢鈹€ app_icon.ico          # 搴旂敤鍥炬爣
鈹溾攢鈹€ Py2EXE_Builder.exe    # 鎵撳寘濂界殑鍙墽琛屾枃浠?鈹溾攢鈹€ LICENSE               # MIT 璁稿彲璇?鈹溾攢鈹€ README.md             # 椤圭洰璇存槑
鈹溾攢鈹€ CONTRIBUTING.md       # 璐＄尞鎸囧崡
鈹斺攢鈹€ .gitignore            # Git 蹇界暐鏂囦欢
```

## 璐＄尞

娆㈣繋璐＄尞浠ｇ爜锛佽闃呰 [CONTRIBUTING.md](CONTRIBUTING.md) 浜嗚В璇︽儏銆?
## 璁稿彲璇?
鏈」鐩噰鐢?[MIT 璁稿彲璇乚(LICENSE)銆?
## 鑷磋阿

- [PyInstaller](https://pyinstaller.org/) 鈥?Python 鎵撳寘宸ュ叿
- [tkinter](https://docs.python.org/3/library/tkinter.html) 鈥?Python GUI 搴?
## 鑱旂郴鏂瑰紡

- Issues: [GitHub Issues](https://github.com/Honest16888/py2exe_builder/issues)
- Email: 3167504185@qq.com

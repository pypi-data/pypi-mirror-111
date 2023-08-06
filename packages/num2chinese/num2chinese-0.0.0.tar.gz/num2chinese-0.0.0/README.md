# num2chinese
## A nlp tool to transform numbers to Chinese

`num2chinese` uses regular expression to parse alphanumeric literals and transform them into readable Chinese charaters.

## Why it matters
- Chinese's pronuncication has lots of exceptions.
- For Chinese numbers, a character is uttered dependent of context.
- Lots of rules are required to handle messy Chinese number pronunciation. Dont' reinvent the wheel!

## Examples
- $120 : 美金一百二十
- 200塊 : 兩百塊
- 12121212個蘋果 : 一千兩百一十二萬一千兩百一十二個蘋果
- 2002002支 : 兩百萬兩千零二支
- 9487 : 九四八七
- 080080123 : 零八零零八零一二

## Usage
```
text = '12121212個蘋果''
normalizer = InverseNormalizer()
text_normalized = normalizer.normalize(text)
print(text_normalized)
# result is '一千兩百萬十二萬一千兩百一十二個蘋果'
```
## Installation

`pip install num2chinese`

## Requirements

`python>=3.2,<4.0`

## License
MIT license


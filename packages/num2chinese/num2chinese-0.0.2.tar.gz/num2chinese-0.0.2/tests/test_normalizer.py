from num2chinese.normalizer import Normalizer


def test_currenncy():
    normalizer = Normalizer()
    assert normalizer.normalize("$120") == "美金一百二十"
    assert normalizer.normalize("200塊") == "兩百塊"
    assert normalizer.normalize("€21212") == "兩萬一千兩百一十二歐元"


def test_serial():
    normalizer = Normalizer()
    assert normalizer.normalize("9487") == "九四八七"
    assert normalizer.normalize("080080123") == "零八零零八零一二三"


def test_number():
    normalizer = Normalizer()
    assert normalizer.normalize("2002002支") == "兩百萬兩千零二支"
    assert normalizer.normalize("1002根") == "一千零二根"

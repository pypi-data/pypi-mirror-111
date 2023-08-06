# -*- coding: utf-8 -*-
import re


class Normalizer:
    def __init__(self, debug=False):
        self.number2character = {
            1: "一",
            2: "兩",
            3: "三",
            4: "四",
            5: "五",
            6: "六",
            7: "七",
            8: "八",
            9: "九",
            0: "零",
        }
        self.digit2character = {
            1: "一",
            2: "二",
            3: "三",
            4: "四",
            5: "五",
            6: "六",
            7: "七",
            8: "八",
            9: "九",
            0: "零",
            ".": "點",
        }
        ### EMAIL PATTERN ###
        self.email_pattern = re.compile(
            r"(\w+(?:[\.-]?\w+)*@\w+(?:[\.-]?\w+)*(?:\.\w{2,3})+)"
        )
        ### URL PATTERN ###
        self.url_pattern = re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )
        ### SEPARATOR ###
        # self.pattern_separator = re.compile('[\:\：、,，。\？\?\!\！]')
        self.pattern_separator = re.compile(r"[\:\：；、。\？\?\!\！]")
        ### REMOVE ###
        self.pattern_remove = re.compile(r"[\(\（][^\)\(\）\）]+[\)\）]")
        ### SPACE REDUCTION ###
        self.pattern_space_reduction = re.compile("(  )[ ]*")
        ### General number ###
        self.pattern_number = re.compile(r"(\-)?\s*([0-9]+)(\.*)([0-9]*)")
        ### General countable ###
        self.pattern_countable = re.compile(
            r"(\-*\s*[0-9]+\.*[0-9]*)\s*(多)*\s*(種|人|國|家|週|碼|個|位|條|只|匹|頭|條|峰|顆|根|張|片|棵|株|朵|頓|道|塊|粒|盤|把|台|坨|件|頂|枚|座|棟|面|扇|間|堵|輛|列|架|艘|方|支|封|則|首|篇|幅|發|門|輪|陣|場|匹|回|尾|闕|網|炮|丘|襲|輛|挑|擔|殼|窠|曲|牆|群|腔|砣|客|貫|扎|捆|刀|令|打|手|羅|坡|山|嶺|江|溪|鍾|隊|單|雙|對|齣|口|頭|腳|板|跳|枝|貼|針|線|管|名|身|堂|課|本|頁|絲|毫|厘|分|錢|兩|斤|擔|銖|石|鈞|錙|忽|毫|厘|分|寸|尺|丈|里|尋|常|鋪|程|撮|勺|合|升|斗|盤|碗|碟|疊|桶|籠|盆|盒|杯|鍾|斛|鍋|簋|籃|盤|桶|罐|瓶|壺|卮|盞|籮|箱|煲|啖|袋|缽|年|月|日|季|刻|時|周|天|秒|分|旬|紀|歲|世|更|夜|春|夏|秋|冬|代|伏|輩|丸|泡|粒|顆|幢|堆|屆)*\s*(\-|~)?\s*(\-*\s*[0-9]+\.*[0-9]*)?\s*(多)*\s*(種|人|國|家|週|碼|個|位|條|只|匹|頭|條|峰|顆|根|張|片|棵|株|朵|頓|道|塊|粒|盤|把|台|坨|件|頂|枚|座|棟|面|扇|間|堵|輛|列|架|艘|方|支|封|則|首|篇|幅|發|門|輪|陣|場|匹|回|尾|闕|網|炮|丘|襲|輛|挑|擔|殼|窠|曲|牆|群|腔|砣|客|貫|扎|捆|刀|令|打|手|羅|坡|山|嶺|江|溪|鍾|隊|單|雙|對|齣|口|頭|腳|板|跳|枝|貼|針|線|管|名|身|堂|課|本|頁|絲|毫|厘|分|錢|兩|斤|擔|銖|石|鈞|錙|忽|毫|厘|分|寸|尺|丈|里|尋|常|鋪|程|撮|勺|合|升|斗|盤|碗|碟|疊|桶|籠|盆|盒|杯|鍾|斛|鍋|簋|籃|盤|桶|罐|瓶|壺|卮|盞|籮|箱|煲|啖|袋|缽|年|月|日|季|刻|時|周|天|秒|分|旬|紀|歲|世|更|夜|春|夏|秋|冬|代|伏|輩|丸|泡|粒|顆|幢|堆|屆)"
        )
        ### Currency ###
        self.pattern_currency = re.compile(
            r"(\$|€|¥|£|美金|美元|美圓|日圓|日元|台幣|新台幣|臺幣|歐元|英鎊|泰銖|披索|馬幣|加幣|新加坡幣)\s*(\-*\s*[0-9]+\.*[0-9]*)(\s*[-~～到]\s*)?(\$|€|¥|£|美金|美元|美圓|日圓|日元|台幣|新台幣|臺幣|歐元|英鎊|泰銖|披索|馬幣|加幣|新加坡幣)?(\-*\s*[0-9]+\.*[0-9]*)?"
        )
        self.pattern_currency2 = re.compile(
            r"(\-*\s*[0-9]+\.*[0-9]*)(元|圓|美金|美元|美圓|日圓|日元|台幣|新台幣|臺幣|歐元|英鎊|泰銖|披索|馬幣|加幣|新加坡幣)?(\s*[-~～到]\s*)?(\-*\s*[0-9]+\.*[0-9]*)?\s*(元|圓|美金|美元|美圓|日圓|日元|台幣|新台幣|臺幣|歐元|英鎊|泰銖|披索|馬幣|加幣|新加坡幣)"
        )
        ### SERIAL NUMBER ###
        self.pattern_serial = re.compile(r"(?<!\d)([\d\.]*[\d]+)(?!\d)")
        ### ###
        self.debug = debug

    def full_to_half(self, text):
        """
        Convert full-width character to half-width one.
        """

        def convert(char):
            num = ord(char)
            if num == 0x3000:  # space
                num = 32
            elif num == 0x3001:  # comma
                num = 44
            elif num == 0x3002:  # full stop
                num = 46
            elif num == 0xFF03:  # full hashtag ＃
                num = 35
            elif 0xFF01 <= num <= 0xFF5E:  # full width digits and alphabets
                num -= 0xFEE0
            elif 0x3008 <= num <= 0x301B:  # parentheses
                num = 40 if (num & 1) == 0 else 41
            return chr(num)

        return "".join(map(convert, text))

    def clean(self, text):
        text = self.pattern_remove.sub("", text)
        text = self.pattern_separator.sub(" ` ", text)
        text = self.full_to_half(text).lower()  # 會把全形句號變成小數點
        return text

    def _to_thousand(self, number, has_larger_part, is_last_zero):
        assert isinstance(number, int)
        assert number < 10000
        # if number == 0 and add_zero:
        #     return self.number2character[0]
        # elif number == 0 and not add_zero:
        #     return ""
        if number == 0:
            return ""
        result = ""

        thousand, remainder = divmod(number, 1000)
        is_zero = True if thousand == 0 else False
        condition = has_larger_part and is_last_zero and not is_zero
        if condition:
            result += self.number2character[0] + self.number2character[thousand] + "千"
        elif not is_zero:
            result += self.number2character[thousand] + "千"
        if self.debug:
            print(
                "[INFO] thousand: {}, remainder: {}, is_zero: {}, has_larger_part: {}, is_last_zero:{}".format(
                    thousand, remainder, is_zero, has_larger_part, is_last_zero
                )
            )
        has_larger_part = has_larger_part or not is_zero  # 更大的數值：要嘛前面已經有，要嘛現在數字就是
        is_last_zero = is_zero

        hundred, remainder = divmod(remainder, 100)
        is_zero = True if hundred == 0 else False
        condition = has_larger_part and is_last_zero and not is_zero
        if condition:
            result += self.number2character[0] + self.number2character[hundred] + "百"
            # add_zero = True
        elif not is_zero:
            result += self.number2character[hundred] + "百"
        if self.debug:
            print(
                "[INFO] hundred: {}, remainder: {}, is_zero: {}, has_larger_part: {}, is_last_zero:{}".format(
                    hundred, remainder, is_zero, has_larger_part, is_last_zero
                )
            )
        has_larger_part = has_larger_part or not is_zero  # 更大的數值：要嘛前面已經有，要嘛現在數字就是
        is_last_zero = is_zero

        ten, digit = divmod(remainder, 10)
        is_zero = True if ten == 0 else False
        condition = has_larger_part and is_last_zero and not is_zero
        if ten == 1 and not has_larger_part:
            ten_char = ""
        elif ten == 2:
            ten_char = self.digit2character[ten]
        else:
            ten_char = self.number2character[ten]
        # ten_char="" if ten==1 and not has_larger_part else self.number2character[ten]
        if condition:
            result += self.number2character[0] + ten_char + "十"
        elif not is_zero:
            result += ten_char + "十"
        if self.debug:
            print(
                "[INFO] ten: {}, digit: {}, is_zero: {}, has_larger_part: {}, is_last_zero:{}".format(
                    ten, digit, is_zero, has_larger_part, is_last_zero
                )
            )
        has_larger_part = has_larger_part or not is_zero  # 更大的數值：要嘛前面已經有，要嘛現在數字就是
        is_last_zero = is_zero

        is_zero = True if digit == 0 else False
        condition = has_larger_part and is_last_zero and not is_zero
        if digit == 2:
            if has_larger_part:
                digit_char = self.digit2character[digit]
            else:
                digit_char = self.number2character[digit]
        else:
            digit_char = self.number2character[digit]
        if condition:
            result += self.number2character[0] + digit_char
        elif not is_zero:
            result += digit_char
        if self.debug:
            print(
                "[INFO] digit: {}, , is_zero: {}, has_larger_part: {}, is_last_zero:{}".format(
                    digit, is_zero, has_larger_part, is_last_zero
                )
            )
        return result

    def normalize_email(self, text):
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        nrm_text = self.email_pattern.sub("", text)
        return nrm_text

    def normalize_url(self, text):
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        nrm_text = self.url_pattern.sub("", text)
        return nrm_text

    def cur2han(self, unit, num):
        unit = unit or ""
        num = num or ""
        if unit == "€":
            return "{}歐元".format(num)
        elif unit == "$":
            return "美金{}".format(num)
        elif unit == "¥":
            return "人民幣{}元".format(num)
        elif unit == "£":
            return "{}英鎊".format(num)
        else:
            return "{}{}".format(num, unit)

    def normalize_number(self, text):
        """normalize (countable) number, including integer and float."""
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        nrm_text = text
        for item in reversed(list(self.pattern_number.finditer(nrm_text))):
            start_idx, end_idx = item.span()
            minus, integer, dot, digit = item.groups()
            integer = self.normalize_int(integer) if integer is not None else None
            digit = self.normalize_digit(digit) if digit is not None else None
            minus = "負" if minus is not None else ""
            if dot != "":
                nrm_text = (
                    nrm_text[:start_idx]
                    + minus
                    + "{}點{}".format(integer, digit)
                    + nrm_text[end_idx:]
                )
            else:
                nrm_text = (
                    nrm_text[:start_idx]
                    + minus
                    + "{}".format(integer)
                    + nrm_text[end_idx:]
                )
        return nrm_text

    def normalize_currency(self, text):
        """Convert text to currency

        Example
                        2019  2019
                        $ 2019 二千零一十九元
                        $12345678 一千二百三十四萬五千六百七十八元
                        €980000301  九億八千萬零三百零一歐元
        """
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        nrm_text = text
        ### 單位在前方 ###
        for item in reversed(list(self.pattern_currency.finditer(nrm_text))):
            start_idx, end_idx = item.span()
            unit1 = item.groups()[0]
            num1 = self.normalize_number(item.groups()[1])
            num1 = self.cur2han(unit1, num1)

            fromto = "到" if item.groups()[2] is not None else ""

            num2 = (
                self.normalize_number(item.groups()[4])
                if item.groups()[4] is not None
                else None
            )
            unit2 = item.groups()[3] or unit1 if num2 is not None else ""
            num2 = self.cur2han(unit2, num2)
            full = num1 + fromto + num2

            nrm_text = nrm_text[:start_idx] + full + nrm_text[end_idx:]

        ### 單位在後方 ###
        for item in reversed(list(self.pattern_currency2.finditer(nrm_text))):
            start_idx, end_idx = item.span()
            num1 = self.normalize_number(item.groups()[0])
            unit1 = item.groups()[1] or item.groups()[4]
            num1 = self.cur2han(unit1, num1)

            fromto = "到" if item.groups()[2] is not None else ""

            num2 = (
                self.normalize_number(item.groups()[3])
                if item.groups()[3] is not None
                else None
            )
            unit2 = item.groups()[4] if num2 is not None else ""
            num2 = self.cur2han(unit2, num2)
            full = num1 + fromto + num2

            nrm_text = nrm_text[:start_idx] + full + nrm_text[end_idx:]
        return nrm_text

    def normalize_int(self, text):
        assert isinstance(text, str)
        try:
            number = int(text)
        except ValueError:
            print("{} cannot be converted to number.".format(text))
            raise
        if number >= 1000000000000000:  # 萬兆
            print("{} is greater than what we can convert to Chinese.".format(number))
            return text
        if number == 0:
            return self.number2character[number]

        zhao, remainder = divmod(number, 1000000000000)
        has_larger_part = False
        is_last_zero = False
        zhao = (
            self._to_thousand(zhao, has_larger_part, is_last_zero) + "兆"
            if zhao > 0
            else ""
        )
        is_zero = True if zhao == "" else False
        has_larger_part = has_larger_part or not is_zero  # 更大的數值：要嘛前面已經有，要嘛現在數字就是
        is_last_zero = is_zero

        yi, remainder = divmod(remainder, 100000000)
        yi = (
            self._to_thousand(yi, has_larger_part, is_last_zero) + "億" if yi > 0 else ""
        )
        is_zero = True if yi == "" else False
        has_larger_part = has_larger_part or not is_zero  # 更大的數值：要嘛前面已經有，要嘛現在數字就是
        is_last_zero = is_zero

        wan, remainder = divmod(remainder, 10000)
        wan = (
            self._to_thousand(wan, has_larger_part, is_last_zero) + "萬"
            if wan > 0
            else ""
        )
        is_zero = True if wan == "" else False
        has_larger_part = has_larger_part or not is_zero  # 更大的數值：要嘛前面已經有，要嘛現在數字就是
        is_last_zero = is_zero

        remainder = (
            self._to_thousand(remainder, has_larger_part, is_last_zero)
            if remainder > 0
            else ""
        )
        if self.debug:
            print(
                "zhao: {}, yi:{}, wan:{}, remainder:{}".format(zhao, yi, wan, remainder)
            )
        return zhao + yi + wan + remainder

    def normalize_digit(self, text):
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        # try:
        #     number = int(text)
        # except ValueError:
        #     print("{} cannot be converted to number.".format(text))
        #     raise
        normalized_text = ""
        for c in text:
            c = int(c) if c.isdigit() else c
            normalized_text += self.digit2character[c]
        return normalized_text

    def normalize_countable(self, text):
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        nrm_text = text

        for item in reversed(list(self.pattern_countable.finditer(nrm_text))):
            start_idx, end_idx = item.span()
            (
                num_left,
                more_left,
                unit_left,
                fromto,
                num_right,
                more_right,
                unit_right,
            ) = item.groups()
            num_left = self.normalize_number(num_left)
            more_left = more_left or ""
            more_right = more_right or ""
            fromto = "到" if fromto else ""
            unit_left = unit_left or ""
            unit_right = unit_right or ""
            num_right = self.normalize_number(num_right) if num_right else ""
            # if fromto=='':
            #     nrm_text = nrm_text[ : start_idx] + num_left + unit_left + num_right + unit_right + nrm_text[ end_idx: ]
            # elif unit_left=='':
            #     nrm_text = nrm_text[ : start_idx] + num_left + fromto + num_right + unit_right + nrm_text[ end_idx: ]
            # else:
            #     nrm_text = nrm_text[ : start_idx] + num_left + unit_left + fromto + num_right + unit_right + nrm_text[ end_idx: ]
            nrm_text = (
                nrm_text[:start_idx]
                + num_left
                + more_left
                + unit_left
                + fromto
                + num_right
                + more_right
                + unit_right
                + nrm_text[end_idx:]
            )
        return nrm_text

    def normalize_serial(self, text):
        assert isinstance(text, str)
        if len(text) == 0:
            return ""
        nrm_text = text
        for item in reversed(list(self.pattern_serial.finditer(nrm_text))):
            digit = item.groups()[0]
            digit = self.normalize_digit(digit) if digit is not None else None
            start_idx, end_idx = item.span()
            nrm_text = nrm_text[:start_idx] + "{}".format(digit) + nrm_text[end_idx:]
        return nrm_text

    def normalize(self, text, skip_url=True, skip_email=True):
        assert isinstance(text, str)
        text = text.strip()
        if skip_url:
            text = self.normalize_url(text)
        if skip_email:
            text = self.normalize_email(text)
        text = self.clean(text)
        text = self.normalize_currency(text)
        text = self.normalize_countable(text)
        text = self.normalize_serial(text)
        text = self.pattern_space_reduction.sub(" ", text)
        return text


if __name__ == "__main__":
    normalizer = Normalizer()
    texts = ["$120", "200塊", "12121212個蘋果", "2002002支", "9487", "080080123", "1002根"]
    for text in texts:
        print(text, " -> ", normalizer.normalize(text))

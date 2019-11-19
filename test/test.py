import unittest
from util.summarize import Summarize
from util.tokenize import Tokenize

class TestCase(unittest.TestCase):
    def setUp(self):
        self.test_sentence = "안녕하세요. 반갑습니다."
        self.length_count_less_100 = "안녕하세요. 반갑습니다. 저는 현재 미스테리코에서 AI 개발과 백엔드 서버 개발을 담당하고 있는 Philip입니다. 오늘은 어떤 일을 해야할 지 잘 모르겠군요."
        self.length_count_less_200 = "서울 은평구 연신내의 한 맥도날드 매장에서 손님이 음식이 든 봉투를 매장 직원에게 던지는 영상이 뒤늦게 공개돼 논란인 가운데, 경찰은 손님이 즉시 사과했고 상황이 일단락됐다라고 밝혔다. 6일 서울 은평경찰서에 따르면 지난달 17일 해당 매장에 지구대가 출동했지만 피해자인 직원이 처벌 의사가 없다고 밝혔다."
        self.length_count_less_300 = "서울 은평구 연신내의 한 맥도날드 매장에서 손님이 음식이 든 봉투를 매장 직원에게 던지는 영상이 뒤늦게 공개돼 논란인 가운데, 경찰은 손님이 즉시 사과했고 상황이 일단락됐다라고 밝혔다. 6일 서울 은평경찰서에 따르면 지난달 17일 해당 매장에 지구대가 출동했지만 피해자인 직원이 처벌 의사가 없다고 밝혔다. 직원이 처벌 의사는 없지만 햄버거를 던진 행동에 대해 사과를 받고 싶다고 하자 손님이 즉시 사과했다고 경찰은 전했다."
        self.length_count_less_400 = "서울 은평구 연신내의 한 맥도날드 매장에서 손님이 음식이 든 봉투를 매장 직원에게 던지는 영상이 뒤늦게 공개돼 논란인 가운데, 경찰은 손님이 즉시 사과했고 상황이 일단락됐다라고 밝혔다. 6일 서울 은평경찰서에 따르면 지난달 17일 해당 매장에 지구대가 출동했지만 피해자인 직원이 처벌 의사가 없다고 밝혔다. 직원이 처벌 의사는 없지만 햄버거를 던진 행동에 대해 사과를 받고 싶다고 하자 손님이 즉시 사과했다고 경찰은 전했다. 이날 맥도날드 관계자도 동아닷컴에 경찰 입회하에 손님이 직원에게 사과했다. 직원은 그 사과를 받아들였고. 사건은 종결됐다라고 말했다. 단 영상이 온라인에 퍼지는 것에 대해선 영상 속 직원이 심적으로 힘들어하고 있다고 걱정했다."
        self.length_count_over_400 = "서울 은평구 연신내의 한 맥도날드 매장에서 손님이 음식이 든 봉투를 매장 직원에게 던지는 영상이 뒤늦게 공개돼 논란인 가운데, 경찰은 손님이 즉시 사과했고 상황이 일단락됐다라고 밝혔다. 6일 서울 은평경찰서에 따르면 지난달 17일 해당 매장에 지구대가 출동했지만 피해자인 직원이 처벌 의사가 없다고 밝혔다. 직원이 처벌 의사는 없지만 햄버거를 던진 행동에 대해 사과를 받고 싶다고 하자 손님이 즉시 사과했다고 경찰은 전했다. 이날 맥도날드 관계자도 동아닷컴에 경찰 입회하에 손님이 직원에게 사과했다. 직원은 그 사과를 받아들였고. 사건은 종결됐다라고 말했다. 단 영상이 온라인에 퍼지는 것에 대해선 영상 속 직원이 심적으로 힘들어하고 있다고 걱정했다. 한편 이날 새벽 유튜브에는 지난달 17일 연신내의 맥도날드 매장에서 손님이 직원에게 음식물이 든 봉투를 던지는 영상이 게재됐다. 현장에 있었다는 누리꾼은 알바(아르바이트생이)가 번호를 계속 불렀는데 (손님들이) 뭘 하고 있었는지 못 들었다라며 실랑이를 벌이다 손님이 직원에게 음식물이 든 봉투를 던졌다고 당시 상황을 전했다. 이에 누리꾼들은 또 갑질이냐?, 왜 말로 하지 던지냐, 진짜 손이 덜덜 떨린다 등의 반응을 보였다."

    def test_attribute_runs(self):
        self.right_case = Tokenize(self.test_sentence)
        self.right_summary = Summarize(self.test_sentence)

    def test_summary_runs(self):
        summary_under_100 = Summarize(self.length_count_less_100)
        summary_under_200 = Summarize(self.length_count_less_200)
        summary_under_300 = Summarize(self.length_count_less_300)
        summary_under_400 = Summarize(self.length_count_less_400)

        self.assertEqual(len(summary_under_100.summarize()), 1)
        self.assertEqual(len(summary_under_200.summarize()), 2)
        self.assertEqual(len(summary_under_300.summarize()), 3)
        self.assertEqual(len(summary_under_400.summarize()), 4)

if __name__ == '__main__':
    unittest.main()
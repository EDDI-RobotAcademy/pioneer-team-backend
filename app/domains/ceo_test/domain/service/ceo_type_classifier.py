from app.domains.ceo_test.domain.value_object.answer import AnswerChoice
from app.domains.ceo_test.domain.value_object.axis import EmpathyAxis, JudgingAxis
from app.domains.ceo_test.domain.value_object.ceo_type import CEOType
from app.domains.ceo_test.domain.value_object.score import Score


REQUIRED_QUESTIONS = 20

EXTREME_TI_TE = CEOType(
    code="EXTREME_TI_TE",
    name="완전체 해결형",
    description="맞는지와 되는지를 동시에 보면서, 감정을 분석 대상으로 처리하는 타입",
)
EXTREME_TE = CEOType(
    code="EXTREME_TE",
    name="순수 실행형",
    description="되는지 보면서, 감정은 판단에 거의 사용하지 않는 타입",
)
EXTREME_FE = CEOType(
    code="EXTREME_FE",
    name="순수 공감형",
    description="타인의 반응을 읽는 것을 중심으로 판단까지 맞추는 타입",
)
EXTREME_TI = CEOType(
    code="EXTREME_TI",
    name="순수 논리형",
    description="맞는지만 따지며, 감정과 현실보다 논리 일관성을 우선하는 타입",
)
EXTREME_FI = CEOType(
    code="EXTREME_FI",
    name="순수 감정형",
    description="스스로 느끼는 감정을 기준으로 판단하며, 논리나 상황보다 내 기준을 우선하는 타입",
)
FULL_BALANCED = CEOType(
    code="FULL_BALANCED",
    name="완전 균형형",
    description="상황에 따라 판단을 바꾸면서, 느끼기도 하고 읽기도 하는 타입",
)

JUDGING_PHRASE: dict[JudgingAxis, str] = {
    JudgingAxis.Ti: "맞는지 따지면서",
    JudgingAxis.Te: "되는지 보면서",
    JudgingAxis.BALANCED: "상황에 따라 판단을 바꾸면서",
}

EMPATHY_PHRASE: dict[EmpathyAxis, str] = {
    EmpathyAxis.Fi: "스스로 느껴 공감하는 타입",
    EmpathyAxis.Fe: "타인의 반응을 읽어 공감하는 타입",
    EmpathyAxis.BALANCED: "느끼기도 하고 읽기도 하는 타입",
}


class InvalidSubmissionError(Exception):
    pass


def calculate_score(answers: list[AnswerChoice]) -> Score:
    ti = sum(1 for a in answers if a == AnswerChoice.A)
    te = sum(1 for a in answers if a == AnswerChoice.B)
    fi = sum(1 for a in answers if a == AnswerChoice.C)
    fe = sum(1 for a in answers if a == AnswerChoice.D)
    return Score(ti=ti, te=te, fi=fi, fe=fe)


def determine_judging_axis(score: Score) -> JudgingAxis:
    if abs(score.ti - score.te) <= 2:
        return JudgingAxis.BALANCED
    if score.ti > score.te:
        return JudgingAxis.Ti
    return JudgingAxis.Te


def determine_empathy_axis(score: Score) -> EmpathyAxis:
    if abs(score.fi - score.fe) <= 2:
        return EmpathyAxis.BALANCED
    if score.fi > score.fe:
        return EmpathyAxis.Fi
    return EmpathyAxis.Fe


def find_extreme_type(score: Score) -> CEOType | None:
    if score.ti >= 8 and score.te >= 8 and score.fi <= 2 and score.fe <= 2:
        return EXTREME_TI_TE
    if score.te >= 10 and score.fi <= 2 and score.fe <= 2:
        return EXTREME_TE
    if score.fe >= 10 and score.ti <= 3 and score.te <= 5:
        return EXTREME_FE
    if score.ti >= 10 and score.fi <= 3 and score.fe <= 3:
        return EXTREME_TI
    if score.fi >= 10 and score.ti <= 3 and score.te <= 3:
        return EXTREME_FI
    return None


def build_basic_type(judging: JudgingAxis, empathy: EmpathyAxis) -> CEOType:
    if judging == JudgingAxis.BALANCED and empathy == EmpathyAxis.BALANCED:
        return FULL_BALANCED
    code = f"{judging.value}_{empathy.value}".upper()
    name = f"{judging.value}-{empathy.value}형"
    description = f"{JUDGING_PHRASE[judging]}, {EMPATHY_PHRASE[empathy]}"
    return CEOType(code=code, name=name, description=description)


def validate_answers(answers: list[AnswerChoice]) -> None:
    if len(answers) != REQUIRED_QUESTIONS:
        raise InvalidSubmissionError(
            f"답변 수는 정확히 {REQUIRED_QUESTIONS}개여야 합니다."
        )


def classify(answers: list[AnswerChoice]) -> CEOType:
    validate_answers(answers)
    score = calculate_score(answers)
    extreme = find_extreme_type(score)
    if extreme is not None:
        return extreme
    judging = determine_judging_axis(score)
    empathy = determine_empathy_axis(score)
    return build_basic_type(judging, empathy)

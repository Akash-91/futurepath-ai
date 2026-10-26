from app.education_recovery import recover_education_from_text


def test_recovers_degree_pipe_institution_with_years():
    text = """EDUCATION
B.Tech | University of Pune | Computer Engineering | 2018 – 2022
PROJECTS
FuturePath AI
"""
    education = recover_education_from_text(text)
    assert len(education) == 1
    assert education[0]["institution"] == "University of Pune"
    assert education[0]["qualification"] == "B.Tech"
    assert education[0]["field_of_study"] == "Computer Engineering"
    assert education[0]["start_date"] == "2018-01-01"
    assert education[0]["end_date"] == "2022-01-01"


def test_recovers_institution_first_format():
    text = """EDUCATION
Indian Institute of Technology Bombay — M.Tech — Computer Science — 2020 – 2022
CERTIFICATIONS
AWS Certified Developer
"""
    education = recover_education_from_text(text)
    assert len(education) == 1
    assert education[0]["institution"] == "Indian Institute of Technology Bombay"


def test_does_not_cross_into_next_section():
    text = """EDUCATION
B.Tech | University of Pune | 2018 – 2022
PROFESSIONAL EXPERIENCE
Software Engineer — Example Corp | Jan 2023 – Present
"""
    education = recover_education_from_text(text)
    assert len(education) == 1
    assert education[0]["institution"] == "University of Pune"

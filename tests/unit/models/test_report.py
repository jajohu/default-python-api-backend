from app.models.report import Report


def test_report():
    report = Report(id=1, name="test report name", credit_cost=1.3)
    assert report.id == 1
    assert report.name == "test report name"
    assert report.credit_cost == 1.3
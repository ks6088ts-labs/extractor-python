from main import get_extra_body


def test_get_extra_body():
    assert get_extra_body(False) is None
    body = get_extra_body(True)
    assert body["dataSources"][0]["type"] == "AzureComputerVision"
    assert body["enhancements"]["ocr"]["enabled"] is True
    assert body["enhancements"]["grounding"]["enabled"] is True

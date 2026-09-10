from app.services.rules import classify

def test_class_c_is_not_auto_approved():
    c,a=classify("DIMENSION_CHANGED")
    assert c=="C"
    assert a=="ENGINEERING_APPROVAL_REQUIRED"

def test_text_is_class_a():
    c,a=classify("TEXT_CHANGED")
    assert c=="A"

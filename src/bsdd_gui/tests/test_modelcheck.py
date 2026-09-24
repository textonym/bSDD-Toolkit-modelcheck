from types import SimpleNamespace

from bsdd_json import BsddClass, BsddClassProperty, BsddDictionary, BsddProperty

from bsdd_gui.plugins.modelcheck.core import modelcheck
from bsdd_gui.plugins.modelcheck.module import constants


def test_check_datatype_accepts_numeric_and_boolean_strings():
    assert modelcheck.check_datatype("3.5", "Real")[0]
    assert modelcheck.check_datatype("false", "Boolean")[0]


def test_check_element_reports_property_issues(monkeypatch):
    dictionary = BsddDictionary(
        OrganizationCode="org",
        DictionaryCode="demo",
        DictionaryVersion="1.0",
        LanguageIsoCode="en-US",
        LanguageOnly=False,
        UseOwnUri=False,
    )
    prop = BsddProperty(Code="Height", Name="Height", DataType="Real", MinInclusive=0, MaxInclusive=10)
    dictionary.Properties.append(prop)

    bsdd_class = BsddClass(Code="Wall", Name="Wall")
    class_prop = BsddClassProperty(
        Code="height",
        PropertyCode="Height",
        PropertySet="Pset_Test",
        IsRequired=True,
    )
    bsdd_class.ClassProperties.append(class_prop)
    dictionary.Classes.append(bsdd_class)
    bsdd_class._set_parent(dictionary)

    monkeypatch.setattr(
        modelcheck,
        "extract_psets",
        lambda _: {"Pset_Test": {"Height": "bad"}},
    )

    issues = []
    modelcheck.check_element(SimpleNamespace(GlobalId="GUID-1", is_a=lambda: "IfcWall"), bsdd_class, issues)

    assert issues
    assert any(issue["issue_type"] == constants.DATATYPE_ISSUE for issue in issues)

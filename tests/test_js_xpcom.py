from js_helper import _do_test_raw


def test_xmlhttprequest():
    """Tests that the XPCOM XHR yields the standard XHR."""

    err = _do_test_raw("""
    // Accessing a member on Components.classes is a wildcard
    var class_ = Components.interfaces.nsIXMLHttpRequest;
    var req = Components.classes["foo.bar"]
                        .createInstance(class_);
    """)
    print "XHR Class:", err.final_context.get("class_").value
    req = err.final_context.get("req").value
    print "Req:", req

    assert "value" in req
    assert "open" in req["value"]


def test_evalinsandbox():
    """Tests that Components.utils.evalInSandbox() is treated like eval."""

    err = _do_test_raw("""
    var Cu = Components.utils;
    Cu.foo("bar");
    """)
    assert not err.failed()

    err = _do_test_raw("""
    var Cu = Components.utils;
    Cu.evalInSandbox("foo");
    """)
    assert err.failed()

    err = _do_test_raw("""
    const Cu = Components.utils;
    Cu.evalInSandbox("foo");
    """)
    assert err.failed()


def test_overwritability():
    """Tests that XPCOM globals can be overwritten"""

    assert not _do_test_raw("""
    xhr = Components.classes[""].createInstance(
        Components.interfaces.nsIXMLHttpRequest);
    xhr = "foo";
    """).failed()


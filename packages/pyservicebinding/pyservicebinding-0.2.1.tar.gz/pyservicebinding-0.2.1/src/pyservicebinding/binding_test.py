import pytest

from pyservicebinding import binding


def test_bindings(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("neo4j")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("neo4j://192.168.94.103:7687/cr")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    sb = binding.ServiceBinding()
    l = sb.bindings("mysql")
    b = l[0]
    assert b["username"] == "john"
    assert b["password"] == "L&ia6W@n7epi18a"
    assert b["url"] == "mysql://192.168.94.102:3306/school"

    l = sb.bindings("neo4j")
    b = l[0]
    assert b["username"] == "jane"
    assert b["password"] == "o4%bGt#D8v2i0ja"
    assert b["uri"] == "neo4j://192.168.94.103:7687/cr"

    l = sb.bindings("non-existing")
    assert len(l) == 0


def test_all_bindings(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("neo4j")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("neo4j://192.168.94.103:7687/cr")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    sb = binding.ServiceBinding()
    l = sb.all_bindings()
    assert len(l) == 2
    count = 0
    for b in l:
        if b["type"] == "mysql":
            count = count + 1
            assert b["username"] == "john"
            assert b["password"] == "L&ia6W@n7epi18a"
            assert b["url"] == "mysql://192.168.94.102:3306/school"

        if b["type"] == "neo4j":
            count = count + 1
            assert b["username"] == "jane"
            assert b["password"] == "o4%bGt#D8v2i0ja"
            assert b["uri"] == "neo4j://192.168.94.103:7687/cr"

    assert len(l) == 2


def test_missing_service_binding_root(tmpdir):
    sb1 = tmpdir.mkdir("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    with pytest.raises(binding.ServiceBindingRootMissingError):
        sb = binding.ServiceBinding()

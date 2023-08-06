from xsdata.codegen.container import ClassContainer
from xsdata.codegen.handlers import ClassDesignateHandler
from xsdata.models.config import GeneratorConfig
from xsdata.models.config import StructureStyle
from xsdata.models.enums import Namespace
from xsdata.utils.testing import AttrFactory
from xsdata.utils.testing import ClassFactory
from xsdata.utils.testing import FactoryTestCase


class ClassDesignateHandlerTests(FactoryTestCase):
    def setUp(self):
        super().setUp()
        self.config = GeneratorConfig()
        self.container = ClassContainer(config=self.config)
        self.handler = ClassDesignateHandler(container=self.container)

    def test_group_by_filenames(self):
        voc = "file://HL7V3/NE2008/coreschemas/voc.xsd"
        prpa = "file://HL7V3/NE2008/multicacheschemas/PRPA_MT201307UV02.xsd"
        coct = "file://HL7V3/NE2008/multicacheschemas/COCT_MT080000UV.xsd"
        foo_bar = "http://xsdata/foo/bar/schema.xsd"
        foo_common = "http://xsdata/foo/common.xsd"
        xsi = Namespace.XSI.location
        xlink = Namespace.XLINK.location

        core = ClassFactory.list(1, inner=[ClassFactory.create()], location=voc)
        multi_one = ClassFactory.list(2, location=prpa)
        multi_two = ClassFactory.list(1, location=coct)
        http_one = ClassFactory.list(1, location=foo_bar)
        http_two = ClassFactory.list(1, location=foo_common)
        local_one = ClassFactory.list(1, location=xsi)
        local_two = ClassFactory.list(1, location=xlink)

        self.container.extend(core)
        self.container.extend(multi_one)
        self.container.extend(multi_two)
        self.container.extend(http_one)
        self.container.extend(http_two)
        self.container.extend(local_one)
        self.container.extend(local_two)

        self.config.output.package = "foo.bar"

        self.handler.run()

        self.assertEqual("foo.bar.coreschemas", core[0].package)
        self.assertEqual("foo.bar.coreschemas", core[0].inner[0].package)
        self.assertEqual("foo.bar.multicacheschemas", multi_one[0].package)
        self.assertEqual("foo.bar.multicacheschemas", multi_one[1].package)
        self.assertEqual("foo.bar.multicacheschemas", multi_two[0].package)
        self.assertEqual("foo.bar.bar", http_one[0].package)
        self.assertEqual("foo.bar", http_two[0].package)
        self.assertEqual("foo.bar", local_one[0].package)
        self.assertEqual("foo.bar", local_two[0].package)

    def test_group_by_namespace(self):
        classes = [
            ClassFactory.create(qname="{a}a", location="foo"),
            ClassFactory.create(qname="{a}b", location="foo"),
            ClassFactory.create(qname="b", location="bar"),
        ]

        self.container.extend(classes)
        self.config.output.structure = StructureStyle.NAMESPACES
        self.config.output.package = "bar"

        self.handler.run()
        self.assertEqual("bar", classes[0].package)
        self.assertEqual("bar", classes[1].package)
        self.assertEqual("bar", classes[2].package)

        self.assertEqual("a", classes[0].module)
        self.assertEqual("a", classes[1].module)
        self.assertEqual("", classes[2].module)

    def test_group_all_together(self):
        classes = [
            ClassFactory.create(qname="{a}a", location="foo"),
            ClassFactory.create(qname="{a}b", location="foo"),
            ClassFactory.create(qname="b", location="bar"),
        ]

        self.container.extend(classes)
        self.config.output.structure = StructureStyle.SINGLE_PACKAGE
        self.config.output.package = "foo.bar.thug"

        self.handler.run()
        self.assertEqual("foo.bar", classes[0].package)
        self.assertEqual("foo.bar", classes[1].package)
        self.assertEqual("foo.bar", classes[2].package)

        self.assertEqual("thug", classes[0].module)
        self.assertEqual("thug", classes[1].module)
        self.assertEqual("thug", classes[2].module)

        # No sub-package
        self.config.output.package = "foo"
        self.handler.run()
        self.assertEqual("", classes[0].package)
        self.assertEqual("", classes[1].package)
        self.assertEqual("", classes[2].package)

        self.assertEqual("foo", classes[0].module)
        self.assertEqual("foo", classes[1].module)
        self.assertEqual("foo", classes[2].module)

    def test_group_by_strong_components(self):
        classes = ClassFactory.list(4)
        classes[0].attrs.append(AttrFactory.reference(classes[1].qname))
        classes[1].attrs.append(AttrFactory.reference(classes[2].qname))
        classes[2].attrs.append(AttrFactory.reference(classes[3].qname))

        self.config.output.structure = StructureStyle.CLUSTERS
        self.config.output.package = "foo.bar"
        self.container.extend(classes)

        self.handler.run()

        self.assertEqual("class_B", classes[0].module)
        self.assertEqual("class_C", classes[1].module)
        self.assertEqual("class_D", classes[2].module)
        self.assertEqual("class_E", classes[3].module)

        classes[3].attrs.append(AttrFactory.reference(classes[1].qname, circular=True))
        self.handler.run()
        self.assertEqual("class_B", classes[0].module)
        self.assertEqual("class_E", classes[1].module)
        self.assertEqual("class_E", classes[2].module)
        self.assertEqual("class_E", classes[3].module)

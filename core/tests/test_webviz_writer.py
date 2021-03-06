import unittest
import tempfile
import shutil
import os
import jinja2

from webviz._webviz_writer import WebvizWriter
from webviz.minimal_theme import minimal_theme


class TestWebvizWriter(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.env = jinja2.Environment(
            loader=jinja2.ChoiceLoader([
                jinja2.PackageLoader('webviz', 'templates'),
                minimal_theme.template_loader,
                ]),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=jinja2.StrictUndefined
        )
        self.template = self.env.get_template('main.html')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_create_dir(self):
        test_dir = os.path.join(self.tempdir, 'testdir')
        with WebvizWriter(test_dir,
                          {},
                          self.template) as writer:
            writer.set_up()

        self.assertTrue(os.path.isdir(test_dir))

    def test_not_clean_subdirs(self):
        for baddir in WebvizWriter.sub_folders:
            test_dir = os.path.join(self.tempdir, baddir)
            os.makedirs(test_dir)
            with WebvizWriter(self.tempdir,
                              {},
                              self.template) as writer:
                self.assertFalse(writer.is_clean())
                writer.clean_up()
                self.assertTrue(writer.is_clean())

    def test_write_js_file(self):
        (_, test_file) = tempfile.mkstemp(suffix='.js')
        with WebvizWriter(self.tempdir,
                          {},
                          self.template) as writer:
            writer.set_up()
            result = writer.write_js_file(test_file)
            absolute_result = os.path.join(self.tempdir, result)
            self.assertTrue(os.path.isfile(absolute_result))

    def test_write_css_file(self):
        (_, test_file) = tempfile.mkstemp(suffix='.css')
        with WebvizWriter(self.tempdir,
                          {},
                          self.template) as writer:
            writer.set_up()
            result = writer.write_css_file(test_file)
            absolute_result = os.path.join(self.tempdir, result)
            self.assertTrue(os.path.isfile(absolute_result))

    def test_resource_file(self):
        (_, test_file) = tempfile.mkstemp(suffix='.ico')
        with WebvizWriter(self.tempdir,
                          {},
                          self.template) as writer:
            writer.set_up()
            result = writer.write_resource(test_file)
            absolute_result = os.path.join(self.tempdir, result)
            self.assertTrue(os.path.isfile(absolute_result))

    def test_not_clean_index_file(self):
        test_file = os.path.join(self.tempdir, WebvizWriter.index_file)
        open(test_file, 'a').close()
        with WebvizWriter(self.tempdir,
                          {},
                          self.template) as writer:
            self.assertFalse(writer.is_clean())
            writer.clean_up()
            self.assertTrue(writer.is_clean())


if __name__ == '__main__':
    unittest.main()

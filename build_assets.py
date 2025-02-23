import io
import os
import json
import tempfile
import sass

class AssetsBuilder():
    
    def __init__(self, project_path):
        self.project_path = project_path
        self.assets = {}
    
    def build(self):
        self.check_project_for_subprojects(os.path.join(self.project_path, "static/js"))

        scss_file_string_content = ""
        for scss_file_path in self.assets["scss"]:
            scss_file_string_content += f"@import '{scss_file_path}';\n"

        static_path = os.path.join(self.project_path, "static")
        parent_static_path = os.path.abspath(os.path.join(static_path, os.pardir))
        
        list_of_xml_assets = []
        for xml_file_path in self.assets["xml"]:
            xml_file_path = xml_file_path.replace(parent_static_path, "")
            list_of_xml_assets.append(xml_file_path)

        js_file_with_xml = os.path.join(self.project_path, "static/js/app/utils/xml_assets.json")
        with open(js_file_with_xml, "w") as json_file:
            json.dump(list_of_xml_assets, json_file, indent=4, ensure_ascii=False)


        in_memory_stream_text = io.StringIO(scss_file_string_content)
        temp_sass_file = tempfile.NamedTemporaryFile(delete=False)
        with temp_sass_file as fp:
            fp.write(in_memory_stream_text.read().encode("utf-8"))


        final_string = sass.compile(
            filename=temp_sass_file.name,
            output_style="expanded",
        )

        with open(os.path.join(self.project_path, "static/css/custom.css"), "w") as file_css:
            file_css.write(final_string)

        os.unlink(temp_sass_file.name)
    
    def build_js_imports(self):
        static_path = os.path.join(self.project_path, "static", "js", "app")
        print("static_path", static_path)
        # parent_static_path = os.path.abspath(os.path.join(static_path, os.pardir))
        print("parent_static_path",static_path)
        imports = {
            "@odoo/owl": "./static/js/libs/owl.js",
        }
        for js_file_path in self.assets["js"]:
            if static_path in js_file_path:
                new_js_file_path = js_file_path.replace(static_path, "")
                new_js_file_path = new_js_file_path[1:]
                key = "@" + f"{new_js_file_path.replace('.js', '')}"
                full_js_path = f"./static/js/app/{new_js_file_path}"
                imports[key] = full_js_path

        return imports
        
        

    def check_project_for_subprojects(self, path: str | os.PathLike) -> list[str | os.PathLike]:
        list_of_scss_files = [os.path.join(self.project_path, "static/bootstrap/scss/bootstrap.scss")]
        list_of_xml_files = []
        list_of_js_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".scss"):
                    scss_file_path = os.path.join(root, file)
                    list_of_scss_files.append(scss_file_path)
                if file.endswith(".xml"):
                    xml_file_path = os.path.join(root, file)
                    list_of_xml_files.append(xml_file_path)
                if file.endswith(".js"):
                    js_file_path = os.path.join(root, file)
                    list_of_js_files.append(js_file_path)
        self.assets = {
            "xml": list_of_xml_files,
            "scss": list_of_scss_files,
            "js": list_of_js_files,
        }